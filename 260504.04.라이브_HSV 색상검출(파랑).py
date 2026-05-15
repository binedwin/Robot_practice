import pyrealsense2 as rs #리얼센스카메라를 제어하는 라이브러리
import numpy as np #이미지 데이터를 배열 형태로 처리하기 위한 하이브러리
import cv2 #OpenCV, 영상 처리, 영상 출력을 위해서 사용

#파이프라인 먼저 설정
pipeline = rs.pipeline() #파이프라인 객체 생성
config = rs.config() #해상도, 영상종류, 프레임을 사용하기 위한 설정 객체를 생성
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
#RGB기반 컬러 스트림을 생성, 해상도, 8bit, 30프레임

pipeline.start(config) #파이프라인 시작

try:
  while True:
    frames = pipeline.wait_for_frames() # 카메라의 실시간 최신 프레임을 수신(색상, 깊이, 자이로..정보..)
    color_frame = frames.get_color_frame() #그 중에서 컬러 프레임만 추출

    if not color_frame: #만약 컬러 프레임이 없으면, 처음 루프로 빠져나가서 수신 실패 방지
      continue
    #컬러 프레임을 numpy 배열로 변환
    color_image = np.asanyarray(color_frame.get_data())
    #BGR 컬러 이미지를 HSV 색 영역으로 변환
    hsv_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

     
    lower_hsv = np.array([100, 100, 100])   # 어두운 파란색
    upper_hsv = np.array([130, 255, 255])   # 밝은 파란색
    

    mask = cv2.inRange(hsv_image, lower_hsv, upper_hsv)

    final_mask = cv2.bitwise_and(color_image, color_image, mask=mask)

    #마스크 연산 후 해당 색상만 출력

   
    #영상 출력
    cv2.imshow("SSAFY RGBD CAMERA STREAM", color_image) #원본 영상
    cv2.imshow("Color Mask (HSV)", mask) #인식된 부분만 흰색으로 마스크, 나머지는 블랙
    cv2.imshow("Color Mask BitWise", final_mask) #인식된 부분만 리얼로 표현

    #q키 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q') :
      break
finally:
  pipeline.stop() #영상 리로스 해제
  cv2.destroyAllWindows() #모든 openCV창을 닫음