import DobotEDU
import time
from pymodbus.client import ModbusTcpClient

# --- 설정 및 객체 초기화 ---
device = DobotEDU.dobot_magician
PORT = 'COM3' # 장치관리자에서 무조건 확인!

# Modbus 클라이언트 설정
MODBUS_IP = "192.168.110.102"
MODBUS_PORT = 5020
client = ModbusTcpClient(MODBUS_IP, port=MODBUS_PORT)

# --- 로봇 제어 함수 ---
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

def vacuum_off():
    device.set_endeffector_suctioncup(PORT, enable=False, on=False)
    time.sleep(2)
    print("진공 OFF")

def cmd_movej(j1, j2, j3, j4):
    device.set_ptpcmd(PORT, ptp_mode=4, x=j1, y=j2, z=j3, r=j4)
    print(f"비선형(관절) 이동 중: {j1}, {j2}, {j3}, {j4}")
    time.sleep(3) # [필수] 이동 시간 보장

def cmd_movel(x1, y1, z1, r1):
    device.set_ptpcmd(PORT, ptp_mode=2, x=x1, y=y1, z=z1, r=r1)
    print(f"선형(좌표) 이동 중: {x1}, {y1}, {z1}, {r1}")
    time.sleep(3) # [필수] 이동 시간 보장

def get_posj():
    p1 = device.get_pose(PORT)
    list_posj = [p1['jointAngle'][0], p1['jointAngle'][1], p1['jointAngle'][2], p1['jointAngle'][3]]
    print(f"저장된 관절 각도: {list_posj}")
    return list_posj

def value1(value):
    connect_robot()
    
    # 공통 동작 시작
    cmd_movej(56.45, 58.06, 51.98, -56.45)
    vacuum_on()
    cmd_movej(56.45, 58.06, 31.98, -56.45)
    cmd_movej(-0.0, 3.04, 13.71, 0.0)

    # 수신된 값에 따른 개별 동작 분기
    if value ==5:
        disconnect_robot()
    elif value == 1:
        cmd_movej(-60.32, 59.03, 44.74, 3.92)
        vacuum_off()
    elif value == 2:
        cmd_movej(-68.24, 52.6, 49.5, 3.92)
        vacuum_off()
    elif value == 3:
        cmd_movej(-77.0, 49.72, 53.44, 3.92)
        vacuum_off()
    elif value == 4:
        cmd_movej(-0.0, 3.04, 13.71, 0.0)
        vacuum_off()

    # 공통 동작 마무리
    vacuum_off()
    cmd_movej(-0.0, 3.04, 13.71, 0.0)

    disconnect_robot()
    return 99

# --- Modbus 통신 함수 ---
def get_sig(num):
    # 주의: 여기서 client.close()를 호출하지 않습니다. 나중에 기록해야 하기 때문입니다.
    result = client.read_holding_registers(address=num, count=1, slave=1)
    if result.isError():
        print(f"Modbus 레지스터 {num}번 읽기 에러 발생")
        return None
        
    val = result.registers[0]
    print(f"서버에서 읽어온 값은 : {val}")
    return val

def set_sig(num1, num2):
    client.write_register(address=num1, value=num2, slave=1)
    print(f"Modbus 서버 주소 {num1}번에 값 {num2} 저장 완료")


# --- 메인 실행 흐름 ---
def main():
    # 1. Modbus 서버 연결
    if not client.connect():
        print("Modbus 서버에 연결할 수 없습니다. IP 설정 및 서버 상태를 확인하세요.")
        return
    print("Modbus 서버 연결 성공")

    # 2. 서버의 6번 주소에서 값 읽기
    target_address = 6
    val = get_sig(target_address)

    # 3. 값이 1, 2, 3, 4 중 하나인지 확인하고 로봇 제어 시작
    if val in [1, 2, 3, 4]:
        print(f"수신된 명령({val})에 따라 로봇 동작을 시작합니다.")
        
        # 로봇 구동 함수 실행 후 반환값(99) 받기
        result_value = value1(val) 
        
        # 4. 동작이 무사히 끝나 99가 반환되면, 다시 서버의 6번 주소에 기록
        if result_value == 99:
            set_sig(target_address, result_value)
            print("모든 작업 시퀀스 완료. 서버에 99를 반환했습니다.")
            
    elif val is not None:
        print(f"수신된 값이 조건(1~4)에 맞지 않아 대기합니다. (현재 값: {val})")

    # 5. Modbus 클라이언트 종료
    client.close()

if __name__ == '__main__':
    main()