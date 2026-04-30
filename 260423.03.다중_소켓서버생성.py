import socket
import threading

HOST = '192.168.27.51'
PORT = 20000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"[서버 시작] {HOST} : {PORT} 접속 대기중 입니다...")

# 클라이언트 처리 함수
def handle_client(client_socket, addr):
    print(f"[연결됨] {addr}")

    #msg = "Hello SSAFY_15th"
    #client_socket.send(msg.encode("utf-8"))

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode("utf-8")
            print(f"[{addr}] 수신된 메시지 : {message}")
    except Exception as e:
        print(f"[에러] {addr} : {e}")
    finally:
        client_socket.close()
        print(f"[연결 종료] {addr}")

# 여러 클라이언트 계속 받기
while True:
    client_socket, addr = server_socket.accept()

    # 클라이언트마다 스레드 생성
    client_thread = threading.Thread(
        target=handle_client,
        args=(client_socket, addr)
    )
    client_thread.start()