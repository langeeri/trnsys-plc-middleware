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

The middleware serves a dual purpose: firstly, it enables bidirectional communication between the PLC and simulation software, and secondly, it synchronizes the time steps of the simulation and the PLCs.

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
Inside the `src` directory, you will find the following files:

### main.py
This module provides functionality to interface with Modbus servers as part of a TRNSYS simulation. 
It defines a `ModbusServer` class for handling connections, reading, and writing to Modbus servers. 
The module is designed to work with TRNSYS by providing custom functions for different stages of 
the simulation process such as initialization, time step processing, and simulation end.

The module also includes helper functions for initializing Modbus server connections based on 
configured settings and for handling various TRNSYS simulation stages like start time, iteration, 
end of time step, and last call of the simulation.

### middleware_config.py
This module defines several constants that are used throughout the `main.py` module for ModBus server 
implementation and its interaction with the TRNSYS simulation environment. These constants are crucial for 
the proper functioning of the data exchange process and logging mechanisms.

> [!IMPORTANT]
> You need to change the `SIMULATION_MODEL` constant to match your simulation model name! For example, if
> your TRNSYS simulation model is named `MyModel.tpf`, the constant should be `SIMULATION_MODEL = 'MyModel'`

### server_manager.py
This script contains definitions for managing Modbus server settings
and a GUI for easy manipulation of these configurations. It includes
functions for adding, deleting, and modifying server configurations.

You should run the GUI and use it to define your ModBus servers. 
The GUI will automatically update the `server_config.py` file, 
which is then read by `main.py`. Alternatively, you can manually 
modify the `server_config.py` configuration file to define your servers.

### server_config.py
This config file contains the `SERVER_CONFIGS` list, which consists of dictionaries. 
Each dictionary represents the configuration of a Modbus server, including details 
such as the host address, port number, and register information. 
Four ModBus servers are defined here as examples.

## Configuration

> [!CAUTION]
> Since this is Python, the indexing is zero-based.


The configuration for Modbus servers should be specified inside `server_configs.py` in SERVER_CONFIGS list. 
This list includes dictionaries with details such as the host, port, registers, and input indexes for each server.

The server is specified with the following parameters: 
- **host**: The IP address of the server.
- **port**: The port number.
- **rw_registers**: The read-write registers.
- **input_indexes**: Indexes of the variables defined inside Type 3157, which should be written to the specified registers.
- **r_registers**: Registers that should be read and the data sent back to TRNSYS.

```python
SERVER_CONFIGS = [
    {
        'host': '127.0.0.1',
        'port': 502,
        'rw_registers': [1, 11, 12],
        'input_indexes': [5, 2, 3],
        'r_registers': [4, 5],
    },
  # If you dont need any read registers, keep the array blank like this:
    {
        'host': '127.0.0.1',
        'port': 502,
        'rw_registers': [1, 11, 12],
        'input_indexes': [5, 2, 3],
        'r_registers': [],
    },
    # Add additional servers as needed
]
```

> [!NOTE]
> Regarding  **r_registers**, the current implementation of the middleware is designed to read data from multiple registers in a single PLC.
> In scenarios where there are multiple PLCs involved, and data from all these PLCs needs to be sent back to TRNSYS,
> additional modifications to the `main.py` file are necessary. Regarding **rw_registers**, reading and writing to/from multiple registers at multiple PLCs is
> supported by the current implementation of the middleware. 

## Usage

> [!CAUTION]
> It is absolutelly necessary to keep all python files in the same directory and on the same level as your TRNSYS model !

Example directory structure:
 `src/`
  - `.gitignore` 
  - `main.py` - *Main Python script*
  - `main.tpf` - *Your simulation model*
  - `middleware_config.py` - *Configuration for middleware*
  - `server_config.py` - *Configuration for the ModBus servers*
  - `server_manager.py` - *GUI for managing ModBus servers configurations*

Follow these steps:
- Inside your TRNSYS model, open the Type 3157 card.
- Inside the `Special Cards` tab, set the `Main Python Script` variable to `main.py` 
- Inside the `middleware_config.py` modify the `SIMULATION_MODEL` constant to match your simulation model name, for example, if your
  TRNSYS simulation model is named `MyModel.tpf`, the constant should be `SIMULATION_MODEL = 'MyModel'`
- Inside the `middleware_config.py` modify the `SIM_SLEEP` variable, if you need different data exchange update time step than the default one (60 seconds).
- Define your ModBus servers and registers either by running the GUI provided by the `server_manager.py` or by manually updating the `server_config.py` config file.
- Run the simulation

The middleware is set up in such a way that ModBus clients are opened in the initialization phase of the simulation, meaning at the first call of Python from TRNSYS. At this stage, a connection to the ModBus servers, i.e., all the used PLCs, is established, but data exchange does not yet occur. It makes no sense to start data exchange before convergence is achieved in the computation of the current simulation step. The communication at this step occurs in a way that the Type 3157 component exchanges data with the communication middleware through a nested hashmap (a hashmap is a data type, it's an unordered set of key-value pairs, in Python it's often referred to as a dictionary), where the inputs from TRNSYS to Type 3157 in the current time step are sent as hashmap variables to the middleware. The data from the hashmap are sorted in the middleware and sent for writing to the registers of the respective PLCs. The data exchange in the opposite direction, i.e., from the PLCs through the middleware to TRNSYS, is resolved in a similar manner.

## Contributing
Contributions are welcome! Follow the guidelines in CONTRIBUTING.md for details on how to submit your contribution to this project.

## License
This repository is licensed under the MIT License, allowing you to use and modify the code freely. Please review the license for more details.
