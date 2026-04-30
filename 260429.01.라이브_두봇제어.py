import DobotEDU

device = DobotEDU.dobot_magician
PORT ='COM5'

def connect_robot():
    device.connect_dobot(PORT)
    time.sleep(1)
    print("로봇연결 완료")

def disconnect_robot():
    device.disconnect_dobot(PORT)
    time.sleep(1)
    print("로봇해제 완료")

def cmd_home():
    device.set_homecmd(PORT)
    print(f"홈위치 이동완료")
    # 홈으로 이동하는 명령어
    # 매번 할 필요없고
    # 충돌로 위치가 틀어졌을 경우
    # 처음 전원을 켜는 경우

def vacuum_on():
    device.set_endeffector_suctionup(PORT, enable= True, on= True)
    time.sleep(2) #진공이 완성되기 까지 걸리는 시간을 줘야함
    print("진공 on")

def vaccum_off():
    device.set_endeffector_suctionup(PORT, enable= False, on= False)
    time.sleep(2) #진공이 떨어지는 순간까지 걸리는 시간을 줘야함
    print("진공 off")

def vaccum_work(num):
    if num =='ON':
        vacuum_on()
    elif num == 'OFF':
        vaccum_off()

def cmd_movej(p1, p2, p3, p4):
    device.set_ptpcmd(PORT, ptp_mode =4, x=p1, y=p2, z=p3, r=p4)
    print("이동완료")

def cmd_movel(x1, y1. z1, r1):
    device.set_ptpcmd(PORT, ptp_mode =2, x=x1, y=y1, z=z1, r=r1)
    print("이동완료")

def cmd_jump1(x1, y1, z1, r1):
    device.set_ptpcmd(PORT, ptp_mode=0, x=x1, y=y1, z=z1, r=r1)
    print("점프 모션 이동완료")


def cmd_movej_rel(p1, p2, p3, p4):
    device.set_ptpcmd(PORT, ptp_mode =6, x=p1, y=p2, z=p3, r=p4)
    print("비선형 상대위치 이동완료")
    # 현재 위치를 기준으로 얼마나 joint(관절각도)만큼 이동할건지 넣으면된다..

def cmd_movel_rel(x1, y1. z1, r1):
    device.set_ptpcmd(PORT, ptp_mode =7, x=x1, y=y1, z=z1, r=r1)
    print("선형 상대위치 이동완료")
    # 현재 위치를 기준으로 얼마나 task(mm단위)만큼 이동할건지 넣으면된다..

def get_posj():
    p1 = device.get_pose(PORT) # 
    print(p1)

def get_posx():
    p1 = device.get_pose(PORT)
    print(p1)

