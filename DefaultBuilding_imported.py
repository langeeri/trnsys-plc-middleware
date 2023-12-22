# -*- coding: utf-8 -*-

"""
Interface for data exchange between the TRNSYS 
simulation environment and Tecomat Foxtrot PLC.

"""

__author__ = "Erika Langerová, Michal Broum"
__copyright__ = "<2023> <Regulus>"
__credits__ = [" ", " "]

__license__ = "MIT (X11)"
__version__ = "1.1.0"
__maintainer__ = ["Erika Langerová"]
__email__ = ["erika.langerova@regulus.cz"]
__status__ = "Alfa"

__python__ = "3.10.5"
__TRNSYS__ = "18.04.0000"


# Copyright 2023 Regulus

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# --------------------------------------------------------------------------

# Import libraries.
import os
import logging
import datetime
import time as osTime
import numpy as np
from typing import Dict, List, Tuple, Union
from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadBuilder, Endian
from server_config import SERVER_CONFIGS



SIM_SLEEP = 1



# ------------------------------- TRNSYS -----------------------------------------

# Pass the name of the TRNSYS .deck file to the simulationModel variable.
simulationModel = os.path.splitext(os.path.basename(__file__))[0]

# Configure the logging module
logging.basicConfig(filename='DataExchange.log', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

# ------------------------------- TRNSYS -----------------------------------------

class ModbusServer:
    def __init__(self, host: str, port: int, rw_register_initial: int, rw_register_final: int, input_indexes: List[int], r_register_initial: int, r_register_final: int):
        self.host = host
        self.port = port
        self.rw_register_initial = rw_register_initial
        self.rw_register_final = rw_register_final
        self.input_indexes = input_indexes
        self.r_register_initial = r_register_initial
        self.r_register_final = r_register_final
        self.client = None

    def connect(self):
        try:
            self.client = ModbusTcpClient(host=self.host, port=self.port)
        except Exception as e:
            logging.error(f"Error initializing Modbus client for {self.host}:{self.port}: {e}")
            raise

    def write_inputs(self, inputs: List[Union[int, float]]):
        try:
            client = self.client
            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
            builder.reset()

            for index, value in enumerate(inputs):
                inputConverted = int(value * 10)
                builder.add_16bit_int(inputConverted)

            payload = builder.to_registers()

            for addressRW in range(self.rw_register_initial - 1, self.rw_register_final):
                result = client.write_registers(addressRW, payload[addressRW - (self.rw_register_initial - 1)])
                if result.isError():
                    logging.error(f"Error writing to PLC register for {self.host}:{self.port}: {result}")
                else:
                    logging.info(f"Successfully wrote {inputs[addressRW - (self.rw_register_initial - 1)]} to PLC register {addressRW} for {self.host}:{self.port}")

            return inputs

        except Exception as e:
            logging.error(f"Error writing to PLC register for {self.host}:{self.port}: {e}")

    def read_outputs(self, TRNData: Dict[str, Dict[str, Union[int, float]]]):
        arrayOfResponses = []
        
        try: 
            for addressR in range(self.r_register_initial - 1, self.r_register_final):
                responseR = self.client.read_holding_registers(addressR)
                registerValue = responseR.getRegister(0)
                arrayOfResponses.append(registerValue)

            # Send response to TRNSYS.
            for x in range(0, (self.r_register_final - self.r_register_initial) + 1):
                TRNData[simulationModel]["outputs"][x] = arrayOfResponses[x]
            
            logging.info(f"TRNData[simulationModel][outputs][x] {TRNData[simulationModel]['outputs'][x]}")

        except Exception as e:
            logging.error(f"Error writing to TRNSYS for {self.host}:{self.port}: {e}")

    def close_connection(self):
        try:
            if self.client:
                self.client.close()
        except Exception as e:
            logging.error(f"Error closing Modbus connection for {self.host}:{self.port}: {e}")

def initialize_servers(server_configs: List[Dict[str, Union[str, int, List[int], int, int]]]) -> List[ModbusServer]:
    servers = []
    for config in server_configs:
        server = ModbusServer(
            host=config['host'],
            port=config['port'],
            rw_register_initial=config['rw_register_initial'],
            rw_register_final=config['rw_register_final'],
            input_indexes=config['input_indexes'],
            r_register_initial=config['r_register_initial'],
            r_register_final=config['r_register_final']
        )
        servers.append(server)
    return servers



# --------------------------------------------------------------------------------
#                                   START
# --------------------------------------------------------------------------------
# ...

def Initialization(TRNData):
    """ 
    Function called at TRNSYS initialization. 
    Opens log files and the communication with the PLC.  
    
    Parameters
    ------------
    TRNData : nested_dict
        Data received from TRNSYS.

    Returns
    ------------
    None

    """
    global servers

    try:
        server_configs = SERVER_CONFIGS  # You can modify this line if necessary
        servers = initialize_servers(server_configs)

        for server in servers:
            server.connect()

    except Exception as e:
        logging.error(f"Error during initialization: {e}")
        for server in servers:
            server.close_connection()


# --------------------------------------------------------------------------------

def StartTime(TRNData):
    """
    Function called at TRNSYS starting time (not an actual time step, 
    initial values should be reported).
    Writes the contents of the nested TRNData dictionary to logFile.

    Parameters
    ------------
    TRNData : nested_dict
        Data received from TRNSYS.

    Returns
    ------------
    None

    """

    return

 
# --------------------------------------------------------------------------------

def Iteration(TRNData):
    """
    Function called at each TRNSYS iteration within a time step.

    Parameters
    ------------
    TRNData : nested_dict
        Data received from TRNSYS.

    Returns
    ------------
    None

    """
    
    return

# --------------------------------------------------------------------------------

def EndOfTimeStep(TRNData: Dict[str, Dict[str, List[Union[int, float]]]]) -> None:
    """
    Function called at the end of each time step after iteration and before moving 
    on to next time step.

    Reads input data from TRNSYS, organizes it into specific categories,
    and writes the data to the corresponding Modbus registers on PLCs.
    It also reads data from specific Modbus registers on a PLC and updates TRNSYS data.
    A delay is introduced using `osTime.sleep` to slow down the simulation time.

    Parameters
    ----------
    TRNData : dict
        A nested dictionary containing TRNSYS simulation data.

    Returns
    -------
    None

    Raises
    ------
    Exception
        If an error occurs during the end of the time step, an exception is raised.
        The error is logged using the logging module.

    Examples
    --------
    >>> trn_data = {'simulationModel': {'inputs': [0, 1, 2, 3, 4, 5, 6, 7], 'outputs': [0, 0, 0]}}
    >>> EndOfTimeStep(trn_data)
    >>> # Perform actions at the end of each time step in the TRNSYS simulation

    """
    
    try:
    
        for server in servers:
            TRNinputs = TRNData[simulationModel]["inputs"]
            logging.info(f"TRNinputs: {TRNinputs}")
            server_inputs = []

            for index in server.input_indexes:
                if 0 < index < len(TRNinputs):
                    server_inputs.append(TRNinputs[index])

            server.write_inputs(server_inputs)

            if server.r_register_initial is not None or server.r_register_final is not None:
                server.read_outputs(TRNData)
        
        logging.info(f"server_inputs: {server_inputs}")


    except Exception as e:
        logging.error(f"Error during EndOfTimeStep: {e}")

    osTime.sleep(SIM_SLEEP)

# --------------------------------------------------------------------------------

def LastCallOfSimulation(TRNData: Dict[str, Dict[str, List[Union[int, float]]]])-> None:
    """
    Function called at the end of the simulation (once).
    Outputs are meaningless at this call.

    This function closes the Modbus TCP clients connected to PLCs
    and shuts down the logging module.

    Parameters
    ----------
    TRNData : dict
        A nested dictionary containing TRNSYS simulation data.

    Returns
    -------
    None

    Raises
    ------
    Exception
        If an error occurs during the last call of the simulation, an exception is raised.
        The error is logged using the logging module.

    Examples
    --------
    >>> trn_data = {'simulationModel': {'outputs': [0, 0, 0]}}
    >>> LastCallOfSimulation(trn_data)
    >>> # Perform actions at the end of the entire TRNSYS simulation

    """

    try:
        for server in servers:
            server.close_connection()

        logging.shutdown()

    except Exception as e:
        logging.error(f"Error during the last call of simulation: {e}")
        raise

    return