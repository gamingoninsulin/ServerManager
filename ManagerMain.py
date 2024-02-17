# ManagerMain
import tkinter as tk
from tkinter import ttk, filedialog
import requests
import subprocess
import json
import os
import time
import shutil
from ServerProperties import PropertiesTab
import threading

root = tk.Tk()
root.title("Minecraft Server Manager")
root.configure(bg='lightblue')

frame = tk.Frame(root, bg='lightblue')  # Set the background color here
frame.pack(padx=3, pady=3)  # The padx and pady options create the effect of a transparent border

server = None

# Load manager settings
with open('ManagerSettings.json', 'r') as file:
    manager_settings = json.load(file)


# Function to get public IP address
def get_public_ip():
    response = requests.get('https://api.ipify.org')
    return response.text


# Function to get server status
def get_server_status():
    # Check if the server process has started
    if server is not None and server.poll() is None:
        # Send a command to the server
        server.stdin.write("/list\n".encode())
        server.stdin.flush()

        # Read the server's response
        response = server.stdout.readline().decode()
        return response
    else:
        return "Server not running"


# Start the server
def start_server():
    # Check if the server.jar file exists
    server_jar_path = os.path.join(os.getcwd(), "server", "server.jar")
    if not os.path.exists(server_jar_path):
        console_output.insert(tk.END, "Error: The server.jar file does not exist.\n")
        return

    console_output.insert(tk.END, "Starting server...\n")
    global server
    server = subprocess.Popen(
        ["java", "-Xmx" + manager_settings["ram_amount"] + "G", "-Xms1024M", "-jar", "server.jar", "nogui"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.dirname(server_jar_path))

    # Create a separate thread to read the server's output and print it to the console
    def print_server_output():
        for line in iter(server.stdout.readline, b''):
            console_output.insert(tk.END, line.decode())
        for line in iter(server.stderr.readline, b''):
            console_output.insert(tk.END, line.decode())

    threading.Thread(target=print_server_output).start()

    # Wait for the server to start before checking the status
    time.sleep(10)  # Adjust the sleep time as needed
    update_status_indicator()


def stop_server():
    console_output.insert(tk.END, "Stopping server...\n")
    server.stdin.write("/stop\n".encode())
    server.stdin.flush()


def restart_server():
    console_output.insert(tk.END, "Restarting server...\n")
    stop_server()
    root.after(10000, start_server)  # Wait 10 seconds before starting the server


def update_status_indicator():
    # Check server status and update the status indicator
    if server is not None and server.poll() is None:  # Server is running
        status_indicator.create_oval(5, 5, 15, 15, fill='green')
    else:  # Server is not running
        status_indicator.create_oval(5, 5, 15, 15, fill='red')

    # Update the status indicator every second (1000 milliseconds)
    root.after(1000, update_status_indicator)


def open_eula():
    eula_path = os.path.join(os.getcwd(), "server", "eula.txt")
    if os.path.exists(eula_path):
        os.system('start "EULA" "notepad.exe" "{}"'.format(eula_path))
    else:
        console_output.insert(tk.END, "Error: The eula.txt file does not exist.\n")


def manage_plugins():
    plugins_dir = os.path.join(os.getcwd(), "server", "plugins")
    if os.path.exists(plugins_dir):
        os.system('start "Plugins" "{}"'.format(plugins_dir))
    else:
        console_output.insert(tk.END, "Error: The plugins directory does not exist.\n")


def download_plugins():
    # Create a new window
    download_window = tk.Toplevel(root)
    download_window.title("Download Plugins")

    # Create a text area at the top
    plugin_info = tk.Text(download_window, height=10)
    plugin_info.pack(fill=tk.BOTH, expand=True)

    # Create a search bar at the bottom
    search_entry = tk.Entry(download_window)
    search_entry.pack(side=tk.BOTTOM, fill=tk.X, expand=True, padx=10, pady=(0, 10))

    def search_plugins():
        # Get the search query
        query = search_entry.get()

        # Search for plugins (you'll need to implement this part yourself)
        results = "Searching for plugins is not implemented in this example."

        # Display the results in the text area
        plugin_info.delete(1.0, tk.END)  # Clear the text area
        plugin_info.insert(tk.END, results)

    # Bind the Return key to the search_plugins function
    download_window.bind('<Return>', lambda event: search_plugins())


# Function to select and copy a server JAR file
def select_server_jar():
    # Open a file dialog to select the server.jar file
    server_jar_path = filedialog.askopenfilename(filetypes=[("JAR files", "*.jar")])
    if not server_jar_path:
        console_output.insert(tk.END, "Error: No file selected.\n")
        return

    # Create the server directory if it doesn't exist
    server_dir = os.path.join(os.getcwd(), "server")
    os.makedirs(server_dir, exist_ok=True)

    # Copy and rename the selected file to server.jar in the server directory
    dest_jar_path = os.path.join(server_dir, "server.jar")
    shutil.copy(server_jar_path, dest_jar_path)


def kill_server():
    if server is not None:
        console_output.insert(tk.END, "Forcefully stopping server...\n")
        server.kill()


# Create a custom style for the notebook and frames
style = ttk.Style()
style.configure('TNotebook', background='lightblue')  # Set the notebook's background color
style.configure('TFrame', background='lightblue')  # Set the frame's background color
style.configure('TNotebook.Tab', background='lightblue')  # Set the tab's background color

# Top bar with modified background color
top_frame = tk.Frame(root, bg='lightblue')  # Set the background color here
top_frame.pack(side=tk.TOP, fill=tk.X)

ip_label = tk.Label(top_frame, text="IP Address: " + get_public_ip() + ":25565", bg='lightblue')  # Set label's
# background color
ip_label.pack(side=tk.LEFT)

# Online status indicator
status_indicator = tk.Canvas(top_frame, width=20, height=20, bg='lightblue',
                             highlightthickness=0)  # Set canvas's background color
status_indicator.pack(side=tk.LEFT)
status_indicator.create_oval(5, 5, 15, 15, fill='red')  # Red dot initially

status_label = tk.Label(top_frame, text=get_server_status(), bg='lightblue')  # Set label's background color
status_label.pack(side=tk.LEFT)

# Console area
console_frame = tk.Frame(root, bg='lightblue')  # Set the background color here
console_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

console_output = tk.Text(console_frame, bg='lightblue')  # Set the background color here
console_output.pack(fill=tk.BOTH, expand=True)

command_entry = tk.Entry(console_frame, bg='lightblue')  # Set the background color here
command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=(0, 10))

