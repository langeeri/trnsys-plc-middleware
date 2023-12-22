# -*- coding: utf-8 -*-

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

__author__ = "Erika Langerová, Michal Broum"
__copyright__ = "<2023> <Regulus>"
__credits__ = [" ", " "]

__license__ = "MIT (X11)"
__version__ = "1.2.0"
__maintainer__ = ["Erika Langerová"]
__email__ = ["erika.langerova@regulus.cz"]
__status__ = "Alfa"

__python__ = "3.10.5"
__TRNSYS__ = "18.04.0000"

# --------------------------------------------------------------------------

import logging
import time as osTime
from typing import Dict, List, Union, Optional
from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadBuilder, Endian
from server_config import SERVER_CONFIGS
from middleware_config import SIM_SLEEP, SIMULATION_MODEL, LOGGING_FILENAME


# --------------------------------------------------------------------------

class ModbusServer:
    """
    Represents a Modbus server with methods for connecting, reading, and writing data.

    Parameters
    ----------
    host : str
        The IP address or hostname of the Modbus server.
    port : int
        The port number on which the Modbus server is listening.
    rw_registers : List[int]
        List of Modbus registers for read-write operations.
    input_indexes : List[int]
        List of input indexes for the server.
    r_registers : List[int]
        List of Modbus registers for read-only operations.

    Attributes
    ----------
    host : str
        The IP address or hostname of the Modbus server.
    port : int
        The port number on which the Modbus server is listening.
    rw_registers : List[int]
        List of Modbus registers for read-write operations.
    input_indexes : List[int]
        List of input indexes for the server.
    r_registers : List[int]
        List of Modbus registers for read-only operations.
    client : ModbusTcpClient
        The Modbus TCP client used to communicate with the server.

    Methods
    -------
    connect()
        Establish a connection to the Modbus server.
    write_inputs(inputs)
        Write inputs to the Modbus server.
    read_outputs(TRNData)
        Read outputs from the Modbus server and update TRNData.
    close_connection()
        Close the connection to the Modbus server.

    """

    def __init__(self, host: str, port: int, rw_registers: Optional[List[int]], input_indexes: List[int], r_registers: Optional[List[int]]):
        self.host = host
        self.port = port
        self.rw_registers = rw_registers
        self.input_indexes = input_indexes
        self.r_registers = r_registers
        self.client = None

    def open_connection(self)-> None:
        """
        Establish a connection to the Modbus server.

        Raises
        ------
        Exception
            If an error occurs during the connection.

        """

        try:
            self.client = ModbusTcpClient(host=self.host, port=self.port)
        except Exception as e:
            logging.error(f"Error initializing Modbus client for {self.host}:{self.port}: {e}")
            raise

    def write_inputs(self, inputs: List[Union[int, float]]) -> List[Union[int, float]]:
        """
        Write inputs to the Modbus server.

        Parameters
        ----------
        inputs : List[Union[int, float]]
            List of input values to be written to the server.

        Returns
        -------
        List[Union[int, float]]
            The list of inputs that were written.

        Raises
        ------
        Exception
            If an error occurs during the write operation.

        """

        try:
            client = self.client
            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
            builder.reset()

            for index, value in enumerate(inputs):
                inputConverted = int(value * 10)
                builder.add_16bit_int(inputConverted)

            payload = builder.to_registers()

            for indexRW, addressRW in enumerate(self.rw_registers):
                result = client.write_registers(addressRW-1, payload[indexRW])  # starts from 0
                if result.isError():
                    logging.error(f"Error writing to PLC register for {self.host}:{self.port}: {result}")
                else:
                    logging.info(f"Successfully wrote {inputs[indexRW]} to PLC register {addressRW} for {self.host}:{self.port}")

            return inputs

        except Exception as e:
            logging.error(f"Error writing to PLC register for {self.host}:{self.port}: {e}")

    def read_outputs(self, TRNData: Dict[str, Dict[str, Union[int, float]]]) -> None:
        """
        Read outputs from the Modbus server and update TRNData.

        Parameters
        ----------
        TRNData : Dict[str, Dict[str, Union[int, float]]]
            A dictionary containing TRNSYS simulation model data.

        Raises
        ------
        Exception
            If an error occurs during the read operation.

        """

        arrayOfResponses = []
        
        try: 
            for addressR in self.r_registers:
                responseR = self.client.read_holding_registers(addressR-1)
                registerValue = responseR.getRegister(0)
                arrayOfResponses.append(registerValue)

            # Send response to TRNSYS.
            for indexR, addressR in enumerate(self.r_registers):
                TRNData[SIMULATION_MODEL]["outputs"][indexR] = arrayOfResponses[indexR]

        except Exception as e:
            logging.error(f"Error writing to TRNSYS from {self.host}:{self.port}: {e}")

    def close_connection(self) -> None:
        """
        Close the connection to the Modbus server.

        Raises
        ------
        Exception
            If an error occurs during the connection closure.

        """
        
        try:
            if self.client:
                self.client.close()
        except Exception as e:
            logging.error(f"Error closing Modbus connection for {self.host}:{self.port}: {e}")

