"""
Supports two modes:
  1. DroneKit / MAVLink  → for Pixhawk flight controllers
  2. Simulated (print)   → for testing without hardware
Set USE_MAVLINK = True if you have a Pixhawk connected via UART.
"""

from avoidance import (SAFE, SLOW_DOWN, AVOID_LEFT,
                       AVOID_RIGHT, AVOID_UP, EMERGENCY_STOP)

USE_MAVLINK = False   # ← Set True for real Pixhawk

# ── MAVLink / DroneKit setup ──────────────────────────────────
if USE_MAVLINK:
    from dronekit import connect, VehicleMode
    from pymavlink import mavutil

    vehicle = connect('/dev/ttyAMA0', baud=57600, wait_ready=True)
    print(f"[FC] Connected: {vehicle.version}")


def send_velocity(vx, vy, vz):
    """Send NED velocity command (m/s) via MAVLink."""
    if not USE_MAVLINK:
        print(f"  [SIM] Velocity → vx={vx} vy={vy} vz={vz} m/s")
        return

    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0, 0, 0,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111,
        0, 0, 0,
        vx, vy, vz,
        0, 0, 0,
        0, 0
    )
    vehicle.send_mavlink(msg)
    vehicle.flush()


def execute_action(action, log_msg):
    """
    Map avoidance decisions to velocity commands.

    NED Frame:
      +X = North (forward)
      +Y = East  (right)
      -Z = Up
    """
    print(f"[ACTION] {action} | {log_msg}")

    if action == SAFE:
        send_velocity(1.0,  0.0,  0.0)   # Move forward normally

    elif action == SLOW_DOWN:
        send_velocity(0.3,  0.0,  0.0)   # Slow forward

    elif action == AVOID_LEFT:
        send_velocity(0.0, -1.0,  0.0)   # Strafe left

    elif action == AVOID_RIGHT:
        send_velocity(0.0,  1.0,  0.0)   # Strafe right

    elif action == AVOID_UP:
        send_velocity(0.0,  0.0, -1.0)   # Climb up (NED: -Z = up)

    elif action == EMERGENCY_STOP:
        send_velocity(0.0,  0.0,  0.0)   # STOP all movement
        if USE_MAVLINK:
            vehicle.mode = VehicleMode("LOITER")


def shutdown():
    if USE_MAVLINK:
        vehicle.close()
    print("[FC] Shutdown")
