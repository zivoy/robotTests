#turn 90 while driving
from ev3dev import ev3
from ev3dev.ev3 import Sound
import robotFunctions

toTurn = 90
toTravel = 20

move = robotFunctions.mover('outA', 'outD')

gy = ev3.GyroSensor()
gy.mode='GYRO-CAL'
gy.mode='GYRO-ANG'

start = gy.value()

speed = 200

turnTo = 'right'

move.drive(toTravel, toTurn, turnTo, speed)

end = gy.value()

turnCon = end - start
units = gy.units

conclusion = 'expected to turn {} degrees and turned {} {}'.format(toTurn, turnCon, units)
print(conclusion)
Sound.speak(conclusion).wait()

