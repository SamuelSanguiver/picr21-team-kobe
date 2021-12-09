from picr21teamkobe.communication import serialcomms
import math
import cv2
from picr21teamkobe.imageprocessing import camera_config

wheel_angle_1 = 240
wheel_angle_2 = 120
wheel_angle_3 = 0

ser = serialcomms.Connection('/dev/ttyACM0')
#processor = ip.ProcessFrames(False)
camera = camera_config.Config()


def stop():
    send_speeds([0, 0, 0, 0])


def move(moving_speed, thrower_speed, direction):
    speeds = get_speeds(moving_speed, thrower_speed, direction)
    send_speeds(speeds)


def get_speeds(moving_speed, thrower_speed, direction):
    speeds = [0, 0, 0, 0]
    speeds[0] = int(calc_wheel_speed(moving_speed, direction, wheel_angle_1))
    speeds[1] = int(calc_wheel_speed(moving_speed, direction, wheel_angle_2))
    speeds[2] = int(calc_wheel_speed(moving_speed, direction, wheel_angle_3))
    speeds[3] = thrower_speed
    return speeds


def send_speeds(speeds):
    print("Sending: " + str(speeds))
    # order: motor1, motor2, motor3, thrower, failsafe
    ser.write_command(speeds[0], speeds[1], speeds[2], speeds[3], 0)


def calc_wheel_speed(moving_speed, direction, wheel_angle):
    wheel_speed = moving_speed * math.cos(math.radians(direction - wheel_angle))
    return wheel_speed


def spin_right(speed):
    send_speeds([-30, -30, -30, 0])


def spin_left(speed):
    send_speeds([15, 15, 15, 0])


def keyboard_control():
    cv2.namedWindow("Controller")
    # print("distance", basket_distance*100)
    moving_speed = 15
    throwing_speed = 1400
    while True:
        #count, y, x, center_x, center_y, basket_distance, floor_area = processor.ProcessFrame(camera.pipeline,
                                                                                              #camera.camera_x,
                                                                                              #camera.camera_y)
        #print("distance", basket_distance * 100)
        #move(0, throwing_speed, 0)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("w"):
            print("Moving forward.")
            move(moving_speed, 0, 330)
        if key == ord("d"):
            print("Moving right.")
            move(moving_speed, 0, 240)
        if key == ord("s"):
            print("Moving backwards.")
            move(moving_speed, 0, 150)
        if key == ord("a"):
            print("Moving left.")
            move(moving_speed, 0, 60)
        if key == ord("e"):
            print("Spinning right.")
            spin_right(moving_speed)
        if key == ord("q"):
            print("Spinning left.")
            spin_left(moving_speed)
        if key == ord("t"):
            print("Throwing.")
            move(0, throwing_speed, 0)
        if key == ord("c"):
            print("Stopping.")
            stop()
        if key == ord("x"):
            print("Shutting down.")
            stop()
            break


keyboard_control()

cv2.destroyAllWindows()
