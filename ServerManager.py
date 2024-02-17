# -*- coding: utf-8 -*-
import json
import shutil
import os
import subprocess
import sys
from multiprocessing import process

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QThread, Signal, QThreadPool, QRunnable)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
                           QCursor, QFont, QFontDatabase, QGradient,
                           QIcon, QImage, QKeySequence, QLinearGradient,
                           QPainter, QPalette, QPixmap, QRadialGradient,
                           QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QLabel,
                               QLineEdit, QMainWindow, QMenu, QMenuBar,
                               QPushButton, QSizePolicy, QStatusBar, QTableWidget,
                               QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QFileDialog, QTextEdit)
from threading import Thread
from queue import Queue, Empty


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


class Worker(QRunnable):
    def __init__(self, function):
        super(Worker, self).__init__()
        self.function = function

    def run(self):
        self.function()


class OutputThread(QThread):
    signal = Signal(str)

    def __init__(self, queue):
        QThread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            try:
                line = self.queue.get_nowait().decode().strip()  # Decode bytes to string
            except Empty:
                pass  # No output
            else:
                self.signal.emit(line)  # Emit signal


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1126, 852)

        self.actionOpen_EULA = QAction(MainWindow)
        self.actionOpen_EULA.setObjectName(u"actionOpen_EULA")
        self.actionOpen_EULA.triggered.connect(self.open_eula)

        self.actionSelect_Server_jar = QAction(MainWindow)
        self.actionSelect_Server_jar.setObjectName(u"actionSelect_Server_jar")
        self.actionSelect_Server_jar.triggered.connect(self.select_server_jar)

        self.actionManage = QAction(MainWindow)
        self.actionManage.setObjectName(u"actionManage")

        self.actionDownload = QAction(MainWindow)
        self.actionDownload.setObjectName(u"actionDownload")

        self.actionserver_properties = QAction(MainWindow)
        self.actionserver_properties.setObjectName(u"actionserver_properties")

        self.actionops_json = QAction(MainWindow)
        self.actionops_json.setObjectName(u"actionops_json")

        self.actionbanned_players_json = QAction(MainWindow)
        self.actionbanned_players_json.setObjectName(u"actionbanned_players_json")

        self.actionbanned_ips_json = QAction(MainWindow)
        self.actionbanned_ips_json.setObjectName(u"actionbanned_ips_json")

        self.actioncommands_yml = QAction(MainWindow)
        self.actioncommands_yml.setObjectName(u"actioncommands_yml")

        self.actionOpen_config = QAction(MainWindow)
        self.actionOpen_config.setObjectName(u"actionOpen_config")

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 20, 1101, 771))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.Label_online = QLabel("Online")
        self.Label_online.setAlignment(Qt.AlignRight)  # Align the label to the right

        # Create a QHBoxLayout for the labels
        self.labelLayout = QHBoxLayout()
        self.labelLayout.addWidget(self.label)  # Add the server IP address label
        self.labelLayout.addWidget(self.Label_online)  # Add the "Online:" label

        # Create a QTextEdit for the file editor
        self.EditFile = QTextEdit(self.gridLayoutWidget)
        self.EditFile.setObjectName(u"EditFile")
        self.EditFile.hide()  # Hide the editor by default

        # Create a QHBoxLayout for the save and close buttons
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(10)  # Set spacing between widgets in the layout

        # Create a QPushButton for the save button
        self.SaveButton = QPushButton("Save", self.gridLayoutWidget)
        self.SaveButton.setObjectName(u"SaveButton")
        self.SaveButton.clicked.connect(self.save_file)
        self.SaveButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.SaveButton.hide()  # Hide the SaveButton by default

        # Create a QPushButton for the close button
        self.CloseButton = QPushButton("Close", self.gridLayoutWidget)
        self.CloseButton.setObjectName(u"CloseButton")
        self.CloseButton.clicked.connect(self.close_editor)
        self.CloseButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.CloseButton.hide()  # Hide the CloseButton by default

        # Add the SaveButton and CloseButton to the button layout
        self.buttonLayout.addWidget(self.SaveButton)
        self.buttonLayout.addWidget(self.CloseButton)

        # Add the button layout to the grid layout
        self.gridLayout.addLayout(self.buttonLayout, 5, 0, 1, 2)  # Span 2 columns

        # Add the button layout to the grid layout
        self.gridLayout.addLayout(self.buttonLayout, 5, 0)  # Adjusted the row index to 5

        # Add the editor, save button, and close button to the grid layout
        self.gridLayout.addWidget(self.EditFile, 4, 0, 1, 2)  # Span 2 columns
        self.gridLayout.addWidget(self.SaveButton, 5, 0)  # Column 0
        self.gridLayout.addWidget(self.CloseButton, 5, 1)  # Column 1

        # Add the label layout to the grid layout
        self.gridLayout.addLayout(self.labelLayout, 0, 0)

        # Create a QHBoxLayout for the input field and the button
        self.inputLayout = QHBoxLayout()
        self.inputLayout.setSpacing(10)  # Set spacing between widgets in the layout

        self.Button_Send_Command = QPushButton(self.gridLayoutWidget)
        self.Button_Send_Command.setObjectName(u"Button_Send_Command")

        self.Line_Server_Console_Input = QLineEdit(self.gridLayoutWidget)
        self.Line_Server_Console_Input.setObjectName(u"Line_Server_Console_Input")
        # Set the size policy of Line_Server_Console_Input to Expanding
        self.Line_Server_Console_Input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Add the Line_Server_Console_Input and Button_Send_Command to the layout
        self.inputLayout.addWidget(self.Line_Server_Console_Input)
        self.inputLayout.addWidget(self.Button_Send_Command)

        self.Server_Console = QTextEdit(self.gridLayoutWidget)
        self.Server_Console.setObjectName(u"Server_Console")
        # Add the Server_Console to the grid layout with a column span of 2
        self.gridLayout.addWidget(self.Server_Console, 2, 0, 1, 2)  # Span 2 columns

        # Create a QHBoxLayout for the buttons
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(10)  # Set spacing between widgets in the layout

        # Add the input layout to the grid layout
        self.gridLayout.addLayout(self.inputLayout, 3, 0)  # Adjusted the row index to 3

        # Then add the buttons
        self.Button_Start_Server = QPushButton("Start Server")
        self.buttonLayout.addWidget(self.Button_Start_Server)
        self.Button_Start_Server.clicked.connect(self.start_server)

        self.Button_Restart_Server = QPushButton("Restart Server")
        self.buttonLayout.addWidget(self.Button_Restart_Server)

        self.Button_StopServer = QPushButton("Stop Server")
        self.buttonLayout.addWidget(self.Button_StopServer)

        self.Button_Kill_Server = QPushButton("Kill Server")
        self.buttonLayout.addWidget(self.Button_Kill_Server)

        # Add the button layout to the grid layout
        self.gridLayout.addLayout(self.buttonLayout, 1, 0)  # Adjusted the row index to 1

        # Create a QHBoxLayout for the input field and the button
        self.inputLayout = QHBoxLayout()
        self.inputLayout.setSpacing(10)  # Set spacing between widgets in the layout

        self.inputLayout.addWidget(self.Line_Server_Console_Input)
        self.inputLayout.addWidget(self.Button_Send_Command)

        # Add the input layout to the grid layout
        self.gridLayout.addLayout(self.inputLayout, 3, 0)  # Adjusted the row index to 3

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1126, 22))
        self.menuGeneral = QMenu(self.menubar)
        self.menuGeneral.setObjectName(u"menuGeneral")
        self.menuProperties = QMenu(self.menubar)
        self.menuProperties.setObjectName(u"menuProperties")
        self.menuPlugins = QMenu(self.menubar)
        self.menuPlugins.setObjectName(u"menuPlugins")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuGeneral.menuAction())
        self.menubar.addAction(self.menuProperties.menuAction())
        self.menubar.addAction(self.menuPlugins.menuAction())
        self.menuGeneral.addAction(self.actionOpen_config)
        self.menuGeneral.addSeparator()
        self.menuGeneral.addAction(self.actionOpen_EULA)
        self.menuGeneral.addAction(self.actionSelect_Server_jar)
        self.menuProperties.addAction(self.actionserver_properties)
        self.menuProperties.addAction(self.actionops_json)
        self.menuProperties.addSeparator()
        self.menuProperties.addAction(self.actionbanned_players_json)
        self.menuProperties.addAction(self.actionbanned_ips_json)
        self.menuPlugins.addAction(self.actionManage)
        self.menuPlugins.addAction(self.actionDownload)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen_EULA.setText(QCoreApplication.translate("MainWindow", u"Open EULA", None))
        self.actionSelect_Server_jar.setText(QCoreApplication.translate("MainWindow", u"Select Server JAR", None))
        self.actionManage.setText(QCoreApplication.translate("MainWindow", u"Manage", None))
        self.actionDownload.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.actionserver_properties.setText(QCoreApplication.translate("MainWindow", u"Server Setings", None))
        self.actionops_json.setText(QCoreApplication.translate("MainWindow", u"Operators", None))
        self.actionbanned_players_json.setText(QCoreApplication.translate("MainWindow", u"Banned Players", None))
        self.actionbanned_ips_json.setText(QCoreApplication.translate("MainWindow", u"Banned IPs", None))
        self.actioncommands_yml.setText(QCoreApplication.translate("MainWindow", u"commands.yml", None))
        self.actionOpen_config.setText(QCoreApplication.translate("MainWindow", u"Open manager config", None))
        self.Label_online.setText(QCoreApplication.translate("MainWindow", u"Online:", None))
        self.Button_Send_Command.setText(QCoreApplication.translate("MainWindow", u"Send Command", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Serves IP Adress: 127.0.0.1:25565", None))
        self.Button_Start_Server.setText(QCoreApplication.translate("MainWindow", u"Start Server", None))
        self.Button_Restart_Server.setText(QCoreApplication.translate("MainWindow", u"Restart Server", None))
        self.Button_StopServer.setText(QCoreApplication.translate("MainWindow", u"Stop Server", None))
        self.Button_Kill_Server.setText(QCoreApplication.translate("MainWindow", u"Kill Server", None))
        self.menuGeneral.setTitle(QCoreApplication.translate("MainWindow", u"General", None))
        self.menuProperties.setTitle(QCoreApplication.translate("MainWindow", u"Properties", None))
        self.menuPlugins.setTitle(QCoreApplication.translate("MainWindow", u"Plugins", None))

    # retranslateUi

    def select_server_jar(self):
        # Open a file dialog for selecting the Minecraft server JAR file
        file_dialog = QFileDialog()
        jar_file_path, _ = file_dialog.getOpenFileName(filter="JAR files (*.jar)")

        if jar_file_path:
            # Check if "ManagerSettings.json" exists
            if os.path.exists("ManagerSettings.json"):
                with open("ManagerSettings.json", "r") as json_file:
                    manager_settings = json.load(json_file)
            else:
                # If "ManagerSettings.json" does not exist, create it with default values
                manager_settings = {
                    "ram_gb": "4",
                    "server_jar": "server",
                    "server_dir": "server"
                }

            # Ensure the server directory exists
            os.makedirs(manager_settings["server_dir"], exist_ok=True)

            # Copy and rename the selected JAR file to "server.jar" in the specified directory
            shutil.copy(jar_file_path, os.path.join(manager_settings["server_dir"], "server.jar"))

            # Update "ManagerSettings.json" with the new server JAR file
            manager_settings["server_jar"] = "server.jar"

            with open("ManagerSettings.json", "w") as json_file:
                json.dump(manager_settings, json_file, indent=4)

    def close_editor(self):
        # Hide the EditFile widget, the SaveButton, and the CloseButton
        self.EditFile.hide()
        self.SaveButton.hide()
        self.CloseButton.hide()

    def start_server(self):
        # Load existing settings
        with open("ManagerSettings.json", "r") as json_file:
            manager_settings = json.load(json_file)

        server_dir = manager_settings["server_dir"]
        print(f"Absolute path to server.jar: {os.path.abspath(os.path.join(server_dir, 'server.jar'))}")

        print(
            f"Attempting to access server JAR at: {os.path.abspath(os.path.join(server_dir, 'server.jar'))}")  # Print the absolute path

        # Check if "server.jar" exists in the specified directory
        if not os.path.exists(os.path.join(server_dir, 'server.jar')):
            error_message = f"ERROR: Server jar not found in {server_dir}. Please select server JAR."

            # Add the error message to the Server_Console without line number
            self.Server_Console.append(error_message)
            return

        # Start the server
        command = ["java", "-Xmx" + manager_settings["ram_gb"] + "G", "-jar", "server.jar", "nogui"]
        process = subprocess.Popen(command, cwd=server_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # Start a thread to redirect the console output to Server_Console
        q = Queue()
        t = Thread(target=enqueue_output, args=(process.stdout, q))
        t.daemon = True
        t.start()

        # Start a QThread to continuously update Server_Console with the server's output
        self.output_thread = OutputThread(q)
        self.output_thread.signal.connect(self.Server_Console.append)
        self.output_thread.start()

        # Hide the EditFile widget and the SaveButton
        self.EditFile.hide()
        self.SaveButton.hide()

    def start_server_threaded(self):
        # Create a QThreadPool instance
        self.threadpool = QThreadPool()

        # Create a Worker instance with your start_server method
        worker = Worker(self.start_server)

        # Start the worker in a separate thread
        self.threadpool.start(worker)

    def open_eula(self):
        # Load existing settings
        with open("ManagerSettings.json", "r") as json_file:
            manager_settings = json.load(json_file)

        server_dir = manager_settings["server_dir"]
        eula_path = os.path.join(server_dir, 'eula.txt')

        # Open the EULA file and set the contents to the EditFile widget
        with open(eula_path, "r") as file:
            self.EditFile.setText(file.read())

        # Show the EditFile widget, the SaveButton, and the CloseButton
        self.EditFile.show()
        self.SaveButton.show()
        self.CloseButton.show()

    def save_file(self):
        # Load existing settings
        with open("ManagerSettings.json", "r") as json_file:
            manager_settings = json.load(json_file)

        server_dir = manager_settings["server_dir"]
        eula_path = os.path.join(server_dir, 'eula.txt')

        # Save the contents of the EditFile widget to the EULA file
        with open(eula_path, "w") as file:
            file.write(self.EditFile.toPlainText())

        # Show the CloseButton
        self.CloseButton.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create an instance of QApplication
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
