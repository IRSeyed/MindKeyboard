import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QMessageBox, QDesktopWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from NeuroPy import NeuroPy
import serial
import time ,json
   


class VirtualKeyboard(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.correct_password = self.read_password()
        self.user_input = ""
        self.last_key = None
        self.password_attempts = 0
        self.index = 0
        self.att_values = []
        self.current_password = ""
        self.scan_columns = True
        
        self.clms_cntr = 0
        self.row_p = 0
        self.scroll = 0

    def init_ui(self):
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Password")
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.setLayout(self.grid_layout)
        self.setStyleSheet("background-color: white;")
        

        self.display = QLineEdit()
        self.grid_layout.addWidget(self.display, 0, 0, 1, 3)

        self.keys = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['Delete']
        ]

        self.buttons = {}
        for i, row in enumerate(self.keys):
            for j, key in enumerate(row):
                button = QPushButton(key)
                button.setStyleSheet('font-size: 24px; border: none; background-color: white;')
                button.setFixedSize(100, 100)
                self.buttons[key] = button
                self.grid_layout.addWidget(button, i + 1, j, 1, 1)

        self.buttons['Delete'].setStyleSheet('background-color: white; font-size: 24px; border: none;')
        self.grid_layout.addWidget(self.buttons['Delete'], 1, 3, 3, 1)
        self.buttons['Delete'].clicked.connect(self.clear_display)

    def read_password(self):
        try:
            with open('config.json') as f:
                d = json.load(f)
                password = d["password"]
                print(password)
                print(type(password))
                if len(password) != 3 or not password.isdigit():
                    raise ValueError("Password should be 3 digits.")
                return password
        except FileNotFoundError:
            print("Password file not found.")
            sys.exit(1)
        except ValueError as e:
            print(f"Error reading password: {e}")
            sys.exit(1)

    def automate_input(self):
        
        self.clear_buttons()
                
        #self.current_password = "2568"  # Use it for Delete Button test with 4 digits
        self.current_password = ""  # Reset the current password

        while True:
            self.scan_columns_logic()
            QApplication.processEvents()  # Allow the GUI to update
        
        self.clear_display()



    def scan_columns_logic(self):
        # Simulate logic for column scanning
        self.att_values = []
        columns = [['1', '4', '7'], ['2', '5', '8'], ['3', '6', '9'], ['Delete', 'Delete', 'Delete']]
        #att = 65  # Replace with actual 'att' assignment
        self.clms_cntr = 0
        self.scroll = 0
        start_time = time.time()
        if (len(self.current_password) == 3):
            self.check_password()
        while (self.clms_cntr < 4):
            # Simulate logic to process each column
            for i in range(3):
                self.buttons[columns[self.clms_cntr][i]].setStyleSheet('background-color: rgb(0,255,67); font-size: 24px; border: none;')
                QApplication.processEvents()
            print("column start", start_time)
            self.att_values = []
            start_time = time.time()
            while time.time() - start_time < 10:
                print("column",time.time() - start_time)
                print(att)
                if (att >= 60):
                    self.att_values.append(1)  
                else :
                    self.att_values.append(0)
                
                if (len(self.att_values) > 10) :
                    self.att_values.pop(0)
                    
                if ((sum(self.att_values)) == 10):
                    if self.clms_cntr == 3:
                        self.delete_num()
                    else :
                        self.scan_rows_logic(self.clms_cntr)
                    for i in range(3):
                        self.buttons[columns[self.clms_cntr][i]].setStyleSheet('background-color: white; font-size: 24px; border: none;')
                        QApplication.processEvents()
                    self.att_values = []
                    break
                time.sleep(0.5)  # Adjust timing between columns
                QApplication.processEvents()
            for i in range(3):
                self.buttons[columns[self.clms_cntr][i]].setStyleSheet('background-color: white; font-size: 24px; border: none;')
                QApplication.processEvents()
            if(self.scroll > 0):
                break
            self.clms_cntr = self.clms_cntr + 1

        return False  # Return False if column scanning fails

    def scan_rows_logic(self, cntr1):
        # Simulate logic for row scanning
        rows = [['1', '4', '7'], ['2', '5', '8'], ['3', '6', '9']]
        self.att_values = []
        #att = 0  # Replace with actual 'att' assignment
        self.row_p = 0
        self.scroll = 0
        
        """if cntr1 == 2 :         #Use it when you want to test the scroll forward
            att = 65"""
        
        if (len(self.current_password) == 3):
            self.check_password()
        for srl in range(3):
                self.buttons[rows[cntr1][srl]].setStyleSheet('background-color: white; font-size: 24px; border: none;')
                QApplication.processEvents()
        while (self.row_p < 3):
            # Simulate logic to process each column
            #if cntr1 == 2 and self.row_p == 2:         #Use it when you want to test the scroll forward
            #    att = 65
            self.att_values = []
            start_time = time.time()
            print("row start:",start_time)
            while time.time() - start_time < 10:
                print("row", time.time() - start_time)
                QApplication.processEvents()
                self.buttons[rows[cntr1][self.row_p]].setStyleSheet('background-color: rgb(0,255,67); font-size: 24px; border: none;')
                print(att)
                if (att >= 60):
                    self.att_values.append(1)  
                else :
                    self.att_values.append(0)
                
                if (len(self.att_values) > 10) :
                    self.att_values.pop(0)
                    
                if ((sum(self.att_values)) == 10):
                    self.update_password(rows[cntr1][self.row_p])
                    self.att_values = []
                    self.buttons[rows[cntr1][self.row_p]].setStyleSheet('background-color: white; font-size: 24px; border: none;')
                    QApplication.processEvents()
                    #self.Call_function()
                    break
                time.sleep(0.5)  # Adjust timing between rows
            self.buttons[rows[cntr1][self.row_p]].setStyleSheet('background-color: white; font-size: 24px; border: none;')
            QApplication.processEvents()
            if(self.scroll > 0):
                break
            self.row_p = self.row_p + 1

        return False  # Return False if column scanning fails

    def check_password(self):
        if len(self.current_password) == 3:
            print("current pass:", type(self.current_password))
            if self.current_password == self.correct_password:
                self.Call_function()
                self.current_password = ""
                self.update_password(self.current_password)
                self.update_display(self.current_password)
                self.clear_buttons()
            else:
                self.current_password = ""
                self.show_password_incorrect_alert()
                self.update_password(self.current_password)
                self.update_display(self.current_password)
                self.clear_buttons()

    def clear_display(self):
        self.display.clear()
        self.user_input = ""
        self.last_key = None
        self.current_password = None

    def Call_function(self):
        print("Password is Correct!")
        self.clear_buttons()
        time.sleep(20)

        
    def update_password(self, passwd):
        self.current_password = self.current_password + passwd # Update password with the last digit only
        self.update_display(self.current_password)
        self.clear_buttons()
        self.clms_cntr = 0
        self.row_p = 0
        self.scroll = 1
         
    def update_display(self, message):
        # Update the GUI display here
        self.display.setText(message)

    def closeEvent(self, event):
        # Stop the timer when the window is closed
        self.timer.stop()
        event.accept()
        
    def delete_num(self):
        if (len(self.current_password) > 0):
            self.current_password = self.current_password[:-1]
            self.update_display(self.current_password)
            #self.clms_cntr = None
        else :
            self.current_password = ""
            #self.clms_cntr = None
            
    def clear_buttons(self):
        columns = [['1', '4', '7'], ['2', '5', '8'], ['3', '6', '9'], ['Delete', 'Delete', 'Delete']]
        
        for ind in range(4):
            for dnd in range(3):
                self.buttons[columns[ind][dnd]].setStyleSheet('background-color: white; font-size: 24px; border: none;')
                QApplication.processEvents()
        
            
    def show_password_incorrect_alert(self):
        alert = QMessageBox()
        alert.setIcon(QMessageBox.Warning)
        alert.setWindowTitle("Incorrect Password")
        alert.setStandardButtons(QMessageBox.NoButton)  # Hide buttons
        alert.setText("Password is Incorrect!")
        
        alert.show()
        QApplication.processEvents()
        time.sleep(10)
        alert.hide()



if __name__ == '__main__':
    with open('config.json') as f:
        d = json.load(f)
        port = d["port"]
    mw = NeuroPy(port)
    #arduino = serial.Serial('/dev/ttyUSB0', 9600)
    global att
    att = 0
    mw.start()
    mw.setCallBack('attention', lambda x: exec(f"global att; att = {x}"))
    time.sleep(10)
    app = QApplication(sys.argv)
    window = VirtualKeyboard()
    window.show()
    window.automate_input()
    sys.exit(app.exec_())
