from ev3dev import ev3
from math import pi
from time import sleep

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


class robotHandler:
    def __init__(self, m1, m2, ar):
        self.m1 = ev3.LargeMotor(m1)
        self.m2 = ev3.LargeMotor(m2)
        self.ar = ev3.MediumMotor(ar)
        self.cl = ev3.ColorSensor()
        self.cl.mode='RGB-RAW'
        self.gy = ev3.GyroSensor()
        self.gy.mode='GYRO-CAL'
        self.gy.mode='GYRO-ANG'

    def getOrientation(self):
        return self.gy.value()

    def drive(self, forward, turnDeg=0, turnDir='', speed=200, wwr=False):
        
        wheel_circum = pi * wheel_diameter * multiplier

        robot_turn_circle = pi * robot_width

        wheel_travel_distance = robot_turn_circle * turnDeg / 360.0

        rotation_deg = wheel_travel_distance / wheel_circum * 360.0

        moveRot = float(forward) / wheel_circum * 360.0

        if turnDir == 'right':
            rRot = rotation_deg + moveRot
            lRot = -rotation_deg + moveRot
            lSpeed = speed * lRot / rRot
            rSpeed = speed
        elif turnDir == 'left':
            rRot = -rotation_deg + moveRot
            lRot = rotation_deg + moveRot
            lSpeed = speed
            rSpeed = speed * rRot / lRot
        else:            
            rRot = moveRot
            lRot = moveRot
            lSpeed = speed
            rSpeed = speed

        self.m1.run_to_rel_pos(position_sp=rRot, speed_sp=rSpeed)
        self.m2.run_to_rel_pos(position_sp=lRot, speed_sp=lSpeed)

        comp = 50.0
        if wwr:  
            self.m1.wait_while('running', timeout=rRot/rSpeed*1000.0 - comp)
            self.m2.wait_while('running', timeout=lRot/lSpeed*1000.0 - comp)

    def stopRunning(self):
        self.m1.stop(stop_action="brake")
        self.m2.stop(stop_action="brake")

    def returnColors(self):
        return [self.cl.value(i) for i in range(3)]

    def scan(self, turn_speed=300):
        posCols = []
        for l in range(-8, 9):
            self.ar.run_to_abs_pos(position_sp=l*10, speed_sp=turn_speed)
            sleep(.04)
            posCols.append((self.returnColors(), l))
        self.ar.run_to_abs_pos(position_sp=-80, speed_sp=900)
        self.ar.run_to_abs_pos(position_sp=-80, speed_sp=100)
        return posCols

    def scanHandler(self):
        colorRan = self.scan()
        nonPass = []
        for col, pos in colorRan:
            if get_closest_color(col) != 'white':
                if get_closest_color(col) == 'green' and (pos == 8 or pos == 9):
                    self.getIntoPos()
                    return
                else:
                    #return get_closest_color(col)
                    self.stopRunning()
                    nonPass.append(pos)
        if nonPass != []:
            self.circleNavigate(nonPass)
        return nonPass

    def circleNavigate(self, positions):
        pass

    def getIntoPos(self, final=False):
        self.drive(20, 0, '', 200, True)
        currOr = self.getOrientation()
        endPos = 0 if final else 180
        self.drive(0, endPos-currOr, 'right', 180, True)
        runAgain = not final
        return runAgain
