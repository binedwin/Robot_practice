import pyrealsense2 as rs
import numpy as np
import cv2

# 파이프라인 먼저 설정
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

pipeline.start(config)

# ========================================================
# [추가된 부분] 빨간 객체가 현재 화면에 있는지를 '기억'하는 상태 변수
is_object_present = False 
# ========================================================

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue 
            
        color_image = np.asanyarray(color_frame.get_data())
        hsv_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        lower_red1 = np.array([0, 200, 80])
        upper_red1 = np.array([10, 255, 255])

        lower_red2 = np.array([170, 200, 80])
        upper_red2 = np.array([179, 255, 255])

        mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
        mask3 = cv2.bitwise_or(mask1, mask2)

        kernel = np.ones((5, 5), np.uint8)
        mask3 = cv2.morphologyEx(mask3, cv2.MORPH_OPEN, kernel)
        contours, _ = cv2.findContours(mask3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # ========================================================
        # 이번 프레임(순간)에 객체가 보이는지 확인하는 임시 변수
        current_detected = False
        # ========================================================
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000: 
                current_detected = True # 크기가 1000 이상인 빨간 객체 발견!
                
                # 인식된 객체에 초록색 네모 그리기
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
        # ========================================================
        # [핵심 로직] 상태가 변했을 때만 반응하기
        
        # 1. 방금 전까지 없었는데(False), 지금 나타났다면(True)?
        if current_detected and not is_object_present:
            print("OK") # 처음 등장하는 순간 딱 1번만 출력!
            is_object_present = True # 이제 화면에 '있음' 상태로 업데이트
            
        # 2. 방금 전까지 있었는데(True), 지금 사라졌다면(False)?
        elif not current_detected and is_object_present:
            is_object_present = False # 화면에서 완전히 사라지면 '없음' 상태로 리셋
        # ========================================================


        final_mask = cv2.bitwise_and(color_image, color_image, mask=mask3)

        cv2.imshow("ssafy stream", color_image) 
        cv2.imshow("color mask hsv", mask3) 
        cv2.imshow("color m5ask bitwise", final_mask) 

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()