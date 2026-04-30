import DobotEDU
import time

device = DobotEDU.dobot_magician
PORT = 'COM3' #장치관리자에서 무조건 확인!


def connect_robot():
  device.connect_dobot(PORT)
  time.sleep(1)
  print("로봇 연결이 완료되었습니다.")

def disconnect_robot():
  device.disconnect_dobot(PORT)
  time.sleep(1)
  print("로봇 연결이 해제되었습니다")


def cmd_home(): 
  device.set_homecmd(PORT)
  print(f"홈위치 이동완료")
  #홈으로 이동하는 명령어
  #매번 할 필요는 없습니다.
  #충돌로 위치가 틀어졌을 경우
  #처음 전원을 켜는 경우

def vacuum_on():
  device.set_endeffector_suctioncup(PORT, enable=True, on=True)
  time.sleep(2) #진공이 완성되기까지 걸리는 시간
  print("진공 ON")

def vacuum_off():
  device.set_endeffector_suctioncup(PORT, enable=False, on=False)
  time.sleep(2)
  print("진공 OFF")

def vacuum_work(num):
  if num == 'ON':
    vacuum_on()
  elif num == 'OFF':
    vacuum_off()

def cmd_movej(j1, j2, j3, j4):
  device.set_ptpcmd(PORT, ptp_mode = 4, x = j1, y = j2, z = j3, r = j4)
  print("비선형 모션 이동완료")

def cmd_movel(x1, y1, z1, r1):
  device.set_ptpcmd(PORT, ptp_mode = 2, x = x1, y = y1, z = z1, r = r1)
  print("선형 모션 이동완료")



def main():
    connect_robot()
    cmd_home()
    cmd_movej(56.45, 58.06, 51.98, -56.45)
    p1=device.get_pose(PORT)
    print(p1)
    vacuum_on()
    cmd_movej(56.45, 58.06, 31.98, -56.45)
    cmd_movej(-60.32, 59.03, 44.74, 3.92)
    vacuum_off()
    disconnect_robot()

if __name__ == '__main__':
  main()
