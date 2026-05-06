# ──────────────────────────────────────────
#  CAMERA SETTINGS
# ──────────────────────────────────────────
FRAME_WIDTH  = 640
FRAME_HEIGHT = 480
FPS          = 30

# ──────────────────────────────────────────
#  DISTANCE ESTIMATION
#  Run calibrate.py once to get FOCAL_LENGTH
# ──────────────────────────────────────────
FOCAL_LENGTH       = 615.0   # pixels  ← replace after calibration
KNOWN_OBJECT_WIDTH = 30.0    # cm  (real-world width of target object)

# ──────────────────────────────────────────
#  AVOIDANCE THRESHOLDS (in cm)
# ──────────────────────────────────────────
DANGER_ZONE  = 40    # cm → Emergency stop + avoid NOW
CAUTION_ZONE = 80    # cm → Slow down, prepare to avoid
SAFE_ZONE    = 120   # cm → All clear, continue

# ──────────────────────────────────────────
#  SCREEN ZONES (divide frame into 3 columns)
#  Used to decide: avoid LEFT, RIGHT, or UP
# ──────────────────────────────────────────
LEFT_BOUNDARY  = FRAME_WIDTH // 3        # 213 px
RIGHT_BOUNDARY = (FRAME_WIDTH * 2) // 3  # 426 px

# ──────────────────────────────────────────
#  OBJECT DETECTION — HSV color range
#  Tune these for your obstacle color
# ──────────────────────────────────────────
LOWER_HSV = [100, 150, 50]   # Blue obstacle (default)
UPPER_HSV = [140, 255, 255]
MIN_CONTOUR_AREA = 800        # Ignore tiny blobs
