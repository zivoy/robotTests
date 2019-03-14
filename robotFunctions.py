import numpy as np
from ev3dev import ev3
from ev3dev.ev3 import Sound

def get_closest_color(color_measure):
    colorm = color_measure[:3]
    colors = {'red': np.array([255, 0, 0]),
              'green': np.array([0, 255, 0]),
              'blue': np.array([0, 0, 255]),
              'grey': np.array([230, 230, 230]),
              'black': np.array([0, 0, 0]),
              'white': np.array([255, 255, 255])}
    distances  =  [ (np.linalg.norm(color - colorm), name) for name, color in colors.items()]
  #  print (distances)
    return min(distances)[1]
'''
def move(motor1, motor2):
    def f
    return def (forward, turnDeg, turnDir, speed):

        pass


class mover:
    def __init__(self, m1, m2):
        self.m1 = m1
        self.m2 = m2
    def move(self, dist):
        self.m1.move(dist)


mcontrol = mover(motor1, motor2)


'''
