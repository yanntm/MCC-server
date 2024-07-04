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

## Setup

### Prerequisites

Ensure Docker is installed on your machine. You can download it from the [Docker website](https://www.docker.com/products/docker-desktop).

### Building the Docker Image

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
   docker run -d -p 1664:1664 mcc-server
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

## License and Acknowledgment

This project is licensed under the GPL-3.0 License. See the [LICENSE](LICENSE) file for details.

Packaging and development by Yann Thierry-Mieg, working at LIP6, Sorbonne Université, CNRS. 
