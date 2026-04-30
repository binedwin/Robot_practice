import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QDial
from PyQt6.QtCore import Qt

class DialApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Dial Example")

        vbox = QVBoxLayout()

        self.dial = QDial()
        self.dial.setRange(-360, 360)
        self.dial.valueChanged.connect(self.update_label)
        vbox.addWidget(self.dial)

        self.label = QLabel("0")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(self.label)

        self.setLayout(vbox)

    def update_label(self, value):
        self.label.setText(str(value))

def main():
    app =QApplication(sys.argv)
    window = DialApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()