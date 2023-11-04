# Pull python image
FROM python:3.8-alpine

# Copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# Switch working directory in image
WORKDIR /app

# Install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# Copy app.py into the image
COPY app.py /app

# Configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

# Start the application
CMD ["app.py" ]
