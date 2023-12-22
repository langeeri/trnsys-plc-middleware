# Communication middleware between TRNSYS and multiple PLCs

This project provides a Modbus server interface designed for use with TRNSYS simulations. It allows communication between TRNSYS and Modbus servers for read-write and read-only operations.

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

This project provides a Python-based implementation of a Modbus server interface to be used in conjunction with the TRNSYS simulation environment. It allows for seamless communication between TRNSYS simulations and Modbus servers, enabling the exchange of data for read-write and read-only operations.

## Requirements

- Python 3.x
- Required Python packages (specified in `requirements.txt`)
- Modbus-compatible servers

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/modbus-trnsys-interface.git
    cd modbus-trnsys-interface
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

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
