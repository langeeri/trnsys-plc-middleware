import tkinter as tk
from tkinter import messagebox
from server_config import SERVER_CONFIGS

def add_server():
    host = host_entry.get()
    port = port_entry.get()
    rw_register_initial = rw_initial_entry.get()
    rw_register_final = rw_final_entry.get()
    input_indexes = input_indexes_entry.get()
    r_register_initial = r_initial_entry.get()
    r_register_final = r_final_entry.get()

    new_server = {
        'host': host,
        'port': int(port),
        'rw_register_initial': int(rw_register_initial),
        'rw_register_final': int(rw_register_final),
        'input_indexes': list(map(int, input_indexes.split(','))),
        'r_register_initial': int(r_register_initial) if r_register_initial else None,
        'r_register_final': int(r_register_final) if r_register_final else None
    }

    SERVER_CONFIGS.append(new_server)
    with open("server_config.py", "w") as config_file:
        config_file.write(f"SERVER_CONFIGS = {str(SERVER_CONFIGS)}")
    update_server_listbox()
    clear_entries()

def delete_selected_server():
    selected_index = servers_listbox.curselection()
    if selected_index:
        SERVER_CONFIGS.pop(selected_index[0])
        with open("server_config.py", "w") as config_file:
            config_file.write(f"SERVER_CONFIGS = {str(SERVER_CONFIGS)}")
        update_server_listbox()

def clear_entries():
    host_entry.delete(0, tk.END)
    port_entry.delete(0, tk.END)
    rw_initial_entry.delete(0, tk.END)
    rw_final_entry.delete(0, tk.END)
    input_indexes_entry.delete(0, tk.END)
    r_initial_entry.delete(0, tk.END)
    r_final_entry.delete(0, tk.END)

def update_server_listbox():
    servers_listbox.delete(0, tk.END)
    for server in SERVER_CONFIGS:
        servers_listbox.insert(tk.END, f"{server['host']}:{server['port']}")

def update_server_listbox():
    servers_listbox.delete(0, tk.END)
    for server in SERVER_CONFIGS:
        servers_listbox.insert(tk.END, f"{server['host']}:{server['port']}")

# Create the main window
root = tk.Tk()
root.title("Server Configuration GUI")

# Labels
tk.Label(root, text="Host:").grid(row=0, column=0, sticky=tk.E)
tk.Label(root, text="Port:").grid(row=1, column=0, sticky=tk.E)
tk.Label(root, text="RW Initial Register:").grid(row=2, column=0, sticky=tk.E)
tk.Label(root, text="RW Final Register:").grid(row=3, column=0, sticky=tk.E)
tk.Label(root, text="Input Indexes (comma-separated):").grid(row=4, column=0, sticky=tk.E)
tk.Label(root, text="R Initial Register:").grid(row=5, column=0, sticky=tk.E)
tk.Label(root, text="R Final Register:").grid(row=6, column=0, sticky=tk.E)

# Entry widgets
host_entry = tk.Entry(root)
port_entry = tk.Entry(root)
rw_initial_entry = tk.Entry(root)
rw_final_entry = tk.Entry(root)
input_indexes_entry = tk.Entry(root)
r_initial_entry = tk.Entry(root)
r_final_entry = tk.Entry(root)

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
rw_initial_entry.grid(row=2, column=1)
rw_final_entry.grid(row=3, column=1)
input_indexes_entry.grid(row=4, column=1)
r_initial_entry.grid(row=5, column=1)
r_final_entry.grid(row=6, column=1)

servers_listbox.grid(row=0, column=2, rowspan=7, padx=10, pady=10)
add_button.grid(row=7, column=0, pady=5)
delete_button.grid(row=7, column=1, pady=5)
clear_button.grid(row=8, column=0, columnspan=2, pady=5)

# Run the GUI
root.mainloop()
