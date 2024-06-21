# Use Ubuntu as base image
FROM ubuntu:20.04

# Set non-interactive mode for installing packages
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Flask
RUN pip3 install flask

# Copy the current directory contents into the container
COPY . /app

# Set the working directory
WORKDIR /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the Flask server
CMD ["python3", "server.py"]
