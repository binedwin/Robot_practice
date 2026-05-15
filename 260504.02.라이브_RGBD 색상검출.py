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

    lower_bgr = np.array([0, 0, 150]) #색상의 최소값(어두운 빨간색)
    upper_bgr = np.array([100, 100, 255]) #색상의 최대값 (밝은 빨간색)
    #lower_bgr = np.array([150, 0, 0])   # 어두운 파란색
    #upper_bgr = np.array([255, 100, 100])  # 밝은 파란색

    mask = cv2.inRange(color_image, lower_bgr, upper_bgr) #최소값, 최대값 마스크 처리
    #입력된 이미지에서, 특정 색 범위에 포함되는 픽셀만 255로 출력(화이트)
    #나머지는 0 값 (블랙)으로 만든 2진  이미지(mask)
    #inRange 조건 생성(마스크만드는 조건)
    
    mask_bit = cv2.bitwise_and(color_image, color_image, mask=mask) #마스크 연산
    #mask 에서 만든 레이어를 이용해서 255인 부분만 원본 이미지로 유지
    #0인 부분은 전부 검정으로 제거, 선택된 부분만 실제로 보여주는거
    #bitwise_and 조건 적용 (이미지에서 추출)


    cv2.imshow("SSAFY RGBD CAMERA STREAM", color_image) #원본 영상
    cv2.imshow("Color Mask (BGR)", mask) #인식된 부분만 마스크(흰색) 처리, 나머지는 블랙
    cv2.imshow("color Mask BitWise", mask_bit) #인식된 부분만 표현

    #'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q') : #cv2.waitKey(1) & 0xFF == 27
      #ESC에 대한 ASCII 코드는 제어문자 주소가 ESC로 하고싶은 경우 27임으로 27을 입력 
      #cv2.waitKey() 하면 불필요한 상위비트까지 반환할 수 있기 때문에
      #우리가 필요한 ASCII 값 8bit(0-255)범위만 AND 연산을 해서 끝자리 8bit만 깔끔하게 남기기 위해
      #0xFF를 적고 AND연산 해줍니다. (0xFF = 11111111)
      break

finally:
  pipeline.stop() #영상 리소스 해제
  cv2.destroyAllWindows() #모든 OpenCV창을 닫음.