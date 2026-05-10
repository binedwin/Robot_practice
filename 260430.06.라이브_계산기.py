import sys
from PyQt6.QtWidgets import (
  QApplication, 
  QWidget, 
  QVBoxLayout,
  QPushButton,
  QLineEdit,
  QGridLayout
)

from PyQt6.QtCore import Qt


class Calculator(QWidget):
  def __init__(self):
    super().__init__()
    self.initUI()
  
  def initUI(self):
    self.setWindowTitle("계산기")

    #전체 레아웃 
    vbox = QVBoxLayout()

    #디스플레이
    self.display = QLineEdit()
    self.display.setReadOnly(True)
    self.display.setAlignment(Qt.AlignmentFlag.AlignRight) #우정렬
    self.display.setFixedHeight(50) #디스플레이 높이
    vbox.addWidget(self.display)

    #버튼 레이아웃
    grid = QGridLayout()

    buttons = [
      ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
      ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
      ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
      ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
    ]
    
    for (text, row, col) in buttons:
      button = QPushButton(text)
      button.setFixedSize(70, 70)
      button.clicked.connect(self.on_click)
      grid.addWidget(button, row, col)

    vbox.addLayout(grid)
    self.setLayout(vbox)
  
  def on_click(self):
    sender = self.sender()
    text = sender.text()

    if text == '=':
      try:
        result = str(eval(self.display.text()))
        self.display.setText(result)
      except Exception:
        self.display.setText("Error")
    elif text in {'+', '-', '*', '/'}:
      self.display.setText(self.display.text() + text + ' ')
    else:
      self.display.setText(self.display.text() + text)

def main():
  app = QApplication(sys.argv)
  window = Calculator()
  window.show()
  sys.exit(app.exec())

if __name__ == "__main__":
  main()