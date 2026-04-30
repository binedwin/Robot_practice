import socket

HOST = '127.0.0.1'
PORT = 20000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#서버로 접속
client_socket.connect((HOST, PORT))
print(f"서버에 접속을 완료하였습니다. 서버주소는 {HOST} : {PORT}")

intro_msg = client_socket.recv(1024).decode('utf-8')
print(f"서버 인사말: {intro_msg}")

try:
  while True:
    #키보드로 메시지를 입력
    message = input("메시지를 입력하세요")
    if message.lower() == 'exit':
      break
    #메시지 전송
    client_socket.send(message.encode('utf-8'))
    data = client_socket.recv(1024)
    
    if not data:
      print("서버 연결이 종료되었습니다!")
      break

    response = data.decode('utf-8')
    print(f"서버 메시지 : {response}")
except KeyboardInterrupt:
  print("강제로 종료되었습니다.")
finally:
  #연결종료
  client_socket.close()
  print("서버종료")
