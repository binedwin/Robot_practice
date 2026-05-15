import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel
)
from PyQt6.QtCore import Qt


class AirconRemote(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("SSAFY 에어컨트롤러")
        self.setGeometry(100, 100, 300, 400)

        # 초기값 설정
        self.temperature = 23
        self.setting_temperature = 24
        self.modes = ["냉방", "제습", "난방", "송풍"]
        self.current_mode_index = 0
        self.fan_speeds = ["미풍", "약풍", "중풍", "강풍"]
        self.current_fan_speeds_index = 1
        self.powered_on = False

        vbox = QVBoxLayout()

        self.current_temp_label = QLabel("현재 온도 : 23")
        self.current_temp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(self.current_temp_label)

        self.setting_temp_label = QLabel("설정 온도 : 24")
        self.setting_temp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(self.setting_temp_label)

        temp_control_layout = QHBoxLayout()

        self.temp_up_btn = QPushButton("온도 +")
        self.temp_down_btn = QPushButton("온도 -")

        self.temp_up_btn.clicked.connect(self.increase_temp)
        self.temp_down_btn.clicked.connect(self.decrease_temp)

        temp_control_layout.addWidget(self.temp_up_btn)
        temp_control_layout.addWidget(self.temp_down_btn)

        vbox.addLayout(temp_control_layout)

        self.power_btn = QPushButton("Power OFF")
        self.power_btn.clicked.connect(self.toggle_power)
        vbox.addWidget(self.power_btn)

        self.mode_label = QLabel("Mode : 냉방")
        self.mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(self.mode_label)

        self.mode_btn = QPushButton("Change Mode")
        self.mode_btn.clicked.connect(self.change_mode)
        vbox.addWidget(self.mode_btn)

        self.fan_speed_label = QLabel("팬 속도 : 약풍")
        self.fan_speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(self.fan_speed_label)

        self.fan_speed_btn = QPushButton("Fan Speed")
        self.fan_speed_btn.clicked.connect(self.change_fan_speed)
        vbox.addWidget(self.fan_speed_btn)

        self.setLayout(vbox)

    def increase_temp(self):
        if self.powered_on:
            self.setting_temperature += 1
            self.setting_temp_label.setText(f"설정 온도 : {self.setting_temperature}")

    def decrease_temp(self):
        if self.powered_on:
            self.setting_temperature -= 1
            self.setting_temp_label.setText(f"설정 온도 : {self.setting_temperature}")

    def toggle_power(self):
        self.powered_on = not self.powered_on

        if self.powered_on:
            self.power_btn.setText("Power ON")
        else:
            self.power_btn.setText("Power OFF")

    def change_mode(self):
        if self.powered_on:
            self.current_mode_index = (self.current_mode_index + 1) % len(self.modes)
            self.mode_label.setText(f"Mode : {self.modes[self.current_mode_index]}")

    def change_fan_speed(self):
        if self.powered_on:
            self.current_fan_speeds_index = (
                self.current_fan_speeds_index + 1
            ) % len(self.fan_speeds)

            self.fan_speed_label.setText(
                f"팬 속도 : {self.fan_speeds[self.current_fan_speeds_index]}"
            )


def main():
    app = QApplication(sys.argv)
    remote = AirconRemote()
    remote.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()