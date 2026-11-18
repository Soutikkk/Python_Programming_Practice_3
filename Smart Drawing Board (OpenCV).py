
import cv2
import numpy as np
from datetime import datetime

WIDTH, HEIGHT = 1000, 650

canvas = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * 255

drawing = False
last_point = None
brush_size = 4
color = (0, 0, 0)

colors = {
    ord("r"): (0, 0, 255),
    ord("g"): (0, 180, 0),
    ord("b"): (255, 0, 0),
    ord("k"): (0, 0, 0),
}

def draw(event, x, y, flags, param):
    global drawing, last_point

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        last_point = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        cv2.line(canvas, last_point, (x, y),
                 color, brush_size)
        last_point = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        if drawing and last_point is not None:
            cv2.line(canvas, last_point, (x, y),
                     color, brush_size)
        drawing = False
        last_point = None


def recognize_shapes(image):
    result = image.copy()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(
        gray, 200, 255, cv2.THRESH_BINARY_INV
    )

    contours, _ = cv2.findContours(
        binary, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:
        area = cv2.contourArea(contour)

        if area < 500:
            continue

        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(
            contour, 0.04 * perimeter, True
        )

        vertices = len(approx)
        x, y, w, h = cv2.boundingRect(approx)

        if vertices == 3:
            shape = "Triangle"

        elif vertices == 4:
            ratio = w / float(h)

            if 0.9 <= ratio <= 1.1:
                shape = "Square"
            else:
                shape = "Rectangle"

        elif vertices > 7:
            shape = "Circle"

        else:
            shape = "Unknown"

        cv2.drawContours(
            result, [approx], -1, (0, 255, 0), 2
        )

        cv2.putText(
            result, shape, (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7, (255, 0, 255), 2
        )

    return result


cv2.namedWindow("Smart Drawing Board")
cv2.setMouseCallback("Smart Drawing Board", draw)

print("SMART DRAWING BOARD")
print("R = Red | G = Green | B = Blue | K = Black")
print("C = Clear | D = Detect Shapes")
print("S = Save | ESC = Exit")

while True:
    cv2.imshow("Smart Drawing Board", canvas)

    key = cv2.waitKey(1) & 0xFF

    if key in colors:
        color = colors[key]

    elif key == ord("c"):
        canvas[:] = 255

    elif key == ord("d"):
        detected = recognize_shapes(canvas)
        cv2.imshow("Shape Detection", detected)

    elif key == ord("s"):
        filename = (
            "drawing_" +
            datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".png"
        )

        cv2.imwrite(filename, canvas)
        print("Saved:", filename)

    elif key == 27:
        break

cv2.destroyAllWindows()
