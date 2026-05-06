from picamera2 import Picamera2
import config

class DroneCamera:
    def __init__(self):
        self.cam = Picamera2()
        self.cam.configure(
            self.cam.create_preview_configuration(
                main={
                    "format": "BGR888",
                    "size": (config.FRAME_WIDTH, config.FRAME_HEIGHT)
                }
            )
        )

    def start(self):
        self.cam.start()
        print("[Camera] Started")

    def get_frame(self):
        return self.cam.capture_array()

    def stop(self):
        self.cam.stop()
        print("[Camera] Stopped")
