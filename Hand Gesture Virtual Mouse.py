
import cv2
import mediapipe as mp
import pyautogui
import math
import time

# Screen dimensions
screen_width, screen_height = pyautogui.size()

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Webcam not found!")

# Cursor smoothing
smoothening = 5
prev_x, prev_y = 0, 0

# Click cooldown
last_click_time = 0
click_delay = 0.5

print("Virtual Mouse Started!")
print("Index finger: Move cursor")
print("Thumb + Index pinch: Left click")
print("Press Q to quit")

try:
    while True:
        success, frame = cap.read()

        if not success:
            print("Failed to read webcam.")
            break

        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape

        rgb_frame = cv2.cvtColor(
            frame, cv2.COLOR_BGR2RGB
        )

        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                landmarks = hand_landmarks.landmark

                # Index fingertip
                index_x = int(
                    landmarks[8].x * width
                )
                index_y = int(
                    landmarks[8].y * height
                )

                # Thumb tip
                thumb_x = int(
                    landmarks[4].x * width
                )
                thumb_y = int(
                    landmarks[4].y * height
                )

                # Map camera coordinates to screen
                target_x = index_x / width * screen_width
                target_y = index_y / height * screen_height

                # Smooth movement
                current_x = prev_x + (
                    target_x - prev_x
                ) / smoothening

                current_y = prev_y + (
                    target_y - prev_y
                ) / smoothening

                # Keep cursor within screen
                current_x = max(
                    1, min(screen_width - 2, current_x)
                )
                current_y = max(
                    1, min(screen_height - 2, current_y)
                )

                pyautogui.moveTo(
                    current_x, current_y
                )

                prev_x, prev_y = current_x, current_y

                # Calculate pinch distance
                distance = math.hypot(
                    index_x - thumb_x,
                    index_y - thumb_y
                )

                # Draw fingertip markers
                cv2.circle(
                    frame,
                    (index_x, index_y),
                    10,
                    (0, 255, 0),
                    -1
                )

                cv2.circle(
                    frame,
                    (thumb_x, thumb_y),
                    10,
                    (255, 0, 0),
                    -1
                )

                # Detect pinch click
                if distance < 30:
                    current_time = time.time()

                    if current_time - last_click_time > click_delay:
                        pyautogui.click()
                        last_click_time = current_time

                        cv2.putText(
                            frame,
                            "CLICK!",
                            (30, 100),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.5,
                            (0, 255, 0),
                            3
                        )

        cv2.putText(
            frame,
            "Virtual Mouse | Press Q to Quit",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.imshow("Hand Gesture Virtual Mouse", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    hands.close()
