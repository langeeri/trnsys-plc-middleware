
# -*- coding: utf-8 -*-

"""
Middleware for data exchange between the TRNSYS 
simulation environment and Tecomat Foxtrot PLC.

"""

__author__ = "Erika Langerová, Michal Broum"
__copyright__ = "<2023> <Regulus>"
__credits__ = [" ", " "]

__license__ = "MIT (X11)"
__version__ = "1.2.0"
__maintainer__ = ["Erika Langerová"]
__email__ = ["langerova@regulus.cz"]
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

import os
import logging
import time as osTime
from typing import Dict, List, Tuple, Union
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadBuilder, Endian

# ------------------------------- Configs ------------------------------------

# Configure the logging module
logging.basicConfig(filename='DataExchange.log', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

# Pass the name of the TRNSYS .deck file to the simulationModel variable.
simulationModel = os.path.splitext(os.path.basename(__file__))[0]

global_event_loop = asyncio.new_event_loop()
asyncio.set_event_loop(global_event_loop)
# --------------------------- Constants --------------------------------------

SIM_SLEEP = 1

SERVER_PORT_1 = 502
SERVER_PORT_2=503

LAB_SERVER_IP = '127.0.0.1'
HOT_DOCK_SERVER_IP = '127.0.0.1'


LAB_RW_REGISTER_INITIAL = 1
LAB_RW_REGISTER_FINAL = 1

HOT_DOCK_RW_REGISTER_INITIAL = 1
HOT_DOCK_RW_REGISTER_FINAL = 1


# ---------------------------------------------------------------------------------

def init_modbus_client(host: str, port: int) -> ModbusTcpClient:
    """
    Initialize a Modbus TCP client.

    Creates and returns a ModbusTcpClient instance with the specified
    host and port for communication with a Modbus TCP server.

    Parameters
    ----------
    host : str
        The IP address or hostname of the Modbus TCP server.
    port : int
        The port number on which the Modbus TCP server is listening.

    Returns
    -------
    pymodbus.client.ModbusTcpClient
        An instance of the ModbusTcpClient class for communication with the Modbus TCP server.

    Raises
    ------
    Exception
        If an error occurs during the initialization of the Modbus client, an exception is raised.
        The error is logged using the logging module.

    Examples
    --------
    >>> client = init_modbus_client('192.168.1.1', 502)
    >>> # Use the 'client' instance for Modbus communication

    """

    try:
        client = ModbusTcpClient(host=host, port=port)
        return client
    except Exception as e:
        logging.error(f"Error initializing Modbus client: {e}")
        raise

# --------------------------------------------------------------------------------
    
async def async_write_to_plc(client: ModbusTcpClient, inputs: List[Union[int, float]], register_initial: int, register_final: int) -> None:
    """
    Write data to Modbus registers on a PLC.

    Constructs a Modbus payload from the given inputs and writes it to the
    specified range of Modbus registers on a PLC.

    Parameters
    ----------
    client : pymodbus.client.ModbusTcpClient
        The Modbus TCP client instance connected to the PLC.
    inputs : list
        A list of input values to be written to the PLC registers.
    register_initial : int
        The starting register address (1-based) to write data to.
    register_final : int
        The ending register address (1-based) to write data to.

    Raises
    ------
    Exception
        If an error occurs during the writing process, an exception is raised.
        The error is logged using the logging module.

    Examples
    --------
    >>> client = ModbusTcpClient('192.168.1.1', 502)
    >>> inputs = [0.5, 1.2, 3.0]
    >>> write_to_plc(client, inputs, 1, 3)
    >>> # Data from 'inputs' is written to registers 1, 2, and 3 on the PLC

    """

    try:
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.reset()

        for index, value in enumerate(inputs):
            inputConverted = int(value * 10)
            builder.add_16bit_int(inputConverted)
        
        payload = builder.to_registers()

        for addressRW in range(register_initial - 1, register_final):
            result = client.write_registers(addressRW, payload[addressRW])
            if result.isError():
                logging.error(f"Error writing to PLC register: {result}")
            else:
                logging.info(f"Successfully wrote {value} to PLC register {addressRW}")

    except Exception as e:
        logging.error(f"Error writing to PLC register: {e}")

# --------------------------------------------------------------------------------
        
def read_from_plc(client: ModbusTcpClient, register_initial: int, register_final: int, TRNData: Dict[str, Dict[str, Union[int, float]]]) -> None:
    """
    Read data from Modbus registers on a PLC and update TRNSYS data.

    Reads data from the specified range of Modbus registers on a PLC
    and updates the TRNSYS data dictionary with the received values.

    Parameters
    ----------
    client : pymodbus.client.ModbusTcpClient
        The Modbus TCP client instance connected to the PLC.
    register_initial : int
        The starting register address (1-based) to read data from.
    register_final : int
        The ending register address (1-based) to read data from.
    TRNData : dict
        A nested dictionary containing TRNSYS simulation data, where the PLC outputs will be stored.

    Raises
    ------
    Exception
        If an error occurs during the reading process or updating TRNSYS data, an exception is raised.
        The error is logged using the logging module.

    Examples
    --------
    >>> client = ModbusTcpClient('192.168.1.1', 502)
    >>> trn_data = {'simulationModel': {'outputs': [0, 0, 0]}}
    >>> read_from_plc(client, 1, 3, trn_data)
    >>> # Data from registers 1, 2, and 3 on the PLC is read and stored in 'trn_data'

    """

    arrayOfResponses = []
    
    try: 
        for addressR in range(register_initial-1, register_final):
            responseR = client.read_holding_registers(addressR)
            registerValue = responseR.getRegister(0)
            arrayOfResponses.append(registerValue)

        # Send response to TRNSYS.
        for x in range(0,(register_final-register_initial)+1):
            TRNData[simulationModel]["outputs"][x] = arrayOfResponses[x]

    except Exception as e:
        logging.error(f"Error writing to TRNSYS: {e}")

# --------------------------------------------------------------------------------
        
def Initialization(TRNData: Dict[str, Dict[str, List[Union[int, float]]]]) -> Tuple:
    """ 
    Function called at TRNSYS initialization. 

    Creates separate processes for each TCP connection to initialize
    Modbus TCP clients for communication with PLCs. Global variables are 
    set to store the Modbus clients for later use in the simulation.

    Parameters
    ----------
    TRNData : dict
        A nested dictionary containing TRNSYS simulation data.

    Returns
    -------
    tuple
        A tuple containing the Modbus TCP clients for the 'lab', 'hot_dock', 'heat_dock', and 'regulus' processes.

    Raises
    ------
    Exception
        If an error occurs during the initialization process, an exception is raised.
        The error is logged using the logging module.

    Examples
    --------
    >>> trn_data = {'simulationModel': {'outputs': [0, 0, 0]}}
    >>> lab_client, hot_dock_client, heat_dock_client, regulus_client = Initialization(trn_data)
    >>> # Use 'lab_client', 'hot_dock_client', 'heat_dock_client', and 'regulus_client' for Modbus communication

    """
    # Global variables for all simulation sequences. #client_regulus
    global client_lab, client_hot_dock
    
    try:

        # Create separate processes for each TCP connection
        client_lab = init_modbus_client(LAB_SERVER_IP, SERVER_PORT_1)
        client_hot_dock = init_modbus_client(HOT_DOCK_SERVER_IP, SERVER_PORT_2)

        # Return the actual Modbus clients #client_regulus
        return client_lab,client_hot_dock
    
    
    except Exception as e:
        # even if one process encounters an error, the clients from other processes are properly closed
        logging.error(f"Error during initialization: {e}")

        raise

    

# --------------------------------------------------------------------------------

def StartTime(TRNData: Dict[str, Dict[str, List[Union[int, float]]]]) -> None:
    """
    Function called at TRNSYS starting time (not an actual time step, 
    initial values should be reported).

    Parameters
    ----------
    TRNData : dict
        A nested dictionary containing TRNSYS simulation data.

    Returns
    ------------
    None

    """

    return

 
# --------------------------------------------------------------------------------

def Iteration(TRNData: Dict[str, Dict[str, List[Union[int, float]]]]) -> None:
    """
    Function called at each TRNSYS iteration within a time step.

    Parameters
    ----------
    TRNData : dict
        A nested dictionary containing TRNSYS simulation data.

    Returns
    ------------
    None

    """

    return

# --------------------------------------------------------------------------------

async def _run_end_of_time_step(client_lab, client_hot_dock, inputs_lab, inputs_hot_dock):
    try:
        # Mark the start of the asynchronous process
        logging.debug("Async process started")

        # Await the asynchronous write functions
        await asyncio.gather(
            async_write_to_plc(client_lab, inputs_lab, LAB_RW_REGISTER_INITIAL, LAB_RW_REGISTER_FINAL),
            async_write_to_plc(client_hot_dock, inputs_hot_dock, HOT_DOCK_RW_REGISTER_INITIAL, HOT_DOCK_RW_REGISTER_FINAL)
        )

        # Mark the end of the asynchronous process
        logging.debug("Async process completed")

        await asyncio.sleep(SIM_SLEEP)
    except Exception as e:
        logging.error(f"Error during EndOfTimeStep: {e}")

def EndOfTimeStep(TRNData: Dict[str, Dict[str, List[Union[int, float]]]]) -> None:
    """
    Function called at the end of each time step after iteration and before moving 
    on to the next time step.
    
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
    TRNinputs = TRNData[simulationModel]["inputs"]

    inputs_lab = []
    inputs_hot_dock = []

    for index, value in enumerate(TRNinputs):
        if index == 5:
            inputs_lab.append(value)
        elif 3 <= index + 1 <= 4:
            inputs_hot_dock.append(value)

    try:
        # Create an event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Run the asynchronous function using the event loop
        loop.run_until_complete(_run_end_of_time_step(client_lab, client_hot_dock, inputs_lab, inputs_hot_dock))

        # Close the event loop
        loop.close()

    except Exception as e:
        logging.error(f"Error during EndOfTimeStep: {e}")

    return

# --------------------------------------------------------------------------------

def LastCallOfSimulation(TRNData: Dict[str, Dict[str, List[Union[int, float]]]]) -> None:
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
        if client_lab:
            client_lab.close()
        if client_hot_dock:
            client_hot_dock.close()

        logging.shutdown()

    except Exception as e:
        logging.error(f"Error during the last call of simulation: {e}")
        raise

    return
