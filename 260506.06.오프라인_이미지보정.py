import pyrealsense2 as rs
import numpy as np
import cv2

# 마우스 클릭 이벤트를 처리할 전역 변수
pts = []

# 마우스 클릭 시 호출될 함수
def click_event(event, x, y, flags, param):
    global pts
    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 버튼 클릭
        pts.append([x, y])  # 클릭한 좌표를 저장

        # 점을 클릭한 곳에 점을 그려준다
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Frame", frame)

        # 4개의 점을 클릭하면 변환 시작
        if len(pts) == 4:
            print("4 points selected, real-time transformation active.")

# 인텔리얼센스 카메라 설정
pipeline = rs.pipeline()
config = rs.config()

# 색상 스트림 설정
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 15)

# 카메라 시작
pipeline.start(config)

# 출력 이미지 크기 설정
output_width, output_height = 1280, 720

try:
    while True:
        # 프레임 가져오기
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        frame = np.asanyarray(color_frame.get_data())  # 프레임을 numpy 배열로 변환

        # 마우스 이벤트로 점 클릭
        cv2.imshow("Frame", frame)
        cv2.setMouseCallback("Frame", click_event)

        if len(pts) == 4:
            # 원본 이미지에서 크롭할 사각형의 4점을 정의
            src_points = np.float32(pts)

            # 출력 평면에서 대응되는 4점 (출력 이미지는 직사각형)
            dst_points = np.float32([[0, 0], [output_width, 0], [output_width, output_height], [0, output_height]])

            # 변환 전 원본 4점으로 변환 행렬 계산
            matrix = cv2.getPerspectiveTransform(src_points, dst_points)

            # 변환 행렬을 적용하여 실시간으로 왜곡된 평면을 펴준다
            result = cv2.warpPerspective(frame, matrix, (output_width, output_height))

            # 변환된 이미지 실시간으로 출력
            cv2.imshow("Warped", result)

        # 'q' 키를 눌러 종료
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
finally:
    # 카메라 종료
    pipeline.stop()
    cv2.destroyAllWindows()