#view.py

from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
import sys

#View uses python command line console input
class BoardView:
    def __init__(self):
        self.controller = None

        self.app = QApplication(sys.argv)
        self.window = QWidget()

        self.layout = QVBoxLayout()
        self.window.setWindowTitle("View")

        self.promptTxtLn = QLineEdit()
        self.sendBtn = QPushButton("Send command")
        self.sendBtn.clicked.connect(self.send_input)
        self.responseTxtLb = QLabel()

        self.layout.addWidget(self.promptTxtLn)
        self.layout.addWidget(self.sendBtn)
        self.layout.addWidget(self.responseTxtLb)

        self.window.setLayout(self.layout)

    def send_input(self):
        userInput = self.promptTxtLn.text()
        output = self.controller.receive_input(userInput)
        self.__show_output(output)

    #Loop to prompt for input from user and write output to console. X can be used to exit the program.
    def read_input_start(self):
        print("\nSTART - Enter E, I, O or P commands, or X to exit...")
        while True:
            #print(input)
            userInput = input("$: ")
            if userInput == "X":            #End program
                print("CLOSE")
                exit()
            output = self.controller.receive_input(userInput)
            self.__write_output(output)

    #Display controller reply to user
    def __write_output(self, output):
        print(f"OUt: {output}")

    #Show output
    def __show_output(self, output):
        #print(f"OUt: {output}")
        self.responseTxtLb.setText(output)

#ontroller = BoardController(BoardModel)
view = BoardView()
