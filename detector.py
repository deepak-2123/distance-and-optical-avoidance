import cv2
import numpy as np

# ─── Tune these HSV values for your drone's marker color ───
LOWER_COLOR = np.array([100, 150, 50])   # Blue marker (example)
UPPER_COLOR = np.array([140, 255, 255])

MIN_AREA = 500  # Ignore small blobs (noise)

def detect_drone(frame):
    """
    Detect drone in frame using color masking.
    Returns: (center_x, center_y, pixel_width, annotated_frame)
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Color mask
    mask = cv2.inRange(hsv, LOWER_COLOR, UPPER_COLOR)

    # Noise removal
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None, None, None, frame

    # Pick the largest contour
    largest = max(contours, key=cv2.contourArea)

    if cv2.contourArea(largest) < MIN_AREA:
        return None, None, None, frame

    x, y, w, h = cv2.boundingRect(largest)
    cx, cy = x + w // 2, y + h // 2

    # Draw on frame
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
    cv2.putText(frame, "DRONE", (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return cx, cy, w, frame
