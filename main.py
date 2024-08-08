from PyQt5 import QtCore, QtGui, QtWidgets
from serial.tools import list_ports
import json
import os
import subprocess  # Import subprocess for running external scripts

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(494, 375)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(150, 100, 171, 61))
        self.startButton.setObjectName("startButton")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(51, 231, 65, 19))
        self.label.setObjectName("label")

        self.password = QtWidgets.QLabel(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(160, 231, 65, 19))
        self.password.setObjectName("password")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(36, 281, 96, 19))
        self.label_3.setObjectName("label_3")

        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(330, 281, 87, 27))
        self.saveButton.setObjectName("saveButton")

        self.passwordlineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.passwordlineEdit.setGeometry(QtCore.QRect(160, 281, 125, 27))
        self.passwordlineEdit.setObjectName("passwordlineEdit")
        self.passwordlineEdit.setMaxLength(3)  # Set the maximum length to 3 characters
        self.passwordlineEdit.setValidator(QtGui.QIntValidator(0, 999))  # Set the validator to accept numbers between 0 and 999

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 20, 16, 16))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("red-circle.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")

        self.portscomboBox = QtWidgets.QComboBox(self.centralwidget)
        self.portscomboBox.setGeometry(QtCore.QRect(59, 21, 81, 27))
        self.portscomboBox.setObjectName("portscomboBox")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Populate the portscomboBox with available serial ports
        self.populate_ports()

        # Connect the saveButton to the save_password function
        self.saveButton.clicked.connect(self.save_password)

        # Connect the startButton to the start_and_run function
        self.startButton.clicked.connect(self.start_and_run)
        self.subprocess_command = None

        # Connect the aboutToQuit signal to run the external script
        QtWidgets.QApplication.instance().aboutToQuit.connect(self.run_external_script)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.label.setText(_translate("MainWindow", "password"))
        with open('config.json') as f:
            d = json.load(f)
        self.password.setText(_translate("MainWindow", d["password"]))
        self.label_3.setText(_translate("MainWindow", "new password"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.portscomboBox.addItem(_translate("MainWindow", "------"))

    def populate_ports(self):
        self.portscomboBox.clear()  # Clear existing items
        ports = list_ports.comports()
        for port in ports:
            self.portscomboBox.addItem(port.device)

    def save_password(self):
    # Get the password from the line edit
        new_password = self.passwordlineEdit.text()
        if new_password:
            # Read existing JSON data
            try:
                with open('config.json', 'r') as json_file:
                    config_data = json.load(json_file)
            except FileNotFoundError:
                config_data = {}

            # Update the password in the JSON data
            config_data['password'] = new_password

            # Write the updated data back to the JSON file
            with open('config.json', 'w') as json_file:
                json.dump(config_data, json_file)

            # Update the password label
            self.password.setText(new_password)

    def start_and_run(self):
        # Get the selected port from the combo box
        selected_port = self.portscomboBox.currentText()
        if selected_port and selected_port != "------":
            # Read existing JSON data
            try:
                with open('config.json', 'r') as json_file:
                    config_data = json.load(json_file)
            except FileNotFoundError:
                config_data = {}

            # Update the port in the JSON data
            config_data['port'] = selected_port

            # Write the updated data back to the JSON file
            with open('config.json', 'w') as json_file:
                json.dump(config_data, json_file)

            # Run the external Python script
            subprocess.run(['python3', 'passwd_final.py'])

            # Exit the application
            QtWidgets.QApplication.quit()
            #sys.exit()

    def run_external_script(self):
        if self.subprocess_command:
            subprocess.run(self.subprocess_command)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
