import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def initUI(self):
        self.setWindowTitle("checkbox")

    vbox = QVBoxLayout()

    self.ch1_1 = QCheckBox("1")
    self.ch1_2 = QCheckBox("2")
    self.ch1_3 = QCheckBox("3")

    hbox.addWidget(self.ch1_1)
    hbox.addWidget(self.ch1_2)
    hbox.addWidget(self.ch1_3)

    vbox.addWidget(hbox)
    
    hbox = QHBoxLayout()

    self.ch1_1 = QCheckBox("4")
    self.ch1_2 = QCheckBox("5")
    self.ch1_3 = QCheckBox("6")

    hbox.addWidget(self.ch2_1)
    hbox.addWidget(self.ch2_2)
    hbox.addWidget(self.ch2_3)

    vbox.addLayout(hbox)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())