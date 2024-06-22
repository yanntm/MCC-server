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

The server accepts a PNML model and returns the result of the specified tool. 

### Endpoints
- `/run`: Runs the specified tool with the provided PNML model.
- `/tools/list`: Lists available tools.
- `/tools/<tool>/examinations`: Lists available examinations for a specific tool.
- `/tools/descriptions`: Provides detailed descriptions of tools and their examinations.

## Integration with PetriVizu

This server can be used with the [PetriVizu](https://github.com/yanntm/PetriVizu) tool for visualizing and analyzing Petri nets.

For more details, visit the [PetriVizu repository](https://github.com/yanntm/PetriVizu).
