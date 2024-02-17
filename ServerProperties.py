import tkinter as tk
from tkinter import ttk
import os


class PropertiesTab(ttk.Frame,):
    def __init__(self, parent, console_output):
        super().__init__(parent)

        self.console_output = console_output  # Reference to the console output Text widget

        self.textbox = tk.Text(self)
        self.textbox.pack(fill=tk.BOTH, expand=True)
        self.textbox.pack_forget()  # Hide the textbox initially

        self.textbox = tk.Text(self)
        self.textbox.pack(fill=tk.BOTH, expand=True)
        self.textbox.pack_forget()  # Hide the textbox initially

        # Create a frame for the buttons
        button_frame = tk.Frame(self, bg='lightblue')  # Set the background color here
        button_frame.pack(side=tk.TOP, fill=tk.X)

        # Determine the width of the widest button
        button_width = max(len("Server Settings"), len("Whitelist"), len("Operators"), len("Banned Players"),
                           len("Banned IPs"), len("Save"))

        server_settings_button = tk.Button(button_frame, text="Server Settings", command=self.load_server_settings,
                                           width=button_width)
        server_settings_button.pack(fill=tk.NONE, padx=10, pady=(0, 2), anchor='center')

        whitelist_button = tk.Button(button_frame, text="Whitelist", command=self.load_server_whitelist,
                                     width=button_width)
        whitelist_button.pack(fill=tk.NONE, padx=10, pady=(0, 2), anchor='center')

        operators_button = tk.Button(button_frame, text="Operators", command=self.load_server_operators,
                                     width=button_width)
        operators_button.pack(fill=tk.NONE, padx=10, pady=(0, 2), anchor='center')

        banned_players_button = tk.Button(button_frame, text="Banned Players", command=self.load_server_banned_players,
                                          width=button_width)
        banned_players_button.pack(fill=tk.NONE, padx=10, pady=(0, 2), anchor='center')

        banned_ips_button = tk.Button(button_frame, text="Banned IPs", command=self.load_server_banned_ips,
                                      width=button_width)
        banned_ips_button.pack(fill=tk.NONE, padx=10, pady=(0, 2), anchor='center')

        save_button = tk.Button(button_frame, text="Save", command=self.save_server_settings, width=button_width)
        save_button.pack(fill=tk.NONE, padx=10, pady=(0, 2), anchor='center')


    # load server settings
    def load_server_settings(self):
        if os.path.exists('server.properties'):  # Check if the file exists
            with open('server.properties', 'r') as file:
                self.textbox.delete('1.0', tk.END)
                self.textbox.insert(tk.END, file.read())
            self.textbox.pack(fill=tk.BOTH, expand=True)  # Show the textbox
        else:
            self.console_output.insert(tk.END, "Error: The server.properties file does not exist.\n")

    def save_server_settings(self):
        with open('server.properties', 'w') as file:
            file.write(self.textbox.get('1.0', tk.END))
        self.textbox.pack_forget()  # Hide the textbox

    # load server whitelist
    def load_server_whitelist(self):
        if os.path.exists('whitelist.json'):  # Check if the file exists
            with open('whitelist.json', 'r') as file:
                self.textbox.delete('1.0', tk.END)
                self.textbox.insert(tk.END, file.read())
            self.textbox.pack(fill=tk.BOTH, expand=True)  # Show the textbox
        else:
            self.console_output.insert(tk.END, "Error: The whitelist.json file does not exist.\n")

    def save_server_whitelist(self):
        with open('whitelist.json', 'w') as file:
            file.write(self.textbox.get('1.0', tk.END))
        self.textbox.pack_forget()  # Hide the textbox

    # load server whitelist
    def load_server_operators(self):
        if os.path.exists('ops.json'):  # Check if the file exists
            with open('ops.json', 'r') as file:
                self.textbox.delete('1.0', tk.END)
                self.textbox.insert(tk.END, file.read())
            self.textbox.pack(fill=tk.BOTH, expand=True)  # Show the textbox
        else:
            self.console_output.insert(tk.END, "Error: The ops.json file does not exist.\n")

    def save_server_operator(self):
        with open('ops.json', 'w') as file:
            file.write(self.textbox.get('1.0', tk.END))
        self.textbox.pack_forget()  # Hide the textbox

    # load server whitelist
    def load_server_banned_players(self):
        if os.path.exists('banned-players.json'):  # Check if the file exists
            with open('banned-players.json', 'r') as file:
                self.textbox.delete('1.0', tk.END)
                self.textbox.insert(tk.END, file.read())
            self.textbox.pack(fill=tk.BOTH, expand=True)  # Show the textbox
        else:
            self.console_output.insert(tk.END, "Error: The banned-players.json file does not exist.\n")

    def save_server_banned_players(self):
        with open('banned-players.json', 'w') as file:
            file.write(self.textbox.get('1.0', tk.END))
        self.textbox.pack_forget()  # Hide the textbox

    # load server whitelist
    def load_server_banned_ips(self):
        if os.path.exists('banned_ips.json'):  # Check if the file exists
            with open('banned_ips.json', 'r') as file:
                self.textbox.delete('1.0', tk.END)
                self.textbox.insert(tk.END, file.read())
            self.textbox.pack(fill=tk.BOTH, expand=True)  # Show the textbox
        else:
            self.console_output.insert(tk.END, "Error: The banned-ips.json file does not exist.\n")

    def save_server_banned_ips(self):
        with open('banned-players.json', 'w') as file:
            file.write(self.textbox.get('1.0', tk.END))
        self.textbox.pack_forget()  # Hide the textbox
