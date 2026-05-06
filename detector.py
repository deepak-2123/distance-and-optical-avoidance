import cv2
import numpy as np
import config

# Convert config lists to numpy arrays
LOWER = np.array(config.LOWER_HSV)
UPPER = np.array(config.UPPER_HSV)


def detect_objects(frame):
    """
    Detect obstacles in the frame using HSV color masking.

    Returns list of detections:
    Each detection = {
        'cx': center x,
        'cy': center y,
        'pixel_width': width in pixels,
        'bbox': (x, y, w, h),
        'position': 'LEFT' | 'CENTER' | 'RIGHT'
    }
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Color mask
    mask = cv2.inRange(hsv, LOWER, UPPER)

    # Clean up noise
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Find all contours
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    detections = []

    for cnt in contours:
        if cv2.contourArea(cnt) < config.MIN_CONTOUR_AREA:
            continue  # skip noise

        x, y, w, h = cv2.boundingRect(cnt)
        cx = x + w // 2
        cy = y + h // 2

        # Determine screen zone
        if cx < config.LEFT_BOUNDARY:
            zone = "LEFT"
        elif cx > config.RIGHT_BOUNDARY:
            zone = "RIGHT"
        else:
            zone = "CENTER"

        detections.append({
            "cx":          cx,
            "cy":          cy,
            "pixel_width": w,
            "bbox":        (x, y, w, h),
            "position":    zone
        })

    return detections


def draw_detections(frame, detections, distances):
    """
    Annotate the frame with bounding boxes, distances, zones.
    """
    h, w = frame.shape[:2]

    # Draw zone dividers
    cv2.line(frame, (config.LEFT_BOUNDARY, 0),
             (config.LEFT_BOUNDARY, h), (200, 200, 200), 1)
    cv2.line(frame, (config.RIGHT_BOUNDARY, 0),
             (config.RIGHT_BOUNDARY, h), (200, 200, 200), 1)

    for i, det in enumerate(detections):
        x, y, bw, bh = det["bbox"]
        dist = distances[i] if i < len(distances) else None

        # Color based on distance
        if dist is None:
            color = (200, 200, 200)
        elif dist < config.DANGER_ZONE:
            color = (0, 0, 255)    # Red  = DANGER
        elif dist < config.CAUTION_ZONE:
            color = (0, 165, 255)  # Orange = CAUTION
        else:
            color = (0, 255, 0)    # Green = SAFE

        cv2.rectangle(frame, (x, y), (x + bw, y + bh), color, 2)
        cv2.circle(frame, (det["cx"], det["cy"]), 4, color, -1)

        label = f"{det['position']}"
        if dist:
            label += f" | {dist:.1f}cm"
        cv2.putText(frame, label, (x, y - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

    return frame
