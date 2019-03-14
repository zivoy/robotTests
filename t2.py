#turn 180 in place

toTurn = 180.0

wheel_diameter = 5.6
robot_width = 11.6

from ev3dev import ev3
from ev3dev.ev3 import Sound
from math import pi

m1 = ev3.LargeMotor('outA')
m2 = ev3.LargeMotor('outD')

gy = ev3.GyroSensor()
gy.mode='GYRO-CAL'
gy.mode='GYRO-ANG'

start = gy.value()

speed = 200

turnRight = True #right=True

multiplier = 1.0

wheel_circum = pi * wheel_diameter * multiplier

robot_turn_circle = pi * robot_width

wheel_travel_distance = robot_turn_circle * toTurn / 360.0

rotation_deg = wheel_travel_distance / wheel_circum * 360

direction = 1.0 if turnRight else -1.0

m1.run_to_rel_pos(position_sp = rotation_deg * direction, speed_sp=speed)
m2.run_to_rel_pos(position_sp = - rotation_deg * direction, speed_sp=speed)

m1.wait_while('running')
m2.wait_while('running')

end = gy.value()

turnCon = end - start
units = gy.units

conclusion = 'expected to turn {} degrees and turned {} {}'.format(toTurn, turnCon, units)
print(conclusion)
Sound.speak(conclusion).wait()

