import pyrealsense2 as rs
import numpy as np
import cv2
import mediapipe as mp
import time

# ---------------------------------------
# MediaPipe
# ---------------------------------------
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
mp_selfie = mp.solutions.selfie_segmentation

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

pose = mp_pose.Pose()

# 사람 영역 분리 모델
segment = mp_selfie.SelfieSegmentation(model_selection=1)

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
# 분신술 변수
# ---------------------------------------
clone_time = 0

# ---------------------------------------
# 손동작 인식
# ✌️ = 분신술
# ---------------------------------------
def is_finger_up(hand_landmarks, tip_id, pip_id):

    return (
        hand_landmarks.landmark[tip_id].y <
        hand_landmarks.landmark[pip_id].y
    )


def detect_shadow_clone(hand_landmarks):

    index_up = is_finger_up(hand_landmarks, 8, 6)
    middle_up = is_finger_up(hand_landmarks, 12, 10)

    ring_up = is_finger_up(hand_landmarks, 16, 14)
    pinky_up = is_finger_up(hand_landmarks, 20, 18)

    if index_up and middle_up and not ring_up and not pinky_up:
        return True

    return False


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

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # ---------------------------------------
        # 손 인식
        # ---------------------------------------
        hand_result = hands.process(rgb)

        if hand_result.multi_hand_landmarks:

            for hand_landmarks in hand_result.multi_hand_landmarks:

                # 손 그리기
                mp.solutions.drawing_utils.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                # 분신술 감지
                if detect_shadow_clone(hand_landmarks):
                    clone_time = time.time()

        # ---------------------------------------
        # 사람 분리
        # ---------------------------------------
        seg_result = segment.process(rgb)

        mask = seg_result.segmentation_mask

        condition = mask > 0.6

        # 배경 제거된 사람만 추출
        person_only = np.zeros_like(frame)

        person_only[condition] = frame[condition]

        output = frame.copy()

        # ---------------------------------------
        # 분신술 실행
        # ---------------------------------------
        if time.time() - clone_time < 3:

            h, w, _ = frame.shape

            # 원본 사람 크기
            clone = person_only.copy()

            # 왼쪽 분신
            left_matrix = np.float32([
                [1, 0, -180],
                [0, 1, 0]
            ])

            left_clone = cv2.warpAffine(
                clone,
                left_matrix,
                (w, h)
            )

            # 오른쪽 분신
            right_matrix = np.float32([
                [1, 0, 180],
                [0, 1, 0]
            ])

            right_clone = cv2.warpAffine(
                clone,
                right_matrix,
                (w, h)
            )

            # 합성
            output = cv2.addWeighted(output, 1.0, left_clone, 1.0, 0)
            output = cv2.addWeighted(output, 1.0, right_clone, 1.0, 0)

            # 연막 효과
            smoke = output.copy()

            cv2.circle(smoke, (120, 320), 90, (220,220,220), -1)
            cv2.circle(smoke, (520, 320), 90, (220,220,220), -1)

            output = cv2.addWeighted(
                smoke,
                0.25,
                output,
                0.75,
                0
            )

            # 텍스트
            cv2.putText(
                output,
                "나루토 분신!!",
                (70, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.4,
                (255,255,255),
                4
            )

        # ---------------------------------------
        # 출력
        # ---------------------------------------
        cv2.imshow("NARUTO AI SHADOW CLONE", output)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:

    hands.close()
    pose.close()
    pipeline.stop()
    cv2.destroyAllWindows()