import config


# ── Avoidance state names ──────────────────
SAFE      = "SAFE"
SLOW_DOWN = "SLOW_DOWN"
AVOID_LEFT    = "AVOID_LEFT"
AVOID_RIGHT   = "AVOID_RIGHT"
AVOID_UP      = "AVOID_UP"
EMERGENCY_STOP = "EMERGENCY_STOP"


def decide_action(closest_detection, closest_distance):
    """
    Given the closest obstacle's info, decide what the drone should do.

    Logic:
      - No obstacle         → SAFE (continue forward)
      - dist > SAFE_ZONE    → SAFE
      - dist > CAUTION_ZONE → SLOW_DOWN
      - dist > DANGER_ZONE  → Steer away (based on obstacle position)
      - dist ≤ DANGER_ZONE  → EMERGENCY_STOP + hard avoid
    """
    if closest_detection is None or closest_distance is None:
        return SAFE, "No obstacle — path clear"

    dist     = closest_distance
    position = closest_detection["position"]  # LEFT / CENTER / RIGHT

    # ── Far away ─────────────────────────────
    if dist > config.SAFE_ZONE:
        return SAFE, f"Clear ({dist:.1f}cm)"

    # ── Medium distance ───────────────────────
    if dist > config.CAUTION_ZONE:
        return SLOW_DOWN, f"Caution {dist:.1f}cm — slowing"

    # ── Close — steer based on object position ─
    if dist > config.DANGER_ZONE:
        if position == "LEFT":
            return AVOID_RIGHT, f"Obstacle LEFT at {dist:.1f}cm → Steer RIGHT"
        elif position == "RIGHT":
            return AVOID_LEFT, f"Obstacle RIGHT at {dist:.1f}cm → Steer LEFT"
        else:
            # CENTER obstacle → go up
            return AVOID_UP, f"Obstacle CENTER at {dist:.1f}cm → Climb UP"

    # ── Danger zone — emergency ────────────────
    return EMERGENCY_STOP, f"DANGER {dist:.1f}cm — EMERGENCY STOP!"
