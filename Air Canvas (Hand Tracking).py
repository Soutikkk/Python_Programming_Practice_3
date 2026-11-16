
import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Webcam not found!")

canvas = None
previous_point = None

colors = [
    (255, 0, 0),    # Blue
    (0, 255, 0),    # Green
    (0, 0, 255),    # Red
    (0, 255, 255)   # Yellow
]

current_color = colors[0]
brush_size = 6

print("AIR CANVAS STARTED")
print("Index finger: Draw")
print("Index + middle fingers: Stop drawing")
print("Press 1-4: Change colors")
print("Press E: Eraser")
print("Press C: Clear")
print("Press S: Save")
print("Press Q: Quit")

while True:
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    if canvas is None:
        canvas = np.zeros_like(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            landmarks = hand.landmark

            index_tip = landmarks[8]
            index_pip = landmarks[6]
            middle_tip = landmarks[12]
            middle_pip = landmarks[10]

            x = int(index_tip.x * width)
            y = int(index_tip.y * height)

            index_up = index_tip.y < index_pip.y
            middle_up = middle_tip.y < middle_pip.y

            if index_up and not middle_up:
                current_point = (x, y)

                if previous_point is not None:
                    cv2.line(
                        canvas,
                        previous_point,
                        current_point,
                        current_color,
                        brush_size
                    )

                previous_point = current_point

                cv2.circle(
                    frame, (x, y), 10,
                    current_color, -1
                )
            else:
                previous_point = None

            mp_draw.draw_landmarks(
                frame, hand,
                mp_hands.HAND_CONNECTIONS
            )
    else:
        previous_point = None

    # Overlay drawing on webcam feed
    mask = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)

    background = cv2.bitwise_and(
        frame, frame,
        mask=cv2.bitwise_not(mask)
    )

    drawing = cv2.bitwise_and(
        canvas, canvas,
        mask=mask
    )

    output = cv2.add(background, drawing)

    cv2.rectangle(
        output, (0, 0), (width, 55),
        (30, 30, 30), -1
    )

    cv2.putText(
        output,
        "1-4: Colors | E: Erase | C: Clear | S: Save | Q: Quit",
        (15, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    cv2.imshow("Air Canvas - Hand Tracking", output)

    key = cv2.waitKey(1) & 0xFF

    if key in [ord('1'), ord('2'), ord('3'), ord('4')]:
        current_color = colors[key - ord('1')]
        brush_size = 6

    elif key == ord('e'):
        current_color = (0, 0, 0)
        brush_size = 35

    elif key == ord('c'):
        canvas[:] = 0

    elif key == ord('s'):
        filename = (
            "AirCanvas_" +
            datetime.now().strftime("%Y%m%d_%H%M%S") +
            ".png"
        )
        cv2.imwrite(filename, canvas)
        print("Saved:", filename)

    elif key == ord('q'):
        break

cap.release()
hands.close()
cv2.destroyAllWindows()
