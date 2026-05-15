import sys
from PyQt6.QtWidgets import (
  QApplication,
  QWidget,
  QLabel,
  QPushButton,
  QVBoxLayout,
  QHBoxLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ImageApp(QWidget):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    #이미지 경로
    image_path = "sample.png"

    label = QLabel(self)
    #이미지 불러오기
    pixmap = QPixmap(image_path)

    if pixmap.isNull():
      label.setText("이미지를 불러올 수 없습니다.")
      label.setAlignment(Qt.AlignmentFlag.AlignCenter)
      self.resize(400, 200)
    else :
      label.setPixmap(pixmap)
      label.setAlignment(Qt.AlignmentFlag.AlignCenter)


    #메인 레이아웃
    vbox = QVBoxLayout()
    #Qlabel을 메인 레이아웃에 추가
    vbox.addWidget(label)
    #버튼 레이아웃 생성
    hbox = QHBoxLayout()

    #버튼 생성
    button1 = QPushButton("좋아요", self)
    button2 = QPushButton("싫어요", self)

    #버튼을 클릭했을 때 이벤트 연결
    button1.clicked.connect(self.like_clicked)
    button2.clicked.connect(self.dislike_clicked)

    hbox.addWidget(button1)
    hbox.addWidget(button2)
    #버튼의 레이아웃을 메인 레이아웃에 추가
    vbox.addLayout(hbox)

    #메인 레이아웃 설정
    self.setLayout(vbox)

    #창 크기를 조정
    if not pixmap.isNull():
      self.resize(pixmap.width(), pixmap.height() + 50)

    #창 제목 설정
    self.setWindowTitle("PyQt6 Image Viewer")

  def like_clicked(self):
    print("좋아요를 눌렀습니다.")

  def dislike_clicked(self):
    print("싫어요를 눌렀습니다.")

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = ImageApp()
  window.show()
  sys.exit(app.exec())
