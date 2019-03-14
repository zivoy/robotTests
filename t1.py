#travel 1m

from ev3dev import ev3
from ev3dev.ev3 import Sound
from math import pi

m1 = ev3.LargeMotor('outA')
m2 = ev3.LargeMotor('outD')

speed = 200

multiplier = 1

circum = pi * 5.6 * multiplier

toTravel = 100

rotation = toTravel / circum * 360

m1.run_to_rel_pos(position_sp=rotation, speed_sp=speed)
m2.run_to_rel_pos(position_sp=rotation, speed_sp=speed)

m1.wait_while('running')
m2.wait_while('running')

Sound.beep()
