
"""server_config.py

This config file contains the `SERVER_CONFIGS` list, which consists of dictionaries. 
Each dictionary represents the configuration of a Modbus server, including details 
such as the host address, port number, and register information. 
Four ModBus servers are defined here as examples.

The indexing starts at zero.

"""

SERVER_CONFIGS = [
    {
        "host": "10.208.8.11",
        "port": 502,
        "rw_registers": [1],
        "input_indexes": [5],
        "r_registers": [],
    },
    {
        "host": "10.202.240.12",
        "port": 502,
        "rw_registers": [1,2],
        "input_indexes": [0,1],
        "r_registers": [4,5],
    },
    {
        "host": "10.202.240.13",
        "port": 502,
        "rw_registers": [1,2],
        "input_indexes": [2,3],
        "r_registers": [],
    },
    {
        "host": "10.208.227.188",
        "port": 502,
        "rw_registers": [1,11,12],
        "input_indexes": [4,7,8],
        "r_registers": [],
    },
]
