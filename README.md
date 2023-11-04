# squarex-flask

SquareX Flask Assignment

Run with `docker compose up -d`

Server will be available at `http://localhost:5000`

## HTTP API

Usage: `http://localhost:5000/?url=<url>`, where `<url>` is a valid url starting with `http://` or `https://`

Example: `http://localhost:5000/?url=https://stackoverflow.com`

Example Response JSON:

```json
{
  "asset_domains": {
    "anchors": [
      "gamedev.stackexchange.com",
      "unix.stackexchange.com",
      "serverfault.com",
      "meta.stackoverflow.com",
      "apple.stackexchange.com",
      "www.instagram.com",
      "api.stackexchange.com",
      "dba.stackexchange.com",
      "askubuntu.com",
      "linkedin.com",
      "stackoverflow.blog",
      "networkengineering.stackexchange.com",
      "www.facebook.com",
      "softwareengineering.stackexchange.com",
      "salesforce.stackexchange.com",
      "stackexchange.com",
      "data.stackexchange.com",
      "chat.stackoverflow.com",
      "superuser.com",
      "ai.stackexchange.com",
      "quantumcomputing.stackexchange.com",
      "stackoverflowteams.com",
      "stackoverflow.co",
      "twitter.com",
      "try.stackoverflow.co"
    ],
    "iframes": [],
    "images": [
      "cdn.sstatic.net"
    ],
    "javascripts": [
      "ajax.googleapis.com",
      "cdn.sstatic.net",
      "www.googletagmanager.com"
    ],
    "stylesheets": [
      "cdn.sstatic.net"
    ]
  },
  "info": {
    "asn": "AS13335",
    "ip": "172.64.155.249",
    "isp": "Cloudflare, Inc.",
    "location": "US",
    "organization": "Cloudflare, Inc."
  },
  "subdomains": [
    "ru.meta.stackoverflow.com",
    "ny-gh.stackoverflow.com",
    "dev.bonfire.stackoverflow.com",
    "ru-www.meta.stackoverflow.com",
    "devdays.stackoverflow.com",
    "br.stackoverflow.com",
    "sso.stackoverflow.com",
    "api.meta.stackoverflow.com",
    "ja.stackoverflow.com",
    "meta.stackoverflow.com",
    "facebook.stackoverflow.com",
    "calendar.stackoverflow.com",
    "business.stackoverflow.com",
    "groups.stackoverflow.com",
    "blog.stackoverflow.com",
    "dev.blog.stackoverflow.com",
    "mail.stackoverflow.com",
    "dev.channels.stackoverflow.com",
    "hello.stackoverflow.com",
    "dev.talent.stackoverflow.com",
    "meta.br.stackoverflow.com",
    "clc.dev.stackoverflow.com",
    "www.careers.stackoverflow.com",
    "meta.es.stackoverflow.com",
    "gh.stackoverflow.com",
    "enterpriseenrollment.stackoverflow.com",
    "dev.careers.stackoverflow.com",
    "ads.stackoverflow.com",
    "careers.stackoverflow.com",
    "talent.stackoverflow.com",
    "dev.meta.stackoverflow.com",
    "meta.jp.stackoverflow.com",
    "rads.stackoverflow.com",
    "meta.ru.stackoverflow.com",
    "chat.meta.stackoverflow.com",
    "insights.stackoverflow.com",
    "pt.meta.stackoverflow.com",
    "dev.insights.stackoverflow.com",
    "meta.ja.stackoverflow.com",
    "dev-email.stackoverflow.com",
    "clc.stackoverflow.com",
    "dev.contests.stackoverflow.com",
    "ru.stackoverflow.com",
    "contests.stackoverflow.com",
    "dev.stackoverflow.com",
    "ja.meta.stackoverflow.com",
    "pt.stackoverflow.com",
    "dev-bonfire.stackoverflow.com",
    "co-gh.stackoverflow.com",
    "api.stackoverflow.com",
    "jp.stackoverflow.com",
    "meta.pt.stackoverflow.com",
    "es.stackoverflow.com",
    "email.stackoverflow.com",
    "dev.email.stackoverflow.com",
    "meta.dev.stackoverflow.com",
    "blog.careers.stackoverflow.com",
    "www.stackoverflow.com",
    "chat.stackoverflow.com",
    "es.meta.stackoverflow.com"
  ]
}
```

## Websocket API

1. Connect to `ws://localhost:5000/ws`.
2. Send a JSON message with the following format: `{"url": "<url>"}`, where `<url>` is a valid url starting
   with `http://` or `https://`
