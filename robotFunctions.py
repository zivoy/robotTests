from ev3dev import ev3
from math import pi
from time import sleep

wheel_diameter = 5.6
robot_width = 11.6


wheel_circum = pi * wheel_diameter
robot_turn_circle = pi * robot_width

def dist(list1, list2):
    return sum([(vi-vj)**2.0 for vi, vj in zip(list1, list2)])


def get_closest_color(color_measure):

    colors = {'red': [225, 50, 50],
              'green': [48, 155, 40],
              'blue': [50, 50, 85],
              'grey': [220, 220, 220],
              'black': [20, 20, 20],
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
        self.us = ev3.UltrasonicSensor()
        self.us.mode='US-DIST-CM'

    def getOrientation(self):
        return self.gy.value()

    def drive(self, forward, turn_deg=0, turn_dir='', speed=200, wwr=False):

        wheel_travel_distance = robot_turn_circle * turn_deg / 360.0

        rotation_deg = wheel_travel_distance / wheel_circum * 360.0

        moveRot = float(forward) / wheel_circum * 360.0

        if turn_dir == 'right':
            rRot = rotation_deg + moveRot
            lRot = -rotation_deg + moveRot
            lSpeed = speed * lRot / rRot
            rSpeed = speed
        elif turn_dir == 'left':
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
        scale = [345.0, 324.0, 214.0]
        return [255.0 / s * self.cl.value(i) for i, s in enumerate(scale)]

    def scan(self, turn_speed=300):
        posCols = []
        retEnd = True
        for l in range(-8, 9):
            self.ar.run_to_abs_pos(position_sp=l*10, speed_sp=turn_speed)
            sleep(.04)
            colRet = get_closest_color((self.returnColors()))
            posCols.append(colRet, l)
            if colRet == 'red' or colRet == 'blue':
                retEnd = False
                break
        if retEnd:
            self.ar.run_to_abs_pos(position_sp=-80, speed_sp=900)
            self.ar.run_to_abs_pos(position_sp=-80, speed_sp=100)
        return posCols

    def scanHandler(self):
        colorRan = self.scan()
        nonPass = []
        greens = []
        for col, pos in colorRan:
            if col != 'white' or col != 'gray':
                '''if col == 'green' and pos == 0:
                    self.getIntoPos()
                    return
                else:'''
                    #return get_closest_color(col)
                if col == 'green':
                    #TODO: color handler
                    greens.append((pos, col))
                else:
                    self.stopRunning()
                    nonPass.append(pos)
                    break
        if nonPass != []:
            return 'circle', nonPass
        elif greens!=[]:
            return 'green', greens
        else:
            return 'clear', colorRan

    def circleNavigate(self, dirOverried=''):
        startRot = self.getOrientation()
        #self.drive(-2)
        #wheelArm = 85 #fix pos of arm guess 40
        #dire = ''
        if dirOverried!='':
            dire=dirOverried
        elif self.ar.position > 0: #on left
            dire = 'right'
            #self.ar.run_to_abs_pos(position_sp=wheelArm, speed_sp=100)
        else:
            dire = 'left'
            #self.ar.run_to_abs_pos(position_sp=-wheelArm, speed_sp=100)
        #self.drive(0, 10, dire)
        self.turnAroundSensor(dirOverried)

        while get_closest_color(self.returnColors())!= 'blue':
            self.drive(2, speed=50)

        while abs(self.getOrientation()-startRot)<90:
            currCol = get_closest_color(self.returnColors())
            if currCol == 'blue':
                self.drive(4, speed=100, wwr=True)
            if currCol == 'white' or currCol == 'gray':
                self.drive(0, 3, dire, 100, True)

        self.stopRunning()
        finalDist = self.toWall()
        self.drive(-6, 0, '', 200, True)
        breakDir = 'left' if dire == 'right' else 'right'
        self.drive(0, 90, breakDir, 150, True)
        return finalDist

    def turnAroundSensor(self, dir_override=''):
        sensor_pos = self.ar.position
#        print(sensor_pos)
#        print(travel_degrees)
        travel_degrees = 90.0 - abs(sensor_pos) * .85  # multiplyer
        drive_compensate = robot_turn_circle * travel_degrees / 360.0
#        print(drive_compensate)

        if sensor_pos < 0:
            direct = ('left', -90)
        elif sensor_pos > 0:
            direct = ('right', 90)

        if dir_override == '':
            turn_side = direct[0]
        else:
            turn_side = dir_override

        self.drive(drive_compensate, travel_degrees, turn_side, 100)
        self.ar.run_to_abs_pos(position_sp=direct[1], speed_sp=50)

    def getIntoPos(self, toEdge, final=False):
        self.drive(toEdge-7.0, 0, '', 200, True)
        currOr = self.getOrientation()
        endPos = 0 if final else 180
        self.drive(0, endPos-currOr, 'right', 180, True)

    def toWall(self):
        return self.us.value()/10.0
