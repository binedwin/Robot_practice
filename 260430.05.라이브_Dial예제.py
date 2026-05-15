import sys
from PyQt6.QtWidgets import (
  QApplication, 
  QWidget, 
  QVBoxLayout,
  QLabel,
  QDial
)

from PyQt6.QtCore import Qt

class DialApp(QWidget):
  def __init__(self):
    super().__init__()
    self.initUI()
  
  def initUI(self):
    self.setWindowTitle("Dial Example")

    #Main 레이아웃
    vbox = QVBoxLayout()

    #Dial add
    self.dial = QDial()
    self.dial.setRange(-3600, 3600)
    self.dial.valueChanged.connect(self.update_label)
    vbox.addWidget(self.dial)

    #Label= 디스플레이
    self.label = QLabel("0")
    self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    vbox.addWidget(self.label)

    #레이아웃 설정
    self.setLayout(vbox)

  def update_label(self, value):
    self.label.setText(str(value))

def main():
  app = QApplication(sys.argv)
  window = DialApp()
  window.show()
  sys.exit(app.exec())

if __name__ == "__main__":
  main()