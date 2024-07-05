# MCC-server

A Dockerized server providing Model-Checking Contest (MCC) compliant tools via a web interface.

## Overview

MCC-server is a Dockerized server that exposes tools from the [MCC-drivers](https://github.com/yanntm/MCC-drivers) project. It provides an interface for running various model-checking tools and retrieving results.

MCC-server is essentially a wrapper for the [MCC-drivers](https://github.com/yanntm/MCC-drivers) project. MCC-drivers adapts various tools to MCC formats and provides the core functionalities that MCC-server exposes.

[PetriVizu](https://github.com/yanntm/PetriVizu) is a demonstrator for the capabilities of MCC compatible tools with a user-friendly front-end for visualizing and analyzing Petri nets. It uses this dockers container if provided to provide an intuitive interface and advanced visualization features to MCC compliant tools.

### Logic File Syntax

Please visit the [property syntax page](https://github.com/yanntm/PetriVizu/blob/master/public/syntax.md) on PetriVizu repository for more information on the human usable syntax proposed to interact with the MCC tools to express bounds, reachability, LTL and CTL properties.

### Supported Tools

MCC-server supports most tools that compete or have competed in the MCC. Refer to the [MCC-drivers repository](https://github.com/yanntm/MCC-drivers) for more details on the tools and their configurations.

|          | COL supported   | LTL   | CTL   | Reachability   | StateSpace   | UpperBounds   | Liveness   | OneSafe   | StableMarking   |
|:---------|:----------------|:------|:------|:---------------|:-------------|:--------------|:-----------|:----------|:----------------|
| itstools | ✓               | ✓     | ✓     | ✓              | ✓            | ✓             | ✓          | ✓         | ✓               |
| greatspn | ✓               | ✓     | ✓     | ✓              | ✓            | ✓             | ✓          | ✓         | ✓               |
| lola     | ✓               | ✓     | ✓     | ✓              |              | ✓             | ✓          | ✓         | ✓               |
| tapaal   | ✓               | ✓     | ✓     | ✓              |              | ✓             | ✓          | ✓         | ✓               |
| smart    |                 |       |       | ✓              | ✓            | ✓             | ✓          | ✓         | ✓               |
| ltsmin   |                 | ✓     | ✓     | ✓              | ✓            | ✓             |            |           |                 |
| marcie   | ✓               |       | ✓     | ✓              | ✓            | ✓             |            |           |                 |
| smpt     | ✓               |       |       | ✓              |              |               |            |           |                 |
| pnmc     |                 |       |       |                | ✓            |               |            |           |                 |


## Setup

### Prerequisites

Ensure Docker is installed on your machine. You can download it from the [Docker website](https://www.docker.com/products/docker-desktop).

### Pulling the Docker Image

1. Pull the Docker image from DockerHub:
   ```bash
   docker pull yanntm/mcc-server:latest
   ```
   
2. Run the Docker container:
   ```bash
   docker run -d -p 1664:1664 yanntm/mcc-server:latest
   ```
   
3. Query the MCC-server (e.g. curl), or open PetriVizu
   https://yanntm.github.io/PetriVizu
   to interact from Analysis mode.  

### Building the Docker Image (Optional)

If you prefer to build the Docker image locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yanntm/MCC-server.git
   cd MCC-server
   ```

2. Build the Docker image:
   ```bash
   docker build -t mcc-server .
   ```

### Running the Docker Container

1. Run the Docker container:
   ```bash
   docker run -d -p 1664:1664 yanntm/mcc-server:latest
   ```

## Usage

The server processes PNML models and returns the results from the specified tool.

### Example Request

To run a tool on a PNML model, use the following `curl` command from the `samples/` folder:
```bash
curl -F "model.pnml=@flot.pnml" -F "model.logic=@flot_prop.logic" -F "timeout=100" http://localhost:1664/mcc/PT/LTLCardinality/itstools
```

### Endpoints

- **`POST /mcc/<col_flag>/<examination>/<tool>`**: Executes the specified tool with the provided PNML model.
  - `col_flag`: Either `COL` for colored Petri nets or `PT` for Petri nets.
  - `examination`: The type of examination to perform. Some require a property file (`.logic`), and some do not.
    - **Examinations without .logic file**: `StateSpace`, `OneSafe`, `StableMarking`, `QuasiLiveness`, `Liveness`, `ReachabilityDeadlock`
    - **Examinations with .logic file**: `UpperBounds`, `ReachabilityFireability`, `ReachabilityCardinality`, `CTLFireability`, `CTLCardinality`, `LTLFireability`, `LTLCardinality`
  - `tool`: The tool to use (e.g., `itstools`, `ltsmin`).

  #### Example
  ```bash
  curl -F "model.pnml=@/path/to/model.pnml" \
       -F "model.logic=@/path/to/model.logic" \
       -F "timeout=300" \
       http://localhost:1664/mcc/PT/ReachabilityCardinality/itstools
  ```

## Querying Available Tools and Examinations

The MCC-server provides an endpoint to query the list of supported tools and their corresponding examinations.

### Endpoint

- **`GET /tools/descriptions`**: Retrieves a list of all available tools and the examinations they support.

### Example Request

To get the list of available tools and examinations, use the following `curl` command:

```bash
curl http://localhost:1664/tools/descriptions
```

This command will return a JSON object containing details about each tool and the examinations it supports.

You can also run the "showTools.py" script in this repository to build a readable list of tools and capacity.

## License and Acknowledgment

This project is licensed under the GPL-3.0 License. See the [LICENSE](LICENSE) file for details.

Packaging and development by Yann Thierry-Mieg, working at LIP6, Sorbonne Université, CNRS. 
