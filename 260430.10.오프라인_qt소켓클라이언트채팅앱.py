import sys
import socket
import threading
from PyQt6.QtWidgets import (
  QApplication,
  QWidget,
  QTextEdit,
  QLineEdit,
  QPushButton,
  QVBoxLayout,
  QHBoxLayout
)
from PyQt6.QtCore import pyqtSignal, QObject

class Communicate(QObject):
  update_chat = pyqtSignal(str)

class ChatClient(QWidget):
  def __init__(self, host="127.0.0.1", port = 20000):
    super().__init__()

    self.host = host
    self.port = port
    self.sock = None

    self.initUI()

    self.comm = Communicate()
    self.comm.update_chat.connect(self.updateChat)

    self.startClient()

  def initUI(self):
    self.setWindowTitle("채팅 클라이언트")

    self.chat_display = QTextEdit()
    self.chat_display.setReadOnly(True)

    self.message_input = QLineEdit()
    self.message_input.returnPressed.connect(self.sendMessage)

    self.send_button = QPushButton("전송")
    self.send_button.clicked.connect(self.sendMessage)

    self.exit_button = QPushButton("채팅창 종료")
    self.exit_button.clicked.connect(self.closeApp)

    hbox = QHBoxLayout()
    hbox.addWidget(self.send_button)
    hbox.addWidget(self.exit_button)

    vbox = QVBoxLayout()
    vbox.addWidget(self.chat_display)
    vbox.addWidget(self.message_input)
    
    vbox.addLayout(hbox)

    self.setLayout(vbox)
    self.resize(800, 600)

  def startClient(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
      self.sock.connect((self.host, self.port))
      threading.Thread(target=self.receiveMessages, daemon=True).start()
      #스레드 처리 안하면, recv()여기서 무한대기하면서 버튼입력 ..모든 작동이 멈춤
      self.comm.update_chat.emit("[서버가 연결되었습니다.]")

    except Exception as e:
      self.comm.update_chat.emit(f"[연결 실패] {e}")

  def receiveMessages(self):
    while True:
      try:
        data = self.sock.recv(1024)
        if not data:
          break
        message = data.decode("utf-8")
        self.comm.update_chat.emit(f"[서버메시지] {message}")
      except :
        break
  def sendMessage(self):
    message = self.message_input.text().strip()

    if message:
      self.chat_display.append(f"[나] {message}")

      try:
        self.sock.send(message.encode("utf-8"))
      except:
        self.chat_display.append("[전송 실패] 서버와 연결이 끊어짐")
        return
      self.message_input.clear()

      if message.lower() == "exit":
        self.closeApp()
  def updateChat(self, message):
    self.chat_display.append(message)

  def closeApp(self):
    try:
      self.sock.send("exit".encode("utf-8"))
      self.sock.close()
    except:
      pass
    self.close()
  
if __name__ == "__main__":
  app = QApplication(sys.argv)
  client = ChatClient()
  client.show()
  sys.exit(app.exec())