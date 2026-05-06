import cv2
import time

from camera         import DroneCamera
from detector       import detect_objects, draw_detections
from distance       import get_distances, get_closest
from avoidance      import decide_action
from flight_control import execute_action, shutdown

SHOW_DISPLAY = True    # Set False when running headless on drone

def main():
    cam = DroneCamera()
    cam.start()

    print("=" * 50)
    print("  DRONE OBSTACLE AVOIDANCE SYSTEM — RUNNING")
    print("  Press 'q' to quit")
    print("=" * 50)

    loop_count = 0

    try:
        while True:
            loop_start = time.time()

            # ── 1. Capture frame ──────────────────────
            frame = cam.get_frame()

            # ── 2. Detect obstacles ───────────────────
            detections = detect_objects(frame)

            # ── 3. Calculate distances ────────────────
            distances = get_distances(detections)

            # ── 4. Find closest threat ────────────────
            closest_det, closest_dist = get_closest(detections, distances)

            # ── 5. Decide avoidance action ────────────
            action, log_msg = decide_action(closest_det, closest_dist)

            # ── 6. Execute flight command ─────────────
            execute_action(action, log_msg)

            # ── 7. Display (optional) ─────────────────
            if SHOW_DISPLAY:
                annotated = draw_detections(frame, detections, distances)

                # HUD overlay
                fps = 1.0 / max(time.time() - loop_start, 0.001)
                cv2.putText(annotated, f"FPS: {fps:.1f}",
                            (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (255, 255, 255), 2)
                cv2.putText(annotated, f"Action: {action}",
                            (10, 55), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (0, 255, 255), 2)
                if closest_dist:
                    cv2.putText(annotated,
                                f"Closest: {closest_dist:.1f} cm",
                                (10, 85), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 200, 255), 2)

                cv2.imshow("Drone View", annotated)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            loop_count += 1

    except KeyboardInterrupt:
        print("\n[Main] Interrupted by user")

    finally:
        cv2.destroyAllWindows()
        cam.stop()
        shutdown()
        print(f"[Main] Total frames processed: {loop_count}")

if __name__ == "__main__":
    main()
