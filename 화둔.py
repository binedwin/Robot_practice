import pyrealsense2 as rs
import numpy as np
import cv2
import mediapipe as mp
import math
import time
import random

# ----------------------------------------
# MediaPipe 설정
# ----------------------------------------
mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_mesh
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

face_mesh = mp_face.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# ----------------------------------------
# RealSense 설정
# ----------------------------------------
pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(
    rs.stream.color,
    640,
    480,
    rs.format.bgr8,
    30
)

pipeline.start(config)

# ----------------------------------------
# 화둔 상태
# ----------------------------------------
fire_mode = False
fire_start_time = 0

# ----------------------------------------
# 손가락 상태 확인
# ----------------------------------------
def is_finger_up(hand_landmarks, tip_id, pip_id):

    return (
        hand_landmarks.landmark[tip_id].y <
        hand_landmarks.landmark[pip_id].y
    )

# ----------------------------------------
# 가위 손모양 판별
# ✌️
# ----------------------------------------
def detect_scissors(hand_landmarks):

    index_up = is_finger_up(hand_landmarks, 8, 6)
    middle_up = is_finger_up(hand_landmarks, 12, 10)

    ring_up = is_finger_up(hand_landmarks, 16, 14)
    pinky_up = is_finger_up(hand_landmarks, 20, 18)

    if index_up and middle_up and not ring_up and not pinky_up:
        return True

    return False

# ----------------------------------------
# 거리 계산
# ----------------------------------------
def distance(x1, y1, x2, y2):

    return math.sqrt(
        (x1 - x2) ** 2 +
        (y1 - y2) ** 2
    )

# ----------------------------------------
# 메인 루프
# ----------------------------------------
try:

    while True:

        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue

        frame = np.asanyarray(color_frame.get_data())

        # 셀카 모드
        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        h, w, _ = frame.shape

        # ----------------------------------------
        # 얼굴 인식
        # ----------------------------------------
        face_result = face_mesh.process(rgb)

        mouth_x = None
        mouth_y = None

        if face_result.multi_face_landmarks:

            for face_landmarks in face_result.multi_face_landmarks:

                # 입 중앙 landmark
                mouth = face_landmarks.landmark[13]

                mouth_x = int(mouth.x * w)
                mouth_y = int(mouth.y * h)

                # 입 표시
                cv2.circle(
                    frame,
                    (mouth_x, mouth_y),
                    5,
                    (0,255,255),
                    -1
                )

        # ----------------------------------------
        # 손 인식
        # ----------------------------------------
        hand_result = hands.process(rgb)

        if hand_result.multi_hand_landmarks:

            for hand_landmarks in hand_result.multi_hand_landmarks:

                # 손 랜드마크
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                # 검지 끝 좌표
                finger = hand_landmarks.landmark[8]

                fx = int(finger.x * w)
                fy = int(finger.y * h)

                # 가위 손모양인지 확인
                scissors = detect_scissors(hand_landmarks)

                if scissors and mouth_x is not None:

                    # 손과 입 거리
                    dist = distance(
                        fx,
                        fy,
                        mouth_x,
                        mouth_y
                    )

                    # 입 근처에서 수인하면 화둔 발동
                    if dist < 80:

                        fire_mode = True
                        fire_start_time = time.time()

        # ----------------------------------------
        # 화둔 이펙트
        # ----------------------------------------
        output = frame.copy()

        if time.time() - fire_start_time < 2:

            center_x = 320
            center_y = 240

            # 불꽃 파티클
            for i in range(120):

                px = random.randint(center_x, center_x + 300)
                py = random.randint(center_y - 120, center_y + 120)

                radius = random.randint(8, 30)

                color_choice = random.randint(0, 2)

                # 빨강 / 주황 / 노랑
                if color_choice == 0:
                    color = (0, 0, 255)

                elif color_choice == 1:
                    color = (0, 140, 255)

                else:
                    color = (0, 255, 255)

                cv2.circle(
                    output,
                    (px, py),
                    radius,
                    color,
                    -1
                )

            # 화염 코어
            cv2.ellipse(
                output,
                (420, 240),
                (220, 100),
                0,
                -20,
                20,
                (0,140,255),
                -1
            )

            cv2.ellipse(
                output,
                (450, 240),
                (170, 70),
                0,
                -20,
                20,
                (0,255,255),
                -1
            )

            # 밝기 합성
            output = cv2.addWeighted(
                output,
                0.85,
                frame,
                0.15,
                0
            )

            # 텍스트
            cv2.putText(
                output,
                "FIRE STYLE : FIREBALL JUTSU!",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (255,255,255),
                4
            )

        # ----------------------------------------
        # UI
        # ----------------------------------------
        cv2.putText(
            output,
            "Naruto Fireball System",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,255),
            2
        )

        cv2.imshow(
            "NARUTO FIREBALL",
            output
        )

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:

    hands.close()
    face_mesh.close()

    pipeline.stop()

    cv2.destroyAllWindows()