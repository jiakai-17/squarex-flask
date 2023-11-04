import json
import socket
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)
app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}


# Returns a dictionary containing information about the IP address of the url
def get_domain_info(url):
    parsed_url = urlparse(url)

    ip = socket.gethostbyname(parsed_url.netloc)

    headers = {
        "origin": "https://ipgeolocation.io",
        "referer": "https://ipgeolocation.io/ip-location",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
    }

    ip_info = requests.get(f"https://api.ipgeolocation.io/ipgeo?ip={ip}", headers=headers).json()

    print("got ip info: ", ip_info)

    return {
        "ip": ip,
        "isp": ip_info['isp'],
        "organization": ip_info['organization'],
        "asn": ip_info['asn'],
        "location": ip_info['country_code2']
    }


# Returns a list of subdomains of the url using the whoisxmlapi
def get_subdomains(url):
    parsed_url = urlparse(url)

    subdomain_apikey = "at_GD9LmBn9XGBSxIWlWYCxDJtXinjht"
    main_domain = '.'.join(parsed_url.netloc.split('.')[-2:])
    subdomains_info = requests.get(
        f"https://subdomains.whoisxmlapi.com/api/v1?apiKey={subdomain_apikey}&domainName={main_domain}").json()

    print("got subdomains: ", subdomains_info)

    return list(i['domain'] for i in subdomains_info['result']['records'])


# Returns a dictionary containing the external domains where assets are loaded from
def get_asset_domains(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    asset_domains = {
        "javascripts": [],
        "stylesheets": [],
        "images": [],
        "iframes": [],
        "anchors": []
    }

    # Helper functions to validate tags
    def has_valid_stylesheet_domain(tag):
        return (tag.name == 'link' and 'stylesheet' in tag.get('rel') and tag.get('href') and
                tag.get('href').startswith('http'))

    def has_valid_script_domain(tag):
        return tag.name == 'script' and tag.get('src') and tag.get('src').startswith('http')

    def has_valid_image_domain(tag):
        return tag.name == 'img' and tag.get('src') and tag.get('src').startswith('http')

    def has_valid_iframe_domain(tag):
        return tag.name == 'iframe' and tag.get('src') and tag.get('src').startswith('http')

    def has_valid_anchor_domain(tag):
        return tag.name == 'a' and tag.get('href') and tag.get('href').startswith('http')

    def get_domain_from_tag(tag, attr):
        return urlparse(tag[attr]).netloc

    # Extracting stylesheets, scripts, images, iframes, and anchor tag references
    for tag in soup.find_all(['link', 'script', 'img', 'iframe', 'a']):
        if has_valid_stylesheet_domain(tag):
            if get_domain_from_tag(tag, 'href').startswith(urlparse(url).netloc):
                continue
            asset_domains['stylesheets'].append(get_domain_from_tag(tag, 'href'))

        elif has_valid_script_domain(tag):
            if get_domain_from_tag(tag, 'src').startswith(urlparse(url).netloc):
                continue
            asset_domains['javascripts'].append(get_domain_from_tag(tag, 'src'))

        elif has_valid_image_domain(tag):
            if get_domain_from_tag(tag, 'src').startswith(urlparse(url).netloc):
                continue
            asset_domains['images'].append(get_domain_from_tag(tag, 'src'))

        elif has_valid_iframe_domain(tag):
            if get_domain_from_tag(tag, 'src').startswith(urlparse(url).netloc):
                continue
            asset_domains['iframes'].append(get_domain_from_tag(tag, 'src'))

        elif has_valid_anchor_domain(tag):
            if get_domain_from_tag(tag, 'href').startswith(urlparse(url).netloc):
                continue
            asset_domains['anchors'].append(get_domain_from_tag(tag, 'href'))

    # Remove duplicates
    for key in asset_domains:
        asset_domains[key] = list(set(asset_domains[key]))

    return asset_domains


@app.route('/')
def analyze_website():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"})

    try:
        # Extract IP information
        domain_info = get_domain_info(url)

        # Extract subdomain information
        subdomains = get_subdomains(url)

        # Extracting asset domains
        asset_domains = get_asset_domains(url)

        # Prepare result
        result = {
            "info": domain_info,
            "subdomains": subdomains,
            "asset_domains": asset_domains
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})


@sock.route('/ws')
def handle_ws(ws):
    cached_url = None
    cached_info = None
    cached_subdomains = None
    cached_asset_domains = None

    while True:
        msg = ws.receive()
        print(msg)
        message = json.loads(msg)
        if 'url' in message:
            # 1st message
            url = message['url']
            if urlparse(url).scheme not in ['http', 'https']:
                cached_url = "https://" + url
            else:
                cached_url = url
            cached_info = None
            cached_subdomains = None
            cached_asset_domains = None
            msg = {"data": "session created for " + url}
            ws.send(json.dumps(msg))

        elif cached_url and 'operation' in message:
            # subsequent messages
            try:
                operation = message['operation']
                if operation == 'get_info':
                    if not cached_info:
                        cached_info = get_domain_info(cached_url)
                    ws.send(json.dumps({"data": cached_info}))

                elif operation == 'get_subdomains':
                    if not cached_subdomains:
                        cached_subdomains = get_subdomains(cached_url)
                    ws.send(json.dumps({"data": cached_subdomains}))

                elif operation == 'get_asset_domains':
                    if not cached_asset_domains:
                        cached_asset_domains = get_asset_domains(cached_url)
                    ws.send(json.dumps({"data": cached_asset_domains}))

                else:
                    ws.send(json.dumps({"error": "Invalid operation"}))

            except Exception as e:
                ws.send(json.dumps({"error": str(e)}))

        else:
            ws.send(json.dumps({"error": "Unknown command"}))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
