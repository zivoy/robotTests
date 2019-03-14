#drive continuesly on white page

from ev3dev import ev3
from ev3dev.ev3 import Sound
from math import pi
import robotFunctions.get_closest_color as getClosestColor

m1 = ev3.LargeMotor('outA')
m2 = ev3.LargeMotor('outD')
ar = ev3.MediumMotor('outB')

cl = ev3.ColorSensor()

cl.mode='RGB-RAW'

speed = 200

ar.run_to_abs_pos(position_sp = 0)

multiplier = 1
goTO = 1

circum = pi * 5.6 * multiplier
rotation = goTO / circum * 360

while getClosestColor(cl.value()) == 'white':
    m1.run_to_rel_pos(position_sp=rotation, speed_sp=speed)
    m2.run_to_rel_pos(position_sp=rotation, speed_sp=speed)

Sound.beep()
