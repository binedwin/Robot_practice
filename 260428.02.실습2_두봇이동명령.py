import DobotEDU
import time

PORT = 'COM3' #확인이 필요 합니다.
device = DobotEDU.dobot_magician
device.connect_dobot(PORT)
print(f"연결이 되었습니다.")
time.sleep(2)


def cmd_home():
    device.set_homecmd(PORT)
    time.sleep(2)

def cmd_movej():
    device.set_ptpcmd(PORT, ptp_mode = 4, x=-4.2, y=26, z=34, r=0)
    device.set_ptpcmd(PORT, ptp_mode = 4, x=-44.2, y=36, z=34, r=0)
    device.set_ptpcmd(PORT, ptp_mode = 4, x=-4.2, y=26, z=34, r=0)


#cmd_home()
time.sleep(1)
cmd_movej()

device.disconnect_dobot(PORT)
print(f"연결이 종료되었습니다.")

