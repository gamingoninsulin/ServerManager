# this file -> MinecraftServerHandler.py
import json
import subprocess
import os
import threading
from MinecraftColorCodeParser import MinecraftColorCodeParser  # import MinecraftColorCodeParser


class MinecraftServerHandler:
    def __init__(self, console_output_callback):
        self.server_status = "Stopped"
        with open(os.path.join(os.getcwd(), 'config.json')) as f:  # Use absolute path for config.json
            self.config = json.load(f)
        self.process = None
        self.console_output_callback = console_output_callback

    def start_server(self):
        if self.server_status == "Stopped":
            server_jar_path = os.path.join(os.getcwd(), self.config['server_jar'])  # Use absolute path for server.jar
            if not os.path.isfile(server_jar_path):
                print("Server jar not found: " + server_jar_path)
                return

            self.server_status = "Running"

            # Create the PyServer directory if it doesn't exist
            os.makedirs('PyServer', exist_ok=True)

            # Change the current working directory to PyServer
            os.chdir('PyServer')

            self.process = subprocess.Popen(
                ['java', '-Xmx' + self.config['ram_gb'] + 'G', '-jar', self.config['server_jar'], 'nogui'],
                stdout=subprocess.PIPE)

            # Check if the process is None
            if self.process is None:
                print("Failed to start the server.")
                self.server_status = "Stopped"
                return

            # Start a new thread to read the console output
            threading.Thread(target=self.read_console_output, daemon=True).start()

            print("Server started.")
        else:
            print("Server is already running.")

    def stop_server(self):
        if self.server_status == "Running":
            self.server_status = "Stopped"
            # Check if self.process is not None and the process is still running before trying to write to its stdin
            if self.process is not None and self.process.poll() is None:
                self.process.stdin.write(b'stop\n')
                self.process.stdin.flush()
                # Wait for the server process to terminate
                self.process.wait()
                print("Server stopped.")
            else:
                print("Server is not running or has crashed.")
        else:
            print("Server is not running.")

    def restart_server(self):
        if self.server_status == "Running":
            self.stop_server()
            self.start_server()
        else:
            print("Server is not running. Can't restart.")

    def send_console_input(self, console_input):
        if self.server_status == "Running":
            self.process.stdin.write(console_input.encode() + b'\n')  # Add a newline character
            self.process.stdin.flush()
        else:
            print("Server is not running. Can't send console input.")

    def read_console_output(self):
        for line in iter(self.process.stdout.readline, b''):
            # Parse the console output
            parsed_output = MinecraftColorCodeParser.parse_color_codes(line.decode())

            # Print the parsed console output for debugging
            print(parsed_output, end='')

            # Call the callback function with the parsed console output
            self.console_output_callback(parsed_output)
