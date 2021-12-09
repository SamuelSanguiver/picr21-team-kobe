from picr21teamkobe.communication import serialcomms
import math

ser = serialcomms.Connection('/dev/ttyACM0')


# Order: motor1, motor2, motor3, thrower, failsafe
def move_omni(x_speed, y_speed, rot_speed, thrower):
    speed = [0, 0, 0, 0]

    move_speed = math.sqrt(x_speed ** 2 + y_speed ** 2)
    # print("move_speed", move_speed)
    direction = math.atan2(x_speed, y_speed)

    speed[0] = int(wheel_speed(move_speed, direction, 240)) + rot_speed
    speed[1] = int(wheel_speed(move_speed, direction, 120)) + rot_speed
    speed[2] = int(wheel_speed(move_speed, direction, 0)) + rot_speed
    speed[3] = int(thrower)

    ser.write_command(speed[0], speed[1], speed[2], speed[3], 0)


def wheel_speed(speed, direction, angle):
    wheel_linear_velocity = speed * math.cos(direction - math.radians(angle + 30))
    return wheel_linear_velocity


def spin_left(speed):
    ser.write_command(speed[0], speed[1], speed[2], speed[3], 0)


def spin_right(speed):
    ser.write_command(speed[0], speed[1], speed[2], speed[3], 0)


def stop():
    speed = [0, 0, 0, 0]
    ser.write_command(speed[0], speed[1], speed[2], speed[3], 0)
