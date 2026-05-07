import cv2
import mediapipe as mp
import numpy as np
import time
import threading
import asyncio

# -----------------------------------
# 전역 변수 및 공유 데이터
# -----------------------------------
latest_x = None  # 손목의 X 좌표 (0~1)
latest_y = None  # 손목의 Y 좌표 (0~1)
latest_fingers = 0 # 펴진 손가락 개수
robot_running = True
lock = threading.Lock()

PORT = "COM3"

# -----------------------------------
# 좌표 매핑 (화면 비율 -> 안전한 각도 제한)
# -----------------------------------
def map_value(x, in_min, in_max, out_min, out_max):
    return out_min + (x - in_min) * (out_max - out_min) / (in_max - in_min + 1e-9)

# -----------------------------------
# 🔥 로봇 제어 스레드 (PTP Mode 4 절대 각도 제어)
# -----------------------------------
def robot_worker():
    global latest_x, latest_y, latest_fingers, robot_running

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    import DobotEDU
    device = DobotEDU.dobot_magician

    print("[Robot] Connecting...")
    try:
        device.connect_dobot(PORT)
        time.sleep(2)
        print("[Robot] 홈 위치로 이동 중... (15초 대기)")
        device.set_homecmd(PORT)
        time.sleep(15) 
        print("[Robot] READY ✔")
    except Exception as e:
        print(f"[Robot] Connection Error: {e}")
        return

    # 🔥 핵심 튜닝 값: 손이 '3도' 이상 변했을 때만 명령 전송 (버퍼 폭주 방지)
    # 로봇이 한 박자 늦게 따라온다면 이 값을 5.0 정도로 높이세요.
    THRESHOLD_DEGREE = 3.0   
    last_sent_angle = -999    # 마지막으로 전송한 각도 기록용
    last_fingers = -1         # 손가락 개수 변경 감지용
    vacuum_state = False      # 진공 펌프 현재 상태

    while robot_running:
        target_x, target_y, fingers = None, None, 0
        
        with lock:
            target_x = latest_x
            target_y = latest_y
            fingers = latest_fingers

        if target_x is not None and target_y is not None:
            try:
                # 💡 손가락 개수(모드)가 바뀌면 이전 각도 기록을 초기화
                if fingers != last_fingers:
                    last_sent_angle = -999
                    last_fingers = fingers
                    print(f"\n[Mode Change] 손가락 {fingers}개 인식됨")

                # --------------------------------------
                # 1. 펌프 제어 (0개: 주먹 ON, 5개: 보자기 OFF)
                # --------------------------------------
                if fingers == 0:
                    if not vacuum_state:
                        device.set_endeffector_suctioncup(PORT, True, True)
                        vacuum_state = True
                        print("[Vacuum] ✊ 주먹 감지 -> 진공 펌프 ON")
                elif fingers == 5:
                    if vacuum_state:
                        device.set_endeffector_suctioncup(PORT, False, False)
                        vacuum_state = False
                        print("[Vacuum] 🖐 보자기 감지 -> 진공 펌프 OFF")

                # --------------------------------------
                # 2. 다관절 독립 절대 제어 (Move J - ptp_mode=4)
                # --------------------------------------
                elif 1 <= fingers <= 4:
                    # 현재 로봇의 4개 관절 각도를 모두 읽어옵니다.
                    pose = device.get_pose(PORT)
                    if not pose or 'jointAngle' not in pose:
                        continue

                    # 현재 각도를 기본값으로 세팅 (선택되지 않은 관절은 움직이지 않게 고정)
                    t_j1 = pose['jointAngle'][0]
                    t_j2 = pose['jointAngle'][1]
                    t_j3 = pose['jointAngle'][2]
                    t_j4 = pose['jointAngle'][3]

                    # 화면의 X축(좌우) 위치를 각도로 변환
                    if fingers == 1:   # 1번 조인트
                        target_angle = map_value(target_x, 0, 1, 80, -80) 
                        t_j1 = target_angle
                        mode_str = "J1(베이스)"
                        
                    elif fingers == 2: # 2번 조인트
                        target_angle = map_value(target_x, 0, 1, 80, 0) 
                        t_j2 = target_angle
                        mode_str = "J2(리어 암)"
                        
                    elif fingers == 3: # 3번 조인트
                        target_angle = map_value(target_x, 0, 1, 80, 10) # J3는 너무 낮추면 충돌위험
                        t_j3 = target_angle
                        mode_str = "J3(포어 암)"
                        
                    elif fingers == 4: # 4번 조인트
                        target_angle = map_value(target_x, 0, 1, 80, -80)
                        t_j4 = target_angle
                        mode_str = "J4(서보 헤드)"

                    # 🔥 목표 각도가 이전보다 THRESHOLD_DEGREE(3도) 이상 변했을 때만명령 전송!
                    if abs(target_angle - last_sent_angle) > THRESHOLD_DEGREE:
                        # ptp_mode=4 (각 관절 독립 제어). x, y, z, r 파라미터가 J1, J2, J3, J4에 1:1로 대응됩니다.
                        device.set_ptpcmd(PORT, ptp_mode=4, x=t_j1, y=t_j2, z=t_j3, r=t_j4)
                        last_sent_angle = target_angle
                        print(f"[{mode_str}] 독립 관절 이동 -> 목표 각도: {target_angle:.1f}도")

            except Exception as e:
                pass 
        else:
            # 손이 화면에서 사라졌을 때
            if last_fingers != -1:
                last_fingers = -1
                print("[Robot] ⚠️ 손 인식 안됨 - 현재 상태 대기")

        time.sleep(0.05) 

    try:
        device.set_endeffector_suctioncup(PORT, False, False)
        device.disconnect_dobot(PORT)
    except:
        pass

