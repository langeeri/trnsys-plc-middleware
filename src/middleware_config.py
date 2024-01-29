
"""middleware_config.py

Configuration settings for the main.py module.

This module defines several constants that are used throughout the Modbus server implementation
and its interaction with the TRNSYS simulation environment. These constants are crucial for 
the proper functioning of the data exchange process and logging mechanisms.

Constants
---------
SIM_SLEEP : int
    The sleep duration in seconds between successive end-of-time-step actions during the simulation.
    This is used to prevent overloading the system with rapid consecutive requests.

LOGGING_FILENAME : str
    The filename for the log file where all log messages related to the data exchange process are stored.
    This log file is useful for debugging and monitoring the flow of data between the TRNSYS simulation
    and the Modbus servers.

SIMULATION_MODEL : str
    The identifier for the simulation model. The name of the .tpf file with the simulation model in-use
    must be provided.

Notes
-----
- These constants are used in the main.py module.
- Changing these values can significantly impact the performance and behavior of the data exchange
  process. Ensure that any modifications are well-tested and compatible with the overall system requirements.

"""
SIM_SLEEP = 60
LOGGING_FILENAME = 'DataExchange.log'
SIMULATION_MODEL = 'main'


    