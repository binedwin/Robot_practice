import pyrealsense2 as rs #인텔 리얼센스 카메라 제어 라이브러리 호출
import numpy as np #이미지, 영상 데이터를 배열 형태로 처리하기 위한 라이브러리 호출
import cv2 #OpenCV, 영상 처리, 영상 출력 등을 하기위한 라이브러리 호출

#파이프라인 설정
pipeline = rs.pipeline() #파이프라인 객체를 생성
config = rs.config() #설정을 하기위한 객체를 생성
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
#컬러스트림을 설정, 해상도, 8bit 색영역, 30프레임

pipeline.start(config) #pipeline 시작

try:
  while True:
    frames = pipeline.wait_for_frames()
    #RGBD카메라를 통해서 실시간 프레임을 수신, (컬러, 깊이, 자이로...등등)
    color_frame = frames.get_color_frame()
    #frames에서 수신되는 정보 중에서 컬러 영상만 추출
    #--------만약 컬러 프레임이 없는 경우
    if not color_frame:
      continue
    #처음 루프로 빠져나와서 수신 실패를 방지

    color_image = np.asanyarray(color_frame.get_data())
    #컬러 프레임을 numpy 배열로 변환
    hsv_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
    #색 영역을 RGB에서 HSV로 변환

    #--- HSV t색영역에서 빨간색은 0도와 360도 영역에 걸쳐있기 때문
    #그런데 OpenCV에서는 0~360도 안쓰고 /2 해서 0~180까지만 사용
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)

    #두 마스크 합치기
    mask_sum = cv2.bitwise_or(mask1, mask2)

    #합친 마스크를 연산 후 대상으로 하는 색상만 출력하는 최종 마스크
    final_mask = cv2.bitwise_and(color_image, color_image, mask = mask_sum)

    #------add 윤곽선 추출 추가 
    contours, _ = cv2.findContours(mask_sum, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #RETR_EXTERNAL = 가장 바깥쪽 윤곽선만 추출
    #CHAIN_APPROX_SIMPLE = 윤곽선 처리를 단순화 시켜서 메모리를 절약

    for i in contours:
      area = cv2.contourArea(i)
      if 1000 > area > 500: #pixel수가 해당 조건에 맞는것만 필터링
        x, y, w, h = cv2.boundingRect(i)
        cv2.rectangle(color_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #그림을 그리는 영역, 색상, 굵기
        #boundingRect 는 외곽에 사각형으로 그림을 그림
    #---------------------------------------------------------------
    #------------------중심점표현 추가-----------------------------
        #if문 안에 작성
        cx = x + w // 2
        cy = y + h // 2

        #중심점에 마커로 표현
        cv2.drawMarker(color_image, (cx, cy), (255, 255, 0), markerType=cv2.MARKER_CROSS, markerSize= 10, thickness=2)

    
    #영상출력
    cv2.imshow("SSAFY RGBD CAMERA", color_image) #원본 영상
    #cv2.imshow("Color Mask (HSV)", mask_sum) #인식된 부분만 하얀색으로 표현, 나머지는 0
    #cv2.imshow("Color Mask2 (HSV)", final_mask) #인식된 부분만 복원해서 컬러로 출력

    #키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

finally:
  pipeline.stop() #영상 리소스 해제
  cv2.destroyAllWindows() #모든 OpenCV창을 종료