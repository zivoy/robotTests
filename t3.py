#turn 90 while driving

toTurn = 90

toTravel = 20

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

turnTo = True #right=True

multiplier = 1

circum = pi * 5.6 * multiplier

rCircum = 15

forGo = toTravel / circum * 360

toGo = rCircum * toTurn / 360
rotation = toGo / circum * 360

if turnTo:
    sRot = -rotation
else:
    sRot = rotation
    rotation *= -1

sRot += forGo
rotation += forGo

m1.run_to_rel_pos(position_sp=rotation, speed_sp=speed)
m2.run_to_rel_pos(position_sp=sRot, speed_sp=speed)

m1.wait_while('running')
m2.wait_while('running')

end = gy.value()

turnCon = end - start
units = gy.units

conclusion = 'expected to turn {} degrees and turned {} {}'.format(toTurn, turnCon, units)
print(conclusion)
Sound.speak(conclusion).wait()

