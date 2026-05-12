import DobotEDU
import time

PORT = 'COM3' #확인이 필요 합니다.
device = DobotEDU.dobot_magician

device.connect_dobot(PORT)
print(f"연결이 되었습니다.")
time.sleep(2)
#2초 후 홈위치로 이동
device.set_homecmd(PORT)
time.sleep(2)


device.disconnect_dobot(PORT)
print(f"연결이 종료되었습니다.")

