import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtGui import QPainter, QPen, QImage
from PyQt6.QtCore import Qt, QPoint

class DrwaingBoard(QWidget):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("그림판")
    self.setFixedSize(800, 600)

    #캔버스 생성
    self.image = QImage(self.size(), QImage.Format.Format_RGB32)
    self.image.fill(Qt.GlobalColor.white)

    self.last_point = QPoint()

  def mousePressEvent(self, event):
    if event.button() == Qt.MouseButton.LeftButton:
      self.last_point = event.position().toPoint()

  def mouseMoveEvent(self, event):
    if event.buttons() == Qt.MouseButton.LeftButton:
      painter = QPainter(self.image)

      pen = QPen(
        Qt.GlobalColor.black, 3,
        Qt.PenStyle.SolidLine,
        Qt.PenCapStyle.RoundCap,
        Qt.PenJoinStyle.RoundJoin
      )
      painter.setPen(pen)
      painter.drawLine(self.last_point, event.position().toPoint())

      self.last_point = event.position().toPoint()
      self.update()

  def paintEvent(self, event):
    canvas_painter = QPainter(self)
    canvas_painter.drawImage(self.rect(), self.image, self.image.rect())


class MainWindow(QWidget):
  def __init__(self):
    super().__init__()

    layout = QVBoxLayout()
    self.board = DrwaingBoard()

    layout.addWidget(self.board)
    self.setLayout(layout)

    self.setWindowTitle("PyQt6 그림판입니다.")


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())
