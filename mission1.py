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
    print("홈위치 이동완료 (약 15초 대기)")
    time.sleep(15) # 홈 이동 대기

def vacuum_on():
    device.set_endeffector_suctioncup(PORT, enable=True, on=True)
    time.sleep(2)
    print("진공 ON")

def vacuum_off(): # 오타 살짝 수정 (vacumm -> vacuum)
    device.set_endeffector_suctioncup(PORT, enable=False, on=False)
    time.sleep(2)
    print("진공 OFF")

def cmd_movej(j1, j2, j3, j4):
    device.set_ptpcmd(PORT, ptp_mode = 4, x = j1, y = j2, z = j3, r = j4)
    print(f"비선형(관절) 이동 중: {j1}, {j2}, {j3}, {j4}")
    time.sleep(3) # [필수] 이동 시간 보장

def cmd_movel(x1, y1, z1, r1):
    device.set_ptpcmd(PORT, ptp_mode = 2, x = x1, y = y1, z = z1, r = r1)
    print(f"선형(좌표) 이동 중: {x1}, {y1}, {z1}, {r1}")
    time.sleep(3) # [필수] 이동 시간 보장

def get_posj():
    p1 = device.get_pose(PORT)
    # 리스트에 관절 각도 4개를 담아 반환
    list_posj = [p1['jointAngle'][0], p1['jointAngle'][1], p1['jointAngle'][2], p1['jointAngle'][3]]
    print(f"저장된 관절 각도: {list_posj}")
    return list_posj

def main():
    connect_robot()
    
    # 1. 초기 위치(관절 각도) 저장
    k = get_posj()

    # 2. 다른 곳으로 이동
    cmd_movej(-0.0, 3.04, 13.71, 0.0)

    # 3. 저장해둔 원래 위치로 복귀
    # [핵심] 리스트 k 앞에 별표(*)를 붙이면 숫자 4개로 쪼개져서 j1, j2, j3, j4로 예쁘게 들어갑니다.
    print("원래 위치로 돌아갑니다.")
    cmd_movej(*k)
    vacuum_on()
    cmd_movej(-0.0, 3.04, 13.71, 0.0)
    cmd_movej(-60.32, 59.03, 44.74, 3.92)
    vacuum_off()

    # 4. 연결 해제
    disconnect_robot()


if __name__ == '__main__':
    main()