send_button = tk.Button(console_frame, text="Send Command", command=lambda: send_command(command_entry.get()))
send_button.pack(side=tk.LEFT, padx=10, pady=(0, 10))

# Bind the Return key to the send_command function
root.bind('<Return>', lambda event: send_command(command_entry.get()))


def send_command(command):
    # Check if the server process is still running
    if server.poll() is None:
        # Send a command to the server
        server.stdin.write((command + "\n").encode())
        server.stdin.flush()
    else:
        console_output.insert(tk.END, "Error: Server is not running.\n")

    # Clear the command entry
    command_entry.delete(0, tk.END)


# Tabs
tab_parent = ttk.Notebook(root)  # No need to set a custom style for the notebook here
tab1 = ttk.Frame(tab_parent)  # No need to set a custom style for the frame here
tab2 = PropertiesTab(tab_parent, console_output)  # Pass console_output here and use a custom style for the frame
tab_parent.add(tab1, text="General")
tab_parent.add(tab2, text="Properties")
# Add more tabs as needed...
tab_parent.pack(expand=1, fill='both')

button_width = max(len("Open EULA"), len("Manage Plugins"), len("Download Plugins"),
                   len("Start Server"), len("Stop Server"), len("Restart Server"))

# Quick server controls
control_frame = tk.Frame(root, bg='lightblue')  # Set the background color here
control_frame.pack(side=tk.RIGHT, fill=tk.Y)

eula_button = tk.Button(tab1, text="Open EULA", command=open_eula)
eula_button.pack(fill=tk.X, padx=10, pady=2)

plugins_button = tk.Button(tab1, text="Manage Plugins", command=manage_plugins)
plugins_button.pack(fill=tk.X, padx=10, pady=2)

Download_button = tk.Button(tab1, text="Download Plugins", command=download_plugins)
Download_button.pack(fill=tk.X, padx=10, pady=2)

select_jar_button = tk.Button(tab1, text="Select Server JAR", command=select_server_jar)
select_jar_button.pack(fill=tk.X, padx=10, pady=2)

start_button = tk.Button(control_frame, text="Start Server", command=start_server)
start_button.pack(fill=tk.X, padx=10, pady=(0, 10))

restart_button = tk.Button(control_frame, text="Restart Server", command=restart_server)
restart_button.pack(fill=tk.X, padx=10, pady=(0, 10))

stop_button = tk.Button(control_frame, text="Stop Server", command=stop_server)
stop_button.pack(fill=tk.X, padx=10, pady=(0, 10))

kill_button = tk.Button(control_frame, text="Kill Server", command=kill_server)
kill_button.pack(fill=tk.X, padx=10, pady=(0, 10))

update_status_indicator()

root.mainloop()
