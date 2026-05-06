from picamera2 import Picamera2
import config
import cv2  # ← ADD THIS

class DroneCamera:
    def __init__(self):
        self.cam = Picamera2()
        self.cam.configure(
            self.cam.create_preview_configuration(
                main={
                    "format": "RGB888",    # ← Change BGR888 to RGB888
                    "size": (config.FRAME_WIDTH, config.FRAME_HEIGHT)
                }
            )
        )

    def start(self):
        self.cam.start()
        print("[Camera] Started")

    def get_frame(self):
        frame = self.cam.capture_array()
        return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # ← ADD THIS FIX

    def stop(self):
        self.cam.stop()
        print("[Camera] Stopped")
