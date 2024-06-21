# MCC-server

A small server to offer MCC (Model-Checking Contest) compliant tools to the web.

## Setup

1. Build the Docker image:
    ```sh
    docker build -t mcc-server .
    ```

2. Run the Docker container:
    ```sh
    docker run -d -p 5000:5000 mcc-server
    ```

## Usage

The server accepts a PNML model and returns the result of the mock tool.