3. Send an operation request. The operation request is a JSON message with the following
   format: `{"operation": "<operation>"}`, where `<operation>` is one of the
   following: `get_info`, `get_subdomains`, `get_asset_domains`.

Example:

Request 1:

```json
{
  "url": "https://stackoverflow.com"
}
```

Response 1:

```json
{
  "data": "session created for https://stackoverflow.com"
}
```

Request 2:

```json
{
  "operation": "get_info"
}
```

Response 2:

```json
{
  "data": {
    "ip": "172.64.155.249",
    "isp": "Cloudflare, Inc.",
    "organization": "Cloudflare, Inc.",
    "asn": "AS13335",
    "location": "US"
  }
}
```

Request 3:

```json
{
  "operation": "get_subdomains"
}
```

Response 3:

```json
{
  "data": [
    "ru.meta.stackoverflow.com",
    "ny-gh.stackoverflow.com",
    "dev.bonfire.stackoverflow.com",
    "ru-www.meta.stackoverflow.com",
    "devdays.stackoverflow.com",
    "br.stackoverflow.com",
    "sso.stackoverflow.com",
    "api.meta.stackoverflow.com",
    "ja.stackoverflow.com",
    "meta.stackoverflow.com",
    "facebook.stackoverflow.com",
    "calendar.stackoverflow.com",
    "business.stackoverflow.com",
    "groups.stackoverflow.com",
    "blog.stackoverflow.com",
    "dev.blog.stackoverflow.com",
    "mail.stackoverflow.com",
    "hello.stackoverflow.com",
    "dev.channels.stackoverflow.com",
    "dev.talent.stackoverflow.com",
    "meta.br.stackoverflow.com",
    "clc.dev.stackoverflow.com",
    "www.careers.stackoverflow.com",
    "meta.es.stackoverflow.com",
    "gh.stackoverflow.com",
    "enterpriseenrollment.stackoverflow.com",
    "dev.careers.stackoverflow.com",
    "ads.stackoverflow.com",
    "careers.stackoverflow.com",
    "talent.stackoverflow.com",
    "dev.meta.stackoverflow.com",
    "meta.jp.stackoverflow.com",
    "rads.stackoverflow.com",
    "meta.ru.stackoverflow.com",
    "chat.meta.stackoverflow.com",
    "dev-email.stackoverflow.com",
    "clc.stackoverflow.com",
    "dev.contests.stackoverflow.com",
    "contests.stackoverflow.com",
    "ru.stackoverflow.com",
    "dev.stackoverflow.com",
    "insights.stackoverflow.com",
    "pt.meta.stackoverflow.com",
    "dev.insights.stackoverflow.com",
    "meta.ja.stackoverflow.com",
    "ja.meta.stackoverflow.com",
    "pt.stackoverflow.com",
    "dev-bonfire.stackoverflow.com",
    "co-gh.stackoverflow.com",
    "api.stackoverflow.com",
    "jp.stackoverflow.com",
    "meta.pt.stackoverflow.com",
    "es.stackoverflow.com",
    "email.stackoverflow.com",
    "dev.email.stackoverflow.com",
    "meta.dev.stackoverflow.com",
    "blog.careers.stackoverflow.com",
    "es.meta.stackoverflow.com",
    "www.stackoverflow.com",
    "chat.stackoverflow.com"
  ]
}
```

Request 4:

```json
{
  "operation": "get_asset_domains"
}
```

Response 4:

```json
{
  "data": {
    "javascripts": [
      "www.googletagmanager.com",
      "cdn.sstatic.net",
      "ajax.googleapis.com"
    ],
    "stylesheets": [
      "cdn.sstatic.net"
    ],
    "images": [
      "cdn.sstatic.net"
    ],
    "iframes": [],
    "anchors": [
      "superuser.com",
      "dba.stackexchange.com",
      "quantumcomputing.stackexchange.com",
      "stackoverflow.blog",
      "linkedin.com",
      "networkengineering.stackexchange.com",
      "unix.stackexchange.com",
      "askubuntu.com",
      "data.stackexchange.com",
      "apple.stackexchange.com",
      "twitter.com",
      "www.instagram.com",
      "serverfault.com",
      "meta.stackoverflow.com",
      "stackexchange.com",
      "salesforce.stackexchange.com",
      "softwareengineering.stackexchange.com",
      "stackoverflowteams.com",
      "stackoverflow.co",
      "api.stackexchange.com",
      "ai.stackexchange.com",
      "chat.stackoverflow.com",
      "try.stackoverflow.co",
      "gamedev.stackexchange.com",
      "www.facebook.com"
    ]
  }
}
```
