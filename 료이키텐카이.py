import pyrealsense2 as rs
import numpy as np
import cv2
import mediapipe as mp
import time

# ---------------------------------------
# MediaPipe
# ---------------------------------------
mp_hands = mp.solutions.hands
mp_selfie = mp.solutions.selfie_segmentation

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

segment = mp_selfie.SelfieSegmentation(model_selection=1)

draw = mp.solutions.drawing_utils

# ---------------------------------------
# RealSense
# ---------------------------------------
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

# ---------------------------------------
# 우주 배경
# ---------------------------------------
space_bg = cv2.imread("space.jpg")

if space_bg is None:
    print("space.jpg 파일이 필요합니다.")
    exit()

# ---------------------------------------
# 영역전개 변수
# ---------------------------------------
domain_active = False
domain_start = 0

fade_strength = 0

# ---------------------------------------
# 손모양 인식
# ---------------------------------------
def is_finger_up(hand_landmarks, tip_id, pip_id):

    return (
        hand_landmarks.landmark[tip_id].y <
        hand_landmarks.landmark[pip_id].y
    )

def detect_domain_pose(hand_landmarks):

    index_up = is_finger_up(hand_landmarks, 8, 6)
    middle_up = is_finger_up(hand_landmarks, 12, 10)

    ring_up = is_finger_up(hand_landmarks, 16, 14)
    pinky_up = is_finger_up(hand_landmarks, 20, 18)

    # ✌️ 손모양
    return index_up and middle_up and not ring_up and not pinky_up

# ---------------------------------------
# 메인 루프
# ---------------------------------------
try:

    while True:

        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue

        frame = np.asanyarray(color_frame.get_data())

        # 셀카모드
        frame = cv2.flip(frame, 1)

        h, w, _ = frame.shape

        # 우주 배경 크기 맞춤
        bg = cv2.resize(space_bg, (w, h))

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # ---------------------------------------
        # 손 인식
        # ---------------------------------------
        hand_result = hands.process(rgb)

        if hand_result.multi_hand_landmarks:

            for hand_landmarks in hand_result.multi_hand_landmarks:

                draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                if detect_domain_pose(hand_landmarks):

                    domain_active = True
                    domain_start = time.time()

        # ---------------------------------------
        # 사람 분리
        # ---------------------------------------
        seg_result = segment.process(rgb)

        mask = seg_result.segmentation_mask

        condition = mask > 0.6

        # 사람만 추출
        person_only = np.zeros_like(frame)
        person_only[condition] = frame[condition]

        # 배경만 추출
        background_only = np.zeros_like(frame)
        background_only[~condition] = frame[~condition]

        output = frame.copy()

        # ---------------------------------------
        # 영역전개 효과
        # ---------------------------------------
        if domain_active:

            elapsed = time.time() - domain_start

            fade_strength += 2

            if fade_strength > 100:
                fade_strength = 100

            alpha = fade_strength / 100

            # 원래 배경 어둡게
            dark_bg = cv2.addWeighted(
                background_only,
                1 - alpha,
                np.zeros_like(background_only),
                alpha,
                0
            )

            # 우주 배경 등장
            if fade_strength > 20:

                bg_alpha = (fade_strength - 20) / 80

                dark_bg = cv2.addWeighted(
                    dark_bg,
                    1 - bg_alpha,
                    bg,
                    bg_alpha,
                    0
                )

            # 사람은 유지
            output = dark_bg.copy()
            output[condition] = person_only[condition]

            # ---------------------------------------
            # 보라색 오오라
            # ---------------------------------------
            overlay = output.copy()

            radius = int(180 + elapsed * 30)

            cv2.circle(
                overlay,
                (w // 2, h // 2),
                radius,
                (120, 0, 180),
                -1
            )

            output = cv2.addWeighted(
                overlay,
                0.12,
                output,
                0.88,
                0
            )

            # ---------------------------------------
            # 텍스트
            # ---------------------------------------
            cv2.putText(
                output,
                "DOMAIN EXPANSION",
                (40, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (255, 255, 255),
                4
            )

            cv2.putText(
                output,
                "Unlimited Void",
                (120, 140),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.1,
                (180, 180, 255),
                3
            )

            # ---------------------------------------
            # 종료
            # ---------------------------------------
            if elapsed > 8:

                domain_active = False
                fade_strength = 0

        # ---------------------------------------
        # 출력
        # ---------------------------------------
        cv2.imshow("JUJUTSU DOMAIN", output)

        key = cv2.waitKey(1)

        if key & 0xFF == ord('q'):
            break

        if key == ord('r'):
            domain_active = False
            fade_strength = 0

finally:

    hands.close()
    pipeline.stop()
    cv2.destroyAllWindows()