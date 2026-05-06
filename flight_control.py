"""
Uses pymavlink directly (DroneKit is broken on Python 3.10+)
Set USE_MAVLINK = True when connected to Pixhawk via UART
"""
import time
from avoidance import (SAFE, SLOW_DOWN, AVOID_LEFT,
                       AVOID_RIGHT, AVOID_UP, EMERGENCY_STOP)

USE_MAVLINK = False   # ← Set True for real Pixhawk

if USE_MAVLINK:
    from pymavlink import mavutil

    master = mavutil.mavlink_connection(
        '/dev/ttyAMA0',
        baud=57600
    )
    master.wait_heartbeat()
    print(f"[FC] Heartbeat from system "
          f"{master.target_system} component "
          f"{master.target_component}")


def send_velocity(vx, vy, vz):
    """Send NED velocity (m/s) via MAVLink SET_POSITION_TARGET_LOCAL_NED"""
    if not USE_MAVLINK:
        print(f"  [SIM] vx={vx:+.1f}  vy={vy:+.1f}  vz={vz:+.1f} m/s")
        return

    master.mav.set_position_target_local_ned_send(
        0,
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111,   # velocity only mask
        0, 0, 0,              # position (ignored)
        vx, vy, vz,           # velocity
        0, 0, 0,              # acceleration (ignored)
        0, 0                  # yaw, yaw_rate (ignored)
    )


def execute_action(action, log_msg):
    print(f"[ACTION] {action} | {log_msg}")

    if action == SAFE:
        send_velocity(1.0,  0.0,  0.0)

    elif action == SLOW_DOWN:
        send_velocity(0.3,  0.0,  0.0)

    elif action == AVOID_LEFT:
        send_velocity(0.0, -1.0,  0.0)

    elif action == AVOID_RIGHT:
        send_velocity(0.0,  1.0,  0.0)

    elif action == AVOID_UP:
        send_velocity(0.0,  0.0, -1.0)   # NED: -Z = Up

    elif action == EMERGENCY_STOP:
        send_velocity(0.0,  0.0,  0.0)
        if USE_MAVLINK:
            # Switch to LOITER mode via MAVLink
            master.mav.command_long_send(
                master.target_system,
                master.target_component,
                mavutil.mavlink.MAV_CMD_DO_SET_MODE,
                0, 1, 5, 0, 0, 0, 0, 0    # 5 = LOITER
            )


def shutdown():
    if USE_MAVLINK:
        send_velocity(0, 0, 0)
    print("[FC] Shutdown complete")
