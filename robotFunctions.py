from ev3dev import ev3
from math import pi

wheel_diameter = 5.6
robot_width = 11.6

multiplier = 1.0

def dist(list1, list2):
    return sum([(vi-vj)**2.0 for vi, vj in zip(list1, list2)])

def get_closest_color(color_measure):
    colors = {'red': [255, 0, 0],
              'green': [0, 255, 0],
              'blue': [0, 0, 255],
              'grey': [230, 230, 230],
              'black': [0, 0, 0],
              'white': [255, 255, 255]}
    distances = [(dist(color, color_measure), name) for name, color in colors.items()]
    color = min(distances)[1]
    print(color)
    return color

class mover:
    def __init__(self, m1, m2):
        self.m1 = ev3.LargeMotor(m1)
        self.m2 = ev3.LargeMotor(m2)
    def drive(self, forward, turnDeg=0, turnDir=True, speed=200):
        wheel_circum = pi * wheel_diameter * multiplier

        robot_turn_circle = pi * robot_width

        wheel_travel_distance = robot_turn_circle * turnDeg / 360.0

        rotation_deg = wheel_travel_distance / wheel_circum * 360

        direction = 1.0 if not turnDir else -1.0

        moveRot = forward / wheel_circum * 360

        if turnDir == 'right':
            rRot = 
            lRot

        self.m1.run_to_rel_pos(position_sp=rotation_deg * direction + moveRot, speed_sp=speed)
        self.m2.run_to_rel_pos(position_sp=- rotation_deg * direction + moveRot, speed_sp=speed)

        self.m1.wait_while('running')
        self.m2.wait_while('running')
