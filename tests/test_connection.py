
"""test_connection.py

This module contains tests for the `ModbusServer` functionality in the communication middleware project.

The tests are designed to ensure that the `ModbusServer` class can successfully establish a connection with a Modbus client, 
handle connection errors, and interact correctly with the Modbus protocol. The module uses the pytest framework for defining 
test cases and the unittest.mock library to mock external dependencies.

Classes
-------
ModbusServer
    A class representing a server in a Modbus communication setup.

Functions
---------
modbus_server()
    Pytest fixture for creating a `ModbusServer` instance.

test_open_connection_success()
    Test case for a successful connection.

test_open_connection_failure()
    Test case for handling connection failures.

Dependencies
------------
pytest
    The framework used for writing and running the test cases.

unittest.mock
    Used for mocking external dependencies.

Author
------
Erika Langerová

Date Created
------------
July 2023

Last Modified
-------------
January 2024

"""

# Third party imports
import pytest
from unittest.mock import patch, MagicMock

# Local imports
from src.main import ModbusServer


@pytest.fixture
def modbus_server() -> ModbusServer:
    """
    Fixture for creating a ModbusServer instance with predefined parameters.

    Returns:
        ModbusServer: A ModbusServer instance initialized with specified host, port, and register settings.
    
    """
    # Provide necessary parameters for ModbusServer initialization
    return ModbusServer(host="107.0.0.1", port=502, rw_registers=None, input_indexes=[], r_registers=None)


@patch("src.main.ModbusTcpClient")  
def test_open_connection_success(mock_modbus_client: MagicMock, modbus_server: ModbusServer) -> None:
    """
    Test to verify successful opening of a Modbus connection.

    Args:
        mock_modbus_client (MagicMock): Mocked ModbusTcpClient.
        modbus_server (ModbusServer): The ModbusServer instance to test.
    
    """
    # Mock the ModbusTcpClient to avoid actual network connections
    mock_client_instance = MagicMock()
    mock_modbus_client.return_value = mock_client_instance

    # Call the open_connection method
    modbus_server.open_connection()

    # Assert that the ModbusTcpClient was initialized with the correct parameters
    mock_modbus_client.assert_called_once_with(host="107.0.0.1", port=502)

    # Assert that the client attribute of the ModbusServer was set to the mock client instance
    assert modbus_server.client == mock_client_instance


@patch("src.main.ModbusTcpClient", side_effect=Exception("Mocked connection error")) 
def test_open_connection_failure(mock_modbus_client: MagicMock, modbus_server: ModbusServer) -> None:
    """
    Test to verify behavior when opening a Modbus connection fails.

    Args:
        mock_modbus_client (MagicMock): Mocked ModbusTcpClient with a side effect to simulate an exception.
        modbus_server (ModbusServer): The ModbusServer instance to test.
    
    """
    # Call the open_connection method, which should raise an exception
    with pytest.raises(Exception, match="Mocked connection error"):
        modbus_server.open_connection()

    # Assert that the ModbusTcpClient was initialized with the correct parameters
    mock_modbus_client.assert_called_once_with(host="107.0.0.1", port=502)

    # Assert that the client attribute of the ModbusServer is still None
    assert modbus_server.client is None


