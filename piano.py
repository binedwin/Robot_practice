import cv2
import mediapipe as mp
import numpy as np
import pygame
import os

# -----------------------------------
# pygame 초기화 (안정 버전)
# -----------------------------------
pygame.mixer.init()

# -----------------------------------
# 음계 (3옥타브 + 검은건반)
# -----------------------------------
notes_freq = {
    "C3": 130.81, "C#3": 138.59, "D3": 146.83, "D#3": 155.56,
    "E3": 164.81, "F3": 174.61, "F#3": 185.00, "G3": 196.00,
    "G#3": 207.65, "A3": 220.00, "A#3": 233.08, "B3": 246.94,

    "C4": 261.63, "C#4": 277.18, "D4": 293.66, "D#4": 311.13,
    "E4": 329.63, "F4": 349.23, "F#4": 369.99, "G4": 392.00,
    "G#4": 415.30, "A4": 440.00, "A#4": 466.16, "B4": 493.88,

    "C5": 523.25, "C#5": 554.37, "D5": 587.33, "D#5": 622.25,
    "E5": 659.25, "F5": 698.46, "F#5": 739.99, "G5": 783.99,
    "G#5": 830.61, "A5": 880.00, "A#5": 932.33, "B5": 987.77
}

# -----------------------------------
# WAV 없으면 생성 (자동)
# -----------------------------------
import wave, struct, math

def create_wav(name, freq):
    if os.path.exists(name):
        return

    sample_rate = 44100
    duration = 0.6
    volume = 0.4

    wav = wave.open(name, "w")
    wav.setparams((1, 2, sample_rate, 0, "NONE", "not compressed"))

    for i in range(int(sample_rate * duration)):
        t = i / sample_rate

        wave_val = (
            math.sin(2 * math.pi * freq * t) +
            0.5 * math.sin(2 * math.pi * freq * 2 * t)
        )

        wave_val *= math.exp(-3 * t)
        wave_val = int(wave_val * volume * 32767)

        wav.writeframes(struct.pack("<h", wave_val))

    wav.close()

# WAV 생성
for n, f in notes_freq.items():
    create_wav(f"{n}.wav", f)

# -----------------------------------
# pygame Sound 로딩
# -----------------------------------
notes = {
    n: pygame.mixer.Sound(f"{n}.wav")
    for n in notes_freq
}

# -----------------------------------
# MediaPipe
# -----------------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

draw = mp.solutions.drawing_utils

# -----------------------------------
# 카메라 (고해상도)
# -----------------------------------
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# -----------------------------------
# 건반 분리
# -----------------------------------
white_keys = [k for k in notes_freq if "#" not in k]

black_keys = [k for k in notes_freq if "#" in k]

# -----------------------------------
# 상태 변수
# -----------------------------------
last_note = ""

# -----------------------------------
# 메인 루프
# -----------------------------------
while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    # -----------------------------------
    # 흰 건반
    # -----------------------------------
    key_width = w // len(white_keys)
    key_height = 240

    key_map = []

    for i, note in enumerate(white_keys):

        x1 = i * key_width
        x2 = x1 + key_width
        y1 = h - key_height
        y2 = h

        key_map.append((note, x1, y1, x2, y2))

        cv2.rectangle(frame, (x1,y1), (x2,y2), (255,255,255), -1)
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,0), 2)

        cv2.putText(frame, note, (x1+10, y1+130),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)

    # -----------------------------------
    # 손 인식
    # -----------------------------------
    pressed_note = ""

    if result.multi_hand_landmarks:

        for hand_landmarks in result.multi_hand_landmarks:

            draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

            tip = hand_landmarks.landmark[8]
            fx, fy = int(tip.x * w), int(tip.y * h)

            cv2.circle(frame, (fx, fy), 15, (0,255,255), -1)

            # -----------------------------------
            # 충돌 체크
            # -----------------------------------
            for note, x1, y1, x2, y2 in key_map:

                if x1 < fx < x2 and y1 < fy < y2:
                    pressed_note = note

                    cv2.rectangle(frame, (x1,y1), (x2,y2), (0,200,255), -1)

    # -----------------------------------
    # 소리 재생
    # -----------------------------------
    if pressed_note and pressed_note != last_note:
        notes[pressed_note].play()

    last_note = pressed_note

    # -----------------------------------
    # UI
    # -----------------------------------
    cv2.putText(frame, "AI HAND PIANO", (20,50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 3)

    cv2.putText(frame, "Touch with index finger", (20,90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200,200,200), 2)

    # -----------------------------------
    # 출력
    # -----------------------------------
    cv2.imshow("AI PIANO", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()