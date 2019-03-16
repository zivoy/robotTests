from ev3dev import ev3
from math import pi
from time import sleep
from enum import Enum

wheel_diameter = 5.6
robot_width = 11.6

wheel_circum = pi * wheel_diameter
robot_turn_circle = pi * robot_width


class Color(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    GREY = 'grey'
    BLACK = 'black'
    WHITE = 'white'


class Direction(Enum):
        RIGHT = 'right'
        LEFT = 'left'

        def __invert__(self):
            if self.value == Direction.LEFT:
                return Direction.RIGHT
            return Direction.LEFT

        def get_arm(self):
            if self.value == Direction.RIGHT:
                return -90
            return 90


def dist(list1, list2):
    return sum([(vi - vj) ** 2.0 for vi, vj in zip(list1, list2)])


def get_closest_color(color_measure):
    colors = {Color.RED: [225, 50, 50],
              Color.GREEN: [48, 155, 40],
              Color.BLUE: [50, 50, 85],
              Color.GREY: [220, 220, 220],
              Color.BLACK: [20, 20, 20],
              Color.WHITE: [255, 255, 255]}
    distances = [(dist(color, color_measure), name) for name, color in colors.items()]
    color = min(distances)[1]
    return color


class RobotHandler:
    def __init__(self, m1, m2, ar):
        self.m1 = ev3.LargeMotor(m1)
        self.m2 = ev3.LargeMotor(m2)
        self.ar = ev3.MediumMotor(ar)
        self.cl = ev3.ColorSensor()
        self.cl.mode = 'RGB-RAW'
        self.gy = ev3.GyroSensor()
        self.gy.mode = 'GYRO-CAL'
        self.gy.mode = 'GYRO-ANG'
        self.us = ev3.UltrasonicSensor()
        self.us.mode = 'US-DIST-CM'

    def get_orientation(self):
        return self.gy.value()

    def drive(self, forward, turn_deg=0, turn_dir=None, speed=200, wwr=True):

        wheel_travel_distance = robot_turn_circle * turn_deg / 360.0

        rotation_deg = wheel_travel_distance / wheel_circum * 360.0

        move_rot = float(forward) / wheel_circum * 360.0

        if turn_dir == Direction.RIGHT:
            r_rot = rotation_deg + move_rot
            l_rot = -rotation_deg + move_rot
            l_speed = speed * l_rot / max(1.0, r_rot)
            r_speed = speed
        elif turn_dir == Direction.LEFT:
            r_rot = -rotation_deg + move_rot
            l_rot = rotation_deg + move_rot
            l_speed = speed
            r_speed = speed * r_rot / max(1.0, l_rot)
        else:
            r_rot = move_rot
            l_rot = move_rot
            l_speed = speed
            r_speed = speed
        l_speed = max(1, l_speed)
        r_speed = max(1, r_speed)

        self.m1.run_to_rel_pos(position_sp=r_rot, speed_sp=r_speed)
        self.m2.run_to_rel_pos(position_sp=l_rot, speed_sp=l_speed)

        comp = 50.0
        if wwr:
            self.m1.wait_while('running', timeout=max(1.0, r_rot / r_speed * 1000.0 - comp))
            self.m2.wait_while('running', timeout=max(1.0, l_rot / l_speed * 1000.0 - comp))

    def stop_running(self):
        self.m1.stop(stop_action="brake")
        self.m2.stop(stop_action="brake")

    def return_colors(self):
        scale = [345.0, 324.0, 214.0]
        return [255.0 / s * self.cl.value(i) for i, s in enumerate(scale)]

    def scan(self, turn_speed=300):
        pos_cols = []
        ret_end = True
        for l in range(-8, 9):
            self.ar.run_to_abs_pos(position_sp=l * 10, speed_sp=turn_speed)
            sleep(.01+10/turn_speed)
            col_ret = get_closest_color((self.return_colors()))
            pos_cols.append((col_ret, l))
            if col_ret == Color.RED or col_ret == Color.BLUE:
                ret_end = False
                break
        if ret_end:
            self.ar.run_to_abs_pos(position_sp=-80, speed_sp=900)
            self.ar.run_to_abs_pos(position_sp=-80, speed_sp=100)
        return pos_cols

    def scan_handler(self):
        color_ran = self.scan()
        non_pass = []
        greens = []

        for col, pos in color_ran:
            if col not in (Color.WHITE, Color.GREY):
                '''if col == Color.GREEN and pos == 0:
                    self.get_into_pos()
                    return
                else:'''
                # return get_closest_color(col)
                if col == Color.GREEN:
                    # TODO: color handler
                    greens.append((pos, col))
                else:
                    self.stop_running()
                    non_pass.append(pos)
                    break
        if non_pass:
            return 'circle', non_pass
        elif greens:
            return Color.GREEN, greens
        else:
            return 'clear', color_ran

    def circle_navigate(self, dir_override):

        # self.drive(-2)
        # wheelArm = 85 #fix pos of arm guess 40
        # dire = ''

            # self.ar.run_to_abs_pos(position_sp=-wheelArm, speed_sp=100)
        # self.drive(0, 10, dire)
        print("ddir_over, ddire: ", dir_override)
        self.turn_around_sensor(dir_override)
        print("turned d_ arond")
        while get_closest_color(self.return_colors()) != Color.BLUE:
            print("i'm not blue")
            self.drive(1, 2, dir_override, 50, True)
        #
        dir_mult = 1 if dir_override == Direction.RIGHT else -1
        while dir_mult * self.get_orientation() < 89:  # TODO: reset direction to 0 when going back
            curr_col = get_closest_color(self.return_colors())
            if curr_col == Color.BLUE:
                print("blue")
                self.drive(4,  speed=100, wwr=True)
            elif curr_col in (Color.WHITE, Color.GREY):
                print("wg")
                self.drive(1, 3, dir_override, speed=100, wwr=True)
            elif curr_col == Color.RED:
                self.drive(-10, wwr=True)
                self.drive(5, 10, ~dir_override, wwr=True)
            else:
                self.drive(-1, wwr=True)
                print(curr_col, 'curr color')

        self.stop_running()
        final_dist = self.to_wall()
        self.drive(-9, 0, '', 200, True)
        self.drive(5, 90, ~dir_override, 150, True)
        return final_dist

    def turn_around_sensor(self, dir_override):

        sensor_pos = self.ar.position
        if abs(sensor_pos) > 88:
            return
        print(sensor_pos)

        travel_degrees = (90.0 - abs(sensor_pos)) ** 1.1 / 141 * .75  # multiplyer
        print(travel_degrees)

        drive_compensate = robot_turn_circle * travel_degrees / 360.0
        #        print(drive_compensate)

        '''
        if sensor_pos < 0:
            direct = (Direction.LEFT, -90)
        elif sensor_pos > 0:
            direct = (Direction.RIGHT, 90)
        elif sensor_pos == 0:

        if dir_override == '':
            turn_side = direct[0]
        else:
            turn_side = dir_override'''

        self.ar.run_to_abs_pos(position_sp=dir_override.get_arm(), speed_sp=50)
        print(~dir_override, dir_override.get_arm(), drive_compensate)
        self.drive(drive_compensate, travel_degrees, ~dir_override, 100, wwr=True)

    def get_into_pos(self, to_edge, final=False):
        self.drive(to_edge - 7.0, 0, '', 200, True)
        curr_or = self.get_orientation()
        end_pos = 0 if final else 180
        self.drive(0, end_pos - curr_or, Direction.RIGHT, 180, True)

    def to_wall(self):
        return self.us.value() / 10.0
