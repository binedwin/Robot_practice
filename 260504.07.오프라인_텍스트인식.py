import pyrealsense2 as rs #리얼센스카메라를 제어하는 라이브러리
import numpy as np #이미지 데이터를 배열 형태로 처리하기 위한 하이브러리
import cv2 #OpenCV, 영상 처리, 영상 출력을 위해서 사용
import pytesseract

#pytessract 엔진 실행
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


#파이프라인 먼저 설정
pipeline = rs.pipeline() #파이프라인 객체 생성
config = rs.config() #해상도, 영상종류, 프레임을 사용하기 위한 설정 객체를 생성
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
#RGB기반 컬러 스트림을 생성, 해상도, 8bit, 30프레임

pipeline.start(config) #파이프라인 시작


try:
  while True:
    frames = pipeline.wait_for_frames() #카메라의 실시간 최신 프레임을 수신(색상, 깊이, 자이로..)
    color_frame = frames.get_color_frame() #위의 정보 중에서 컬러 프레임만 추출

    if not color_frame: #만약 컬러 프레임이 없으면, 처음 루프로 빠져나갑니다.(수신 실패 방지)
      continue
    #컬러 프레임을 numpy 배열로 변환
    color_image = np.asanyarray(color_frame.get_data())

    #OCR 전처리
    gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

    # 노이즈 제거
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    #이진화 처리 (텍스트 인식률 향상)
    _, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)

    #OCR 실행

    text =pytesseract.image_to_string(thresh, lang='kor')

    #출력
    print("인식된 텍스트 :")
    print(text)

    cv2.imshow("SSAFY RGBD CAMERA STREAM", color_image) #원본 영상
    cv2.imshow("threshold", thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

finally:
  pipeline.stop() #리소스 해제
  cv2.destroyAllWindows() #모든 CV닫기