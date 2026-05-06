import pyrealsense2 as rs
import numpy as np
import cv2
from pyModbusTCP.client import ModbusClient

# ========================================================
# [Modbus TCP 설정]
# 연결할 PLC나 로봇 제어기의 실제 IP 주소로 변경해 주세요.
MODBUS_IP = "192.168.1.100" 
MODBUS_PORT = 502
client = ModbusClient(host=MODBUS_IP, port=MODBUS_PORT, auto_open=True)
# ========================================================

# 파이프라인 먼저 설정
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

# 각 색상별 객체가 화면에 있는지를 '기억'하는 상태 변수
is_red_present = False 
is_blue_present = False
is_yellow_present = False

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue 
            
        color_image = np.asanyarray(color_frame.get_data())
        hsv_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        # ========================================================
        # 1. 색상별 HSV 범위 설정
        # ========================================================
        # 빨간색 (H값 0~10, 170~179)
        lower_red1 = np.array([0, 150, 80])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 150, 80])
        upper_red2 = np.array([179, 255, 255])
        
        # 파란색 (H값 100~130 주변)
        lower_blue = np.array([100, 150, 80])
        upper_blue = np.array([130, 255, 255])
        
        # 노란색 (H값 20~35 주변)
        lower_yellow = np.array([20, 150, 80])
        upper_yellow = np.array([35, 255, 255])

        # ========================================================
        # 2. 마스크 생성 및 모폴로지 연산 (노이즈 제거)
        # ========================================================
        kernel = np.ones((5, 5), np.uint8)
        
        mask_red = cv2.bitwise_or(cv2.inRange(hsv_image, lower_red1, upper_red1), 
                                  cv2.inRange(hsv_image, lower_red2, upper_red2))
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
        
        mask_blue = cv2.inRange(hsv_image, lower_blue, upper_blue)
        mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel)
        
        mask_yellow = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
        mask_yellow = cv2.morphologyEx(mask_yellow, cv2.MORPH_OPEN, kernel)

        # ========================================================
        # 3. 색상별 윤곽선(Contour) 검출 및 Modbus 전송 로직
        # ========================================================
        current_red_detected = False
        current_blue_detected = False
        current_yellow_detected = False

        # --- [빨간색 검사] ---
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours_red:
            if cv2.contourArea(contour) > 1000:
                current_red_detected = True
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 0, 255), 2) # 빨간색 네모

        if current_red_detected and not is_red_present:
            print("Red OK -> Modbus Address 11에 1 쓰기")
            # 11번 레지스터 주소에 1을 기록 (Holding Register)
            client.write_single_register(11, 1)
            is_red_present = True
        elif not current_red_detected and is_red_present:
            is_red_present = False

        # --- [파란색 검사] ---
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours_blue:
            if cv2.contourArea(contour) > 1000:
                current_blue_detected = True
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(color_image, (x, y), (x + w, y + h), (255, 0, 0), 2) # 파란색 네모

        if current_blue_detected and not is_blue_present:
            print("Blue OK -> Modbus Address 12에 2 쓰기")
            # 12번 레지스터 주소에 2를 기록
            client.write_single_register(12, 2)
            is_blue_present = True
        elif not current_blue_detected and is_blue_present:
            is_blue_present = False

        # --- [노란색 검사] ---
        contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours_yellow:
            if cv2.contourArea(contour) > 1000:
                current_yellow_detected = True
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 255, 255), 2) # 노란색 네모

        if current_yellow_detected and not is_yellow_present:
            print("Yellow OK -> Modbus Address 13에 3 쓰기")
            # 13번 레지스터 주소에 3을 기록
            client.write_single_register(13, 3)
            is_yellow_present = True
        elif not current_yellow_detected and is_yellow_present:
            is_yellow_present = False

        # ========================================================
        
        cv2.imshow("ssafy stream", color_image)
        # 여러 마스크를 동시에 보려면 합쳐서 출력할 수도 있습니다.
        # combined_mask = cv2.bitwise_or(mask_red, cv2.bitwise_or(mask_blue, mask_yellow))
        # cv2.imshow("combined mask", combined_mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()