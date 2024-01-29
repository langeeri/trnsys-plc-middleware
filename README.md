# Communication middleware built on top of Type 3157

This project provides middleware designed for use within Hardware-in-the-Loop testbeds in conjunction with TRNSYS simulations. It facilitates communication between TRNSYS and PLCs for both read-write and read-only operations. 

## Table of Contents

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Contents](#contents)
  - [main.py](#mainpy)
  - [middleware_config.py](#middleware_configpy)
  - [server_manager.py](#server_managerpy)
  - [server_config.py](#server_configpy)
- [Configuration](#configuration)
- [Usage](#usage)
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

## Contents
Inside the 'src' directory, you will find the following files:

### main.py
This module provides functionality to interface with Modbus servers as part of a TRNSYS simulation. 
It defines a `ModbusServer` class for handling connections, reading, and writing to Modbus servers. 
The module is designed to work with TRNSYS by providing custom functions for different stages of 
the simulation process such as initialization, time step processing, and simulation end.

The module also includes helper functions for initializing Modbus server connections based on 
configured settings and for handling various TRNSYS simulation stages like start time, iteration, 
end of time step, and last call of the simulation.

### middleware_config.py
This module defines several constants that are used throughout the main.py module for ModBus server 
implementation and its interaction with the TRNSYS simulation environment. These constants are crucial for 
the proper functioning of the data exchange process and logging mechanisms.

> [!IMPORTANT]
> You need to change the SIMULATION_MODEL constant to match your simulation model name! For example, if
> your TRNSYS simulation model is named MyModel.tpf, the constant should be SIMULATION_MODEL = 'MyModel'

### server_manager.py
This script contains definitions for managing Modbus server settings
and a GUI for easy manipulation of these configurations. It includes
functions for adding, deleting, and modifying server configurations.

You should run the GUI and use it to define your ModBus servers. 
The GUI will automatically update the server_config.py file, 
which is then read by main.py. Alternatively, you can manually 
modify the server_config.py configuration file to define your servers.

### server_config.py
This config file contains the `SERVER_CONFIGS` list, which consists of dictionaries. 
Each dictionary represents the configuration of a Modbus server, including details 
such as the host address, port number, and register information. 
Four ModBus servers are defined here as examples.


## Configuration
The configuration for Modbus servers should be specified inside server_configs.py in SERVER_CONFIGS list. 
This list includes dictionaries with details such as the host, port, registers, and input indexes for each server.

> [!CAUTION]
> Since this is Python, the indexing is zero-based.

The server is specified like this, where host is the IP adress of the server, port is self-explanatory, rw_registers are
read-write registers, input_indexes are indexes of the variables defined inside the Type 3157 that should be written 
to the specified registers. Read registers are the ones that should be read and send back to TRNSYS.

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

## Usage


## Contributing
Contributions are welcome! Follow the guidelines in CONTRIBUTING.md for details on how to submit your contribution to this project.

## License
This repository is licensed under the MIT License, allowing you to use and modify the code freely. Please review the license for more details.
