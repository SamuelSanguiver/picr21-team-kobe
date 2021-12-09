from inputs import get_gamepad
import math
import threading


class Values:
    def __init__(self, x, y, a, y_btn, rx, start, stop, right_trigger, b) -> None:
        self.x = x
        self.y = y
        self.a = a
        self.y_btn = y_btn
        self.rx = rx
        self.start = stop
        self.stop = start
        self.right_trigger = right_trigger
        self.b = b


class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):
        self.left_joystick_y = 0
        self.left_joystick_x = 0
        self.right_joystick_y = 0
        self.right_joystick_x = 0
        self.left_trigger = 0
        self.right_trigger = 0
        self.left_bumper = 0
        self.right_bumper = 0
        self.a = 0
        self.x = 0
        self.y = 0
        self.b = 0
        self.left_thumb = 0
        self.right_thumb = 0
        self.back = 0
        self.start = 0
        self.left_d_pad = 0
        self.right_d_pad = 0
        self.up_d_pad = 0
        self.down_d_pad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def read(self):
        x = self.left_joystick_x
        y = self.left_joystick_y
        a = self.a
        y_btn = self.y
        rx = self.right_joystick_x
        start = self.start
        stop = self.back
        right_trigger = self.right_trigger
        b = self.b
        return Values(x, y, a, y_btn, rx, start, stop, right_trigger, b)

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.left_joystick_y = event.state / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.left_joystick_x = event.state / XboxController.MAX_JOY_VAL
                elif event.code == 'ABS_RX':
                    self.right_joystick_x = event.state / XboxController.MAX_JOY_VAL
                elif event.code == 'BTN_SOUTH':
                    self.a = event.state
                elif event.code == 'BTN_NORTH':
                    self.y = event.state
                elif event.code == 'BTN_WEST':
                    self.x = event.state
                elif event.code == 'BTN_EAST':
                    self.b = event.state
                elif event.code == 'BTN_SELECT':
                    self.back = event.state
                elif event.code == 'BTN_START':
                    self.start = event.state
                elif event.code == 'ABS_RZ':
                    self.right_trigger = event.state / XboxController.MAX_TRIG_VAL  # normalize between 0 and 1


if __name__ == '__main__':
    joy = XboxController()
    while True:
        print(joy.read())
