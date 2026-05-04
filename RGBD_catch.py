import pyrealsense2 as rs #리얼센스 카메라를 제어하는 라이브러리
import numpy as np #이미지 데이터를 배열 형태로 처리하기 위한 라이브러리
import cv2 # opencv 영상처리 영상출력을 위해서 사용

#파이프라인 먼저 설정
pipeline = rs.pipeline() # 파이프라인 객체생성
config = rs.config() # 해상도, 영상종류, 프레임을 사용하기 위한 설정 객체를 생성
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
#RGB 기반 컬러 스트림을 생성, 해상도, 8bit, 30 프레임

pipeline.start(config) #파이프라인 ㅅ ㅣ작

try:
    while True:
        frames = pipeline.wait_for_frames() # 카메라의 실시간 최신 프레임을 수신 (색상, 깊이, 자이로..)
        color_frame = frames.get_color_frame() # 위의 정보 중에서 컬러 프레임만 추출

        if not color_frame: # 만약 컬러 프레임이 없으면 처음 루프로 빠져나감
            continue 
        #컬러 프레임을 numpy 배열로 변환
        color_image= np.asanyarray(color_frame.get_data())

        lower_bgr = np.array([150,0, 0]) # 최소값 (어두운 빨간색 )
        upper_bgr = np.array([255,100,100]) # 최대값 (밝은 빨간색)

        mask = cv2.inRange(color_image, lower_bgr, upper_bgr) # 최소값, 최대값 마스크 처리 

        mask_bit = cv2.bitwise_and(color_image, color_image, mask = mask) # 마스크 연산

        cv2.imshow("ssafy stream", color_image) #원본 영상
        cv2.imshow("color mask bgr", mask) # 인식된 부분만 마스크 처리
        cv2.imshow("color mask bitwise", mask_bit) #인식된 부분만 표현

        if cv2.waitKey(1) & 0xFF == ord('q'):
            # ESC에 대한 ASCII 코드는 제어문자 주소가 ESC로 하고싶은 경우 27임으로 27을 입력
            break

finally:
    pipeline.stop() # 영상 리소스 해제
    cv2.destroyAllWindows() # 모든 opencv 창을 닫음