def define_servers(server_configs: List[Dict[str, Union[str, int, List[int], int, List[int]]]]) -> List[ModbusServer]:
    """
    Initialize Modbus servers based on the provided configuration.

    Parameters
    ----------
    server_configs : List[Dict[str, Union[str, int, List[int], int, List[int]]]]
        List of dictionaries containing configuration information for Modbus servers.

    Returns
    -------
    List[ModbusServer]
        List of initialized ModbusServer instances.

    """

    servers = []
    for config in server_configs:
        server = ModbusServer(
            host=config['host'],
            port=config['port'],
            rw_registers=config['rw_registers'],
            input_indexes=config['input_indexes'],
            r_registers=config['r_registers']
        )
        servers.append(server)
    return servers



# --------------------------------------------------------------------------------
#                                   START
# --------------------------------------------------------------------------------
# ...

def Initialization(TRNData: Dict[str, Dict[str, List[Union[int, float]]]]) -> None:
    """
    Function called at TRNSYS initialization. 
    Used to initialize servers based on the provided configuration. 

    Parameters
    ----------
    TRNData : Dict[str, Dict[str, List[Union[int, float]]]]
        A nested dictionary containing simulation data.

    Raises
    ------
    Exception
        If an error occurs during initialization, an exception is raised with
        details about the error.

    Notes
    -----
    This function initializes global variable 'servers' by connecting to servers
    based on the provided server configurations in SERVER_CONFIGS.

    Examples
    --------
    >>> Initialization(TRNData)

    The above example initializes servers using the configuration provided in
    'TRNData'. 

    """

    global servers

    logging.basicConfig(filename=LOGGING_FILENAME, level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

    try:
        server_configs = SERVER_CONFIGS  
        servers = define_servers(server_configs)

        for server in servers:
            server.open_connection()

    except Exception as e:
        logging.error(f"Error during initialization: {e}")
        for server in servers:
            server.close_connection()


# --------------------------------------------------------------------------------

def StartTime(TRNData: Dict[str, Dict[str, List[Union[int, float]]]]) -> None:
    """
    Function called at TRNSYS starting time (not an actual time step, 
    initial values should be reported).

    Parameters
    ----------
    TRNData : Dict[str, Dict[str, List[Union[int, float]]]]
        A nested dictionary containing simulation data.

    Returns
    -------
    None
        This function does not return any value.

    """

    return

 
# --------------------------------------------------------------------------------

def Iteration(TRNData: Dict[str, Dict[str, List[Union[int, float]]]]) -> None:
    """
    Function called at each TRNSYS iteration within a time step.

    Parameters
    ----------
    TRNData : Dict[str, Dict[str, List[Union[int, float]]]]
        A nested dictionary containing simulation data.

    Returns
    -------
    None
        This function does not return any value.

    """
    
    return

# --------------------------------------------------------------------------------

def EndOfTimeStep(TRNData: Dict[str, Dict[str, List[Union[int, float]]]]) -> None:
    """
    Perform end-of-time-step actions on connected servers based on TRNData.

    Parameters
    ----------
    TRNData : Dict[str, Dict[str, List[Union[int, float]]]]
        A nested dictionary containing simulation data.

    Returns
    -------
    None
        This function does not return any value.

    Raises
    ------
    Exception
        If an error occurs during the end-of-time-step actions, an exception is raised
        with details about the error.

    Notes
    -----
    This function iterates over connected servers, writes inputs based on the provided
    TRNData, and reads outputs if applicable. It logs relevant information during the process.

    Examples
    --------
    >>> EndOfTimeStep(TRNData)

    The above example performs end-of-time-step actions on connected servers using the
    values provided in 'TRNData'.

    """
    
    try:
    
        for server in servers:
            TRNinputs = TRNData[SIMULATION_MODEL]["inputs"]
            server_inputs = []

            for index in server.input_indexes:
                if 0 < index < len(TRNinputs):
                    server_inputs.append(TRNinputs[index])
            server.write_inputs(server_inputs)

            if server.r_registers:
                server.read_outputs(TRNData)
        
        logging.info(f"server_inputs: {server_inputs}")

    except Exception as e:
        logging.error(f"Error during EndOfTimeStep: {e}")

    osTime.sleep(SIM_SLEEP)

# --------------------------------------------------------------------------------

def LastCallOfSimulation(TRNData: Dict[str, Dict[str, List[Union[int, float]]]]) -> None:
    """
    Function called at the end of the simulation (once).
    Outputs are meaningless at this call.

    This function closes the Modbus TCP clients connected to PLCs
    and shuts down the logging module.

    Parameters
    ----------
    TRNData : Dict[str, Dict[str, List[Union[int, float]]]]
        A nested dictionary containing simulation data.

    Returns
    -------
    None
        This function does not return any value.

    Raises
    ------
    Exception
        If an error occurs during the last call of the simulation, an exception is raised.
        The error is logged using the logging module.

    Examples
    --------
    >>> trn_data = {'SIMULATION_MODEL': {'outputs': [0, 0, 0]}}
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