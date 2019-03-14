#travel 1m
from ev3dev.ev3 import Sound
import robotFunctions

move = robotFunctions.mover('outA', 'outD')

toTravel = 100

speed = 200

move.drive(toTravel, 0, True, speed)

Sound.beep()
