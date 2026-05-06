"""
Run this ONCE with your drone at a KNOWN distance.
Hold the drone at exactly KNOWN_DISTANCE cm from the camera.
The script prints your focal length — paste it into main.py.
"""

import cv2
import numpy as np
from picamera2 import Picamera2
from detector import detect_drone

KNOWN_DISTANCE = 50.0   # cm — drone is THIS far from camera
KNOWN_WIDTH    = 20.0   # cm — width of colored marker on drone

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(
    main={"format": "BGR888", "size": (640, 480)}))
picam2.start()

print("=== CALIBRATION MODE ===")
print(f"Hold drone at exactly {KNOWN_DISTANCE} cm. Press 'c' to capture.")

while True:
    frame = picam2.capture_array()
    _, _, pixel_width, annotated = detect_drone(frame.copy())

    cv2.imshow("Calibrate", annotated)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c') and pixel_width:
        focal_length = (pixel_width * KNOWN_DISTANCE) / KNOWN_WIDTH
        print(f"\n✅ Focal Length = {focal_length:.2f}")
        print("Paste this value into main.py → FOCAL_LENGTH variable")
        break
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
picam2.stop()
