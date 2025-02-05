# Use the official lightweight Python image
FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Set the working directory to /app
ENV APP_HOME /app
WORKDIR $APP_HOME

# Install necessary system libraries
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy local code to the container image
COPY . ./ 

# Install production dependencies
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Pre-download the ResNet101 model so it's cached in the image
RUN python -c "import torchvision.models as models; models.resnet101(pretrained=True)"

# Run the web service on container startup using gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
