import sys
from PyQt6.QtWidgets import (
  QApplication, 
  QWidget, 
  QPushButton, 
  QVBoxLayout
)


class ButtonApp(QWidget):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.setWindowTitle("Button Example")

    #메인 레이아웃
    vbox = QVBoxLayout()

    #버튼을 추가
    self.btn1 = QPushButton("Button 1")
    vbox.addWidget(self.btn1)

    self.btn2 = QPushButton("Button 2")
    vbox.addWidget(self.btn2)

    #전체 레아웃 설정
    self.setLayout(vbox)

def main():
  app = QApplication(sys.argv)
  window = ButtonApp()
  window.show()

  sys.exit(app.exec())

if __name__ == "__main__":
  main()