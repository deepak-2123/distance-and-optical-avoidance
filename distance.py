import config


def calculate_distance(pixel_width):
    """
    Pinhole camera model:
        Distance = (Real Width × Focal Length) / Pixel Width
    
    Returns distance in cm, or None if pixel_width is zero.
    """
    if pixel_width <= 0:
        return None
    return (config.KNOWN_OBJECT_WIDTH * config.FOCAL_LENGTH) / pixel_width


def get_distances(detections):
    """
    Calculate distances for all detected objects.
    Returns list of distances in same order as detections.
    """
    return [calculate_distance(d["pixel_width"]) for d in detections]


def get_closest(detections, distances):
    """
    Find the single closest (most dangerous) obstacle.
    Returns (detection, distance) or (None, None).
    """
    valid = [
        (det, dist)
        for det, dist in zip(detections, distances)
        if dist is not None
    ]
    if not valid:
        return None, None

    return min(valid, key=lambda x: x[1])
