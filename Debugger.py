import os
import logging
import time as osTime
from typing import Dict, List, Tuple, Union
from multiprocessing import Process
from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadBuilder, Endian


# Pass the name of the TRNSYS .deck file to the simulationModel variable.
simulationModel = os.path.splitext(os.path.basename(__file__))[0]

# --------------------------- Constants --------------------------------------

SIM_SLEEP = 1

SERVER_PORT_1 = 502
SERVER_PORT_2 = 503

LAB_SERVER_IP = '127.0.0.1'
HOT_DOCK_SERVER_IP = '127.0.0.1'

LAB_RW_REGISTER_INITIAL = 1
LAB_RW_REGISTER_FINAL = 1

HOT_DOCK_RW_REGISTER_INITIAL = 1
HOT_DOCK_RW_REGISTER_FINAL = 2


def init_modbus_client(host: str, port: int) -> ModbusTcpClient:
    try:
        client = ModbusTcpClient(host=host, port=port)
        print(f"Modbus client initialized successfully for {host}:{port}")
        return client
    except Exception as e:
        print(f"Error initializing Modbus client: {e}")
        raise


# Create separate processes for each TCP connection
print("Initializing lab_client...")
lab_client = init_modbus_client(LAB_SERVER_IP, SERVER_PORT_1)
print("Initializing hot_dock_client...")
hot_dock_client = init_modbus_client(HOT_DOCK_SERVER_IP, SERVER_PORT_2)

# Additional print statements for debugging
print(f"lab_client address: {lab_client}")
print(f"hot_dock_client address: {hot_dock_client}")