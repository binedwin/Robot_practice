import sys
from PyQt6.QtWidgets import (
  QApplication, 
  QWidget, 
  QCheckBox, 
  QPushButton, 
  QVBoxLayout, 
  QHBoxLayout
)


class Mainwindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Check Box Example")

        # 메인 레이아웃 (세로)
        vbox = QVBoxLayout()

        # 첫 번째 줄
        hbox1 = QHBoxLayout()

        self.cb1_1 = QCheckBox("1")
        self.cb1_2 = QCheckBox("2")
        self.cb1_3 = QCheckBox("3")

        hbox1.addWidget(self.cb1_1)
        hbox1.addWidget(self.cb1_2)
        hbox1.addWidget(self.cb1_3)

        vbox.addLayout(hbox1)

        # 두 번째 줄
        hbox2 = QHBoxLayout()

        self.cb2_1 = QCheckBox("4")
        self.cb2_2 = QCheckBox("5")
        self.cb2_3 = QCheckBox("6")

        hbox2.addWidget(self.cb2_1)
        hbox2.addWidget(self.cb2_2)
        hbox2.addWidget(self.cb2_3)

        vbox.addLayout(hbox2)

        # 버튼 생성
        self.btn = QPushButton("출력")
        self.btn.clicked.connect(self.print_checked)

        vbox.addWidget(self.btn)

        # 전체 레이아웃 설정
        self.setLayout(vbox)

    def print_checked(self):
        check_values = []

        if self.cb1_1.isChecked():
            check_values.append(self.cb1_1.text())

        if self.cb1_2.isChecked():
            check_values.append(self.cb1_2.text())

        if self.cb1_3.isChecked():
            check_values.append(self.cb1_3.text())

        if self.cb2_1.isChecked():
            check_values.append(self.cb2_1.text())

        if self.cb2_2.isChecked():
            check_values.append(self.cb2_2.text())

        if self.cb2_3.isChecked():
            check_values.append(self.cb2_3.text())

        print("체크된 값은 ...", check_values)


def main():
    app = QApplication(sys.argv)

    window = Mainwindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()