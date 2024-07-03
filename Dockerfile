# Use Ubuntu as base image
FROM ubuntu:rolling

# Set non-interactive mode for installing packages
ENV DEBIAN_FRONTEND=noninteractive

# Install basic necessary packages
RUN apt-get update && apt-get install -y \
    git \
    ca-certificates \
    python3 \
    python3-pip \
    unzip \
    openjdk-17-jdk \
    psmisc \
    wget \
    python3-flask \
    python3-flask-cors \
    && rm -rf /var/lib/apt/lists/*

# Clone the MCC-drivers repository
RUN mkdir -p /home/mcc/BenchKit
WORKDIR /home/mcc/BenchKit
RUN git clone https://github.com/yanntm/MCC-drivers.git .
RUN mkdir -p /home/mcc/BenchKit/itstools
WORKDIR /home/mcc/BenchKit/itstools
RUN git clone https://github.com/yanntm/ITS-Tools-MCC.git .
WORKDIR /home/mcc/BenchKit

# Download and setup the converter tool
RUN wget -O /home/mcc/BenchKit/fr.lip6.converter.jar https://github.com/lip6/ITSTools/raw/gh-pages/fr.lip6.converter.jar


# Install additional packages from install_packages.sh scripts
RUN bash ./install_packages.sh

# Run the main install script
RUN bash ./install.sh


# Copy the Flask server code to the Docker image
COPY . /app

# Set the working directory
WORKDIR /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the Flask server
CMD ["python3", "server.py"]
