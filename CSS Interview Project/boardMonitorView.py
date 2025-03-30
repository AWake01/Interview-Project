import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QVBoxLayout

class BoardMonitorView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Board")

        self.layout = QVBoxLayout()
        self.btn = QPushButton()
        self.displayLbl = QLabel()

        self.layout.addWidget(self.btn)
        self.layout.addWidget(self.displayLbl)
        self.setLayout(self.layout)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = BoardMonitorView()
    window.show()
    app.exec_()