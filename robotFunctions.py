import numpy as np
from ev3dev import ev3

wheel_diameter = 5.6
robot_width = 11.6

multiplier = 1.0

def get_closest_color(color_measure):
    colorm = color_measure[:3]
    colors = {'red': np.array([255, 0, 0]),
              'green': np.array([0, 255, 0]),
              'blue': np.array([0, 0, 255]),
              'grey': np.array([230, 230, 230]),
              'black': np.array([0, 0, 0]),
              'white': np.array([255, 255, 255])}
    distances = [(np.linalg.norm(color - colorm), name) for name, color in colors.items()]
    return min(distances)[1]

class mover:
    def __init__(self, m1, m2):
        self.m1 = ev3.LargeMotor(m1)
        self.m2 = ev3.LargeMotor(m2)
    def drive(self, forward, turnDeg=0, turnDir=True, speed=200):
        wheel_circum = np.pi * wheel_diameter * multiplier

        robot_turn_circle = np.pi * robot_width

        wheel_travel_distance = robot_turn_circle * turnDeg / 360.0

        rotation_deg = wheel_travel_distance / wheel_circum * 360

        direction = 1.0 if turnDir else -1.0

        moveRot = forward / wheel_circum * 360

        self.m1.run_to_rel_pos(position_sp=rotation_deg * direction + moveRot, speed_sp=speed)
        self.m2.run_to_rel_pos(position_sp=- rotation_deg * direction + moveRot, speed_sp=speed)

        self.m1.wait_while('running')
        self.m2.wait_while('running')
