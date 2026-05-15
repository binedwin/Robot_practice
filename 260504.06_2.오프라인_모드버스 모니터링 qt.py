import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QTimer
from pymodbus.client import ModbusTcpClient


class ModbusMonitor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Modbus Monitor")

        # Modbus 연결
        self.client = ModbusTcpClient("127.0.0.1", port=5020)
        self.client.connect()

        # 레이블 4개 생성
        self.labels = []
        main_layout = QVBoxLayout()
        row_layout = QHBoxLayout()

        for i in range(4):
            vbox = QVBoxLayout()

            title = QLabel(f"{i+11}번 값")
            value_label = QLabel("-----")

            self.labels.append(value_label)

            vbox.addWidget(title)
            vbox.addWidget(value_label)
            row_layout.addLayout(vbox)

        main_layout.addLayout(row_layout)
        self.setLayout(main_layout)

        # 타이머 (0.5초)
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_values)
        self.timer.start(500)

    def read_values(self):
        try:
            # 4개 레지스터 한 번에 읽기
            result = self.client.read_holding_registers(
                address=11, count=4, slave=1
            )

            if result and not result.isError():
                values = result.registers

                for i in range(4):
                    self.labels[i].setText(str(values[i]))
            else:
                for label in self.labels:
                    label.setText("읽기 오류")

        except Exception as e:
            for label in self.labels:
                label.setText(f"에러")

    def closeEvent(self, event):
        self.client.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModbusMonitor()
    window.show()
    sys.exit(app.exec())