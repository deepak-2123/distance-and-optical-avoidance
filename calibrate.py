"""
STEP 1: Place a known object (width = KNOWN_OBJECT_WIDTH cm)
        exactly KNOWN_DISTANCE cm in front of the drone camera.
STEP 2: Run this script.
STEP 3: Press 'c' to capture when the object is clearly boxed.
STEP 4: Copy the printed FOCAL_LENGTH into config.py
"""

import cv2
import numpy as np
from picamera2 import Picamera2
from detector import detect_objects

KNOWN_DISTANCE    = 60.0   # cm — object is this far from camera
KNOWN_OBJECT_WIDTH = 30.0  # cm — real width of the object

print("=== CALIBRATION ===")
print(f"Place object at exactly {KNOWN_DISTANCE}cm → Press 'c' to capture")

cam = Picamera2()
cam.configure(cam.create_preview_configuration(
    main={"format": "BGR888", "size": (640, 480)}))
cam.start()

while True:
    frame = cam.capture_array()
    detections = detect_objects(frame.copy())

    for d in detections:
        x, y, w, h = d["bbox"]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(frame, f"W={d['pixel_width']}px",
                    (x, y-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    cv2.putText(frame, "Press 'c' to calibrate, 'q' to quit",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
    cv2.imshow("Calibrate", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c') and detections:
        pw = detections[0]["pixel_width"]
        focal = (pw * KNOWN_DISTANCE) / KNOWN_OBJECT_WIDTH
        print(f"\n✅ Pixel Width   : {pw} px")
        print(f"✅ FOCAL_LENGTH  : {focal:.2f}")
        print(f"\n→ Open config.py and set: FOCAL_LENGTH = {focal:.2f}")
        break
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
cam.stop()
