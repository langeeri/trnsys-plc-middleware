# Communication middleware built on top of Type 3157

This project provides middleware designed for use within Hardware-in-the-Loop testbeds in conjunction with TRNSYS simulations. It facilitates communication between TRNSYS and PLCs for both read-write and read-only operations. 

## Table of Contents

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Initialization](#initialization)
  - [Start Time](#start-time)
  - [Iteration](#iteration)
  - [End of Time Step](#end-of-time-step)
  - [Last Call of Simulation](#last-call-of-simulation)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project provides middleware designed for use within Hardware-in-the-Loop testbeds in conjunction with TRNSYS simulations. It allows for seamless communication between TRNSYS simulations and Modbus servers, enabling the exchange of data for read-write and read-only operations. The middleware functions as a Modbus client, while the PLCs functions as Modbus servers.


## Requirements

- TRNSYS 18.04.0000 and higher
- Type 3157
- Python 3.10.5
- Required Python packages (specified in `requirements.txt`)
- PLCs or other Modbus-compatible servers

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/langeeri/trnsys-plc-middleware.git
    cd trnsys-plc-middleware
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Define inputs and outputs inside the Type 1375. For more information check Type´s 1375 documentation.
Configure ModBus servers inside your PLCS
Start the server_manager.exe
Define all your servers and registers


### Initialization

To initialize Modbus servers, use the provided `Initialization` function. This function establishes connections to Modbus servers based on the provided configuration in `SERVER_CONFIGS`.

```python
from modbus_server import Initialization

TRNData = {
    'SIMULATION_MODEL': {'inputs': [0, 0, 0]}
}

try:
    Initialization(TRNData)
except Exception as e:
    print(f"Error during initialization: {e}")
```

### Configuration
The configuration for Modbus servers is specified in SERVER_CONFIGS. This list includes dictionaries with details such as the host, port, registers, and input indexes for each server.

```python
SERVER_CONFIGS = [
    {
        'host': '127.0.0.1',
        'port': 502,
        'rw_registers': [1, 11, 12],
        'input_indexes': [5, 2, 3],
        'r_registers': [4, 5],
    },
    # Add additional servers as needed
]
```

