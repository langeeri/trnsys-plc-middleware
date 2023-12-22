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
import datetime
import time as osTime
import numpy as np
from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadBuilder, Endian


# ------------------------------- TRNSYS -----------------------------------------

# Pass the name of the TRNSYS .deck file to the simulationModel variable.
simulationModel = os.path.splitext(os.path.basename(__file__))[0]

# Simulation sleep time
SIM_SLEEP = 1 
SERVER_PORT = 502

# ------------------------------- Servers -----------------------------------------


LAB_SERVER_IP = '10.208.8.11' 

HEAT_DOCK_SERVER_IP = '10.202.240.12' 

HOT_DOCK_SERVER_IP = '10.202.240.13'

#REGULUS_SERVER_IP = '10.208.227.188'

# ------------------------------- Registers -----------------------------------------

# ID of enabled ModBus read/write registers.
LAB_RW_REGISTER_INITIAL = 1
LAB_RW_REGISTER_FINAL = 1

# ID of enabled ModBus read/write registers.
HOT_DOCK_RW_REGISTER_INITIAL = 1
HOT_DOCK_RW_REGISTER_FINAL = 2

# ID of enabled ModBus read/write registers.
HEAT_DOCK_RW_REGISTER_INITIAL = 1
HEAT_DOCK_RW_REGISTER_FINAL = 3

# ID of enabled ModBus read registers.
HEAT_DOCK_R_REGISTER_INITIAL = 4
HEAT_DOCK_R_REGISTER_FINAL = 5

#Regulus
# ID of enabled ModBus read/write registers.
#REGULUS_RW_REGISTER_INITIAL = 1
#REGULUS_RW_REGISTER_FINAL = 13

# ID of enabled ModBus read/write registers that SHOULD NOT be multiplied by *10.
#REGULUS_RW_REGISTER_L1 = 8
#REGULUS_RW_REGISTER_L2 = 9
#REGULUS_RW_REGISTER_L3 = 10
#REGULUS_RW_REGISTER_HDO = 13

# ID of enabled ModBus read registers.
#REGULUS_R_REGISTER_INITIAL =49
#REGULUS_R_REGISTER_FINAL = 56

# --------------------------------------------------------------------------------
#                                   START
# --------------------------------------------------------------------------------

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

    # Global variables for all simulation sequences.  
    global client_lab, client_heat_dock,client_hot_dock,client_regulus

    # Open communication between trnsys and PLC.
    client_lab = ModbusTcpClient(host=LAB_SERVER_IP, port=SERVER_PORT)
    client_heat_dock = ModbusTcpClient(host=HEAT_DOCK_SERVER_IP, port=SERVER_PORT)
    client_hot_dock = ModbusTcpClient(host=HOT_DOCK_SERVER_IP, port=SERVER_PORT)
    #client_regulus = ModbusTcpClient(host=REGULUS_SERVER_IP, port=SERVER_PORT)
    
    return


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

def EndOfTimeStep(TRNData):
    """
    Function called at the end of each time step after iteration and 
    before moving on to next time step.
    Writes data from TRNSYS to the PLC ModBus registers.
    Reads data from the PLC ModBus registers to TRNSYS.
    Writes the contents of the nested TRNData dictionary to the log file.
    
    Parameters
    ------------
    TRNData : nested_dict
        Data received from TRNSYS.

    Returns
    ------------
    None

    """
    # Assign to variables.
    inputs = TRNData[simulationModel]["inputs"]
   

    # ------------------------------- Write to registers -----------------------------

    # Create builder.
    builder_lab = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
    builder_hot_dock = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
    builder_heat_dock = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
    #builder_regulus = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)

    # Reset builder.
    builder_lab.reset()
    builder_hot_dock.reset()
    builder_heat_dock.reset()
    #builder_regulus.reset()

    # Read values from TRNSYS.
    for index, value in enumerate(inputs):
        inputConverted = int(value * 10)

        if index == 5: 
            builder_lab.add_16bit_int(inputConverted)
            #builder_regulus.add_16bit_int(inputConverted)
        elif 3 <= index + 1 <= 4:  
            builder_hot_dock.add_16bit_int(inputConverted)
        elif 0 <= index + 1 <= 2 or index == 7:  
            builder_heat_dock.add_16bit_int(inputConverted)
        #elif 5 <= index + 1 <= 6: 
            #builder_regulus.add_16bit_int(inputConverted)

    # Convert values to registers.
    inputs_lab = builder_lab.to_registers()
    inputs_hot_dock = builder_hot_dock.to_registers()
    inputs_heat_dock = builder_heat_dock.to_registers()
    #inputs_regulus = builder_regulus.to_registers()

    # Write values to Lab registers.
    for addressRW in range(LAB_RW_REGISTER_INITIAL - 1, LAB_RW_REGISTER_FINAL):
        responseRW = client_lab.write_register(addressRW, inputs_lab[addressRW])

    # Write values to Hot Dock registers.
    for addressRW in range(HOT_DOCK_RW_REGISTER_INITIAL - 1, HOT_DOCK_RW_REGISTER_FINAL):
        responseRW = client_hot_dock.write_register(addressRW, inputs_hot_dock[addressRW])

    # Write values to Heat Dock registers.
    for addressRW in range(HEAT_DOCK_RW_REGISTER_INITIAL - 1, HEAT_DOCK_RW_REGISTER_FINAL):
        responseRW = client_heat_dock.write_register(addressRW, inputs_heat_dock[addressRW])

    # Write values to regulus registers.
    #for addressRW in range(REGULUS_RW_REGISTER_INITIAL - 1, REGULUS_RW_REGISTER_FINAL):
        #responseRW = client_regulus.write_register(addressRW, inputs_regulus[addressRW])

    # ------------------------------- Read from registers -----------------------------

    # Blank array for responses.
    arrayOfResponses = []

    # Handle response from PLC, append response to array of responses.
    for addressR in range(HEAT_DOCK_R_REGISTER_INITIAL, HEAT_DOCK_R_REGISTER_FINAL+1):
        responseR = client_heat_dock.read_holding_registers(addressR)
        registerValue = responseR.getRegister(0)
        arrayOfResponses.append(registerValue)

    # Send response to TRNSYS.
    for x in range(0,(HEAT_DOCK_R_REGISTER_FINAL-HEAT_DOCK_R_REGISTER_INITIAL)+1):
        TRNData[simulationModel]["outputs"][x] = arrayOfResponses[x]

    # Set sleep time.
    osTime.sleep(SIM_SLEEP)

    
    return


# --------------------------------------------------------------------------------

def LastCallOfSimulation(TRNData):
    """
    Function called at the end of the simulation (once).
    Outputs are meaningless at this call.
    Writes the contents of the nested TRNData dictionary to logFile.
    Closes the log files.

    Parameters
    ------------
    TRNData : nested_dict
        Data received from TRNSYS.

    Returns
    ------------
    None

    """

    # Close connection
    client_lab.close()
    client_hot_dock.close()
    client_heat_dock.close()
    #client_regulus.close()

    return