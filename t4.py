#drive continuesly on white page

from ev3dev import ev3
from ev3dev.ev3 import Sound
import robotFunctions

move = robotFunctions.mover('outA', 'outD')
#ar = ev3.MediumMotor('outB')

cl = ev3.ColorSensor()

cl.mode='RGB-RAW'

speed = 200

#ar.run_to_abs_pos(position_sp=0)

while robotFunctions.get_closest_color(cl.value()) == 'white':
    move.drive(1, 0, True, speed)

Sound.beep()
