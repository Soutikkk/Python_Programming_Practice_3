import cv2
import numpy as np

# Create a black image
img = np.zeros((500, 500, 3), dtype=np.uint8)

# Center of the scanner
center = (250, 250)
max_radius = 180

# Draw concentric circles
for r in range(40, max_radius + 1, 20):
    cv2.circle(img, center, r, (255, 255, 0), 2)

# Draw radial lines
for angle in range(0, 360, 15):
    x = int(center[0] + max_radius * np.cos(np.radians(angle)))
    y = int(center[1] + max_radius * np.sin(np.radians(angle)))
    cv2.line(img, center, (x, y), (0, 255, 255), 1)

# Outer border
cv2.circle(img, center, max_radius, (0, 255, 0), 2)

# Center point
cv2.circle(img, center, 5, (0, 0, 255), -1)

# Title
cv2.putText(
    img,
    "IRIS SCAN",
    (165, 455),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0),
    2,
)

# Display the image
cv2.imshow("Iris Scanner Simulation", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
