import pytest
from unittest.mock import patch, MagicMock
from src.main import ModbusServer # Adjust the import path

@pytest.fixture
def modbus_server():
    # Provide necessary parameters for ModbusServer initialization
    return ModbusServer(host="107.0.0.1", port=502, rw_registers=None, input_indexes=[], r_registers=None)

@patch("src.main.ModbusTcpClient")  # Adjust the import path
def test_open_connection_success(mock_modbus_client, modbus_server):
    # Mock the ModbusTcpClient to avoid actual network connections
    mock_client_instance = MagicMock()
    mock_modbus_client.return_value = mock_client_instance

    # Call the open_connection method
    modbus_server.open_connection()

    # Assert that the ModbusTcpClient was initialized with the correct parameters
    mock_modbus_client.assert_called_once_with(host="107.0.0.1", port=502)

    # Assert that the client attribute of the ModbusServer was set to the mock client instance
    assert modbus_server.client == mock_client_instance

@patch("src.main.ModbusTcpClient", side_effect=Exception("Mocked connection error"))  # Adjust the import path
def test_open_connection_failure(mock_modbus_client, modbus_server):
    # Call the open_connection method, which should raise an exception
    with pytest.raises(Exception, match="Mocked connection error"):
        modbus_server.open_connection()

    # Assert that the ModbusTcpClient was initialized with the correct parameters
    mock_modbus_client.assert_called_once_with(host="107.0.0.1", port=502)

    # Assert that the client attribute of the ModbusServer is still None
    assert modbus_server.client is None


