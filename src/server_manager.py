
"""server_manager.py

Manage Modbus server configurations with a graphical user interface.

This script contains definitions for managing Modbus server settings
and a GUI for easy manipulation of these configurations. It includes
functions for adding, deleting, and modifying server configurations.

The output of the GUI is directed to the server_config.py, from which
the main.py module reads the ModBus servers definitions.

The `SERVER_CONFIGS` list consists of dictionaries, each representing
the configuration of a Modbus server, including details such as host
address, port number, and register information.

Attributes
----------
SERVER_CONFIGS : list of dict
    A list containing the configurations for each Modbus server. Each
    dictionary includes the host, port, and register information.

Functions
---------
add_server()
    Adds a new server configuration to `SERVER_CONFIGS` and updates
    the configuration file.
delete_selected_server()
    Removes the selected server configuration from `SERVER_CONFIGS`.
clear_entries()
    Clears all input fields in the GUI.
update_server_listbox()
    Updates the listbox to display the current server configurations.

See Also
--------
tkinter : The standard Python interface to the Tk GUI toolkit.

Notes
-----
- The script should be directly run to launch the GUI for managing server
  configurations.
- Direct modifications to the `SERVER_CONFIGS` affect Modbus server
  connections.
- Ensure accurate and valid data entry for stable Modbus server
  communication.

Examples
--------
To launch the GUI, run the script:

    $ python server_manager.py

In the GUI, add, delete, or view Modbus server configurations as needed.

"""

if __name__ == "__main__":
    
    # Standard library imports
    from typing import NoReturn

    # Third party imports
    import tkinter as tk
    
    # Local imports
    from server_config import SERVER_CONFIGS


    def add_server() -> NoReturn:
        """
        Add a new server configuration to the SERVER_CONFIGS list and update the configuration file.

        Retrieves server details from the GUI entries, creates a dictionary for the new server,
        appends it to SERVER_CONFIGS, and writes the updated list to the server_config.py file.
        
        """
        host = host_entry.get()
        port = port_entry.get()
        rw_registers = rw_registers_entry.get()
        input_indexes = input_indexes_entry.get()
        r_registers = r_registers_entry.get()

        new_server = {
            'host': host,
            'port': int(port),
            'rw_registers': [] if not rw_registers else list(map(int, rw_registers.split(','))),
            'input_indexes': list(map(int, input_indexes.split(','))),
            'r_registers': [] if not r_registers else list(map(int, r_registers.split(',')))
        }

        SERVER_CONFIGS.append(new_server)
        with open("server_config.py", "w") as config_file:
            config_file.write(f"SERVER_CONFIGS = {str(SERVER_CONFIGS)}")
        update_server_listbox()
        clear_entries()

    def delete_selected_server() -> NoReturn:
        """
        Delete the selected server configuration from the SERVER_CONFIGS list and update the configuration file.

        Identifies the selected server in the GUI listbox, removes it from SERVER_CONFIGS,
        and writes the updated list to the server_config.py file.
        
        """
        selected_index = servers_listbox.curselection()
        if selected_index:
            SERVER_CONFIGS.pop(selected_index[0])
            with open("server_config.py", "w") as config_file:
                config_file.write(f"SERVER_CONFIGS = {str(SERVER_CONFIGS)}")
            update_server_listbox()

    def clear_entries() -> NoReturn:
        """
        Clear all input fields in the GUI.
        
        """
        host_entry.delete(0, tk.END)
        port_entry.delete(0, tk.END)
        rw_registers_entry.delete(0, tk.END)
        input_indexes_entry.delete(0, tk.END)
        r_registers_entry.delete(0, tk.END)
        update_server_listbox()

    def update_server_listbox():
        """
        Update the listbox in the GUI to display the current server configurations.
        
        """
        servers_listbox.delete(0, tk.END)
        for server in SERVER_CONFIGS:
            servers_listbox.insert(tk.END, f"{server['host']}:{server['port']}")

    # Create the main window
    root = tk.Tk()
    root.title("Server Configuration GUI")

    # Labels
    tk.Label(root, text="Host:").grid(row=0, column=0, sticky=tk.E)
    tk.Label(root, text="Port:").grid(row=1, column=0, sticky=tk.E)
    tk.Label(root, text="RW Registers (comma-separated):").grid(row=2, column=0, sticky=tk.E)
    tk.Label(root, text="Input Indexes (comma-separated):").grid(row=3, column=0, sticky=tk.E)
    tk.Label(root, text="R Registers (comma-separated):").grid(row=4, column=0, sticky=tk.E)

    # Entry widgets
    host_entry = tk.Entry(root)
    port_entry = tk.Entry(root)
    rw_registers_entry = tk.Entry(root)
    input_indexes_entry = tk.Entry(root)
    r_registers_entry = tk.Entry(root)

    # Listbox to display current servers
    servers_listbox = tk.Listbox(root, selectmode=tk.SINGLE, height=5)
    update_server_listbox()

    # Buttons
    add_button = tk.Button(root, text="Add Server", command=add_server)
    delete_button = tk.Button(root, text="Delete Selected", command=delete_selected_server)
    clear_button = tk.Button(root, text="Clear Entries", command=clear_entries)

    # Grid layout
    host_entry.grid(row=0, column=1)
    port_entry.grid(row=1, column=1)
    rw_registers_entry.grid(row=2, column=1)
    input_indexes_entry.grid(row=3, column=1)
    r_registers_entry.grid(row=4, column=1)

    servers_listbox.grid(row=0, column=2, rowspan=5, padx=10, pady=10)
    add_button.grid(row=5, column=0, pady=5)
    delete_button.grid(row=5, column=1, pady=5)
    clear_button.grid(row=6, column=0, columnspan=2, pady=5)

    # Run the GUI
    root.mainloop()