# -----------------------------------
# MediaPipe 및 손가락 카운팅 로직
# -----------------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)

def get_finger_count(hand_landmarks):
    count = 0
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    for tip, pip in zip(tips, pips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            count += 1
            
    wrist_x = hand_landmarks.landmark[0].x
    thumb_tip_x = hand_landmarks.landmark[4].x
    thumb_mcp_x = hand_landmarks.landmark[2].x
    
    if abs(thumb_tip_x - wrist_x) > abs(thumb_mcp_x - wrist_x):
        count += 1
        
    return count

# -----------------------------------
# Vision Thread
# -----------------------------------
def vision_loop():
    global latest_x, latest_y, latest_fingers, robot_running

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("🚨 [에러] 카메라를 열 수 없습니다!")
        robot_running = False
        return

    print("[Camera] READY ✔")

    ALPHA = 0.15 # 스무딩 필터
    smoothed_x, smoothed_y = None, None

    while robot_running:
        ret, frame = cap.read()
        if not ret: continue

        frame = cv2.flip(frame, 1) 
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        h, w, _ = frame.shape

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                wrist = hand_landmarks.landmark[0]
                
                if smoothed_x is None:
                    smoothed_x, smoothed_y = wrist.x, wrist.y
                else:
                    smoothed_x = ALPHA * wrist.x + (1 - ALPHA) * smoothed_x
                    smoothed_y = ALPHA * wrist.y + (1 - ALPHA) * smoothed_y

                fingers = get_finger_count(hand_landmarks)

                cv2.putText(frame, f"Fingers: {fingers}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # 조작 가이드 출력 (이제 모두 X축(좌우) 컨트롤 기반입니다!)
                guides = {
                    0: "FIST : Vacuum ON",
                    1: "1 FINGER : Move Hand L/R -> Base Angle",
                    2: "2 FINGERS: Move Hand L/R -> Rear Arm Angle",
                    3: "3 FINGERS: Move Hand L/R -> Fore Arm Angle",
                    4: "4 FINGERS: Move Hand L/R -> Servo Angle",
                    5: "5 FINGERS: Vacuum OFF"
                }
                cv2.putText(frame, guides.get(fingers, ""), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                
                # X축 컨트롤을 강조하기 위해 화면 중앙에 가이드 선 그리기
                cv2.line(frame, (w//2, 0), (w//2, h), (100, 100, 100), 1)
                cv2.circle(frame, (int(wrist.x * w), int(wrist.y * h)), 10, (255, 0, 0), -1)

                with lock:
                    latest_x = smoothed_x
                    latest_y = smoothed_y
                    latest_fingers = fingers

        else:
            smoothed_x, smoothed_y = None, None
            with lock:
                latest_x = None
                latest_y = None
                latest_fingers = 0

        cv2.imshow("Iron Man Control (X-Axis Mode)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            robot_running = False
            break

    cap.release()
    cv2.destroyAllWindows()

# -----------------------------------
# 실행
# -----------------------------------
if __name__ == "__main__":
    t1 = threading.Thread(target=robot_worker, daemon=True)
    t2 = threading.Thread(target=vision_loop)

    t1.start()
    t2.start()
    t2.join()