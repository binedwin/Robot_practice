import socket
#소켓 기본 라이브러리 가져오기

HOST = '127.0.0.1' #내부 IP
PORT = 20000 #8000번 이하? 포트는 예약되어있는 경우가 많음.

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#AF_INET = IPv4 사용 #SOCK_STREAM = 소켓 스트림 생성

#생성한 소켓을 IP랑 PORT BIND 처리
server_socket .bind((HOST, PORT))
#듣기 시작
server_socket.listen()

print(f"[서버 시작] {HOST} : {PORT} 접속 대기중 입니다...")

#만약 클라이언트가 나의 서버로 접속하면 잡기
client_socket, addr = server_socket.accept()
print(f"클라이언트가 접속되었습니다. 주소는 : {addr}")

msg = "Hello SSAFY_15th"
#문자열데이터를 바이너리 타입으로 인코딩을 해서 UTF-8 규격으로 전송
client_socket.send(msg.encode("utf-8"))

while True:
  data = client_socket.recv(1024)
  if not data:
    break
  message = data.decode("utf-8")
  print(f"수신된 메시지 : {message}")
  
  response = f"서버가 확인했습니다: {message}"
  client_socket.send(response.encode("utf-8"))

client_socket.close()
server_socket.close()
print(f"서버가 종료되었습니다.")

  

