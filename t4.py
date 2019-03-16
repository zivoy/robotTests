#drive continuesly on white page

from ev3dev import ev3
from ev3dev.ev3 import Sound
import robotFunctions
import robotFunctions.Color


move = robotFunctions.mover('outA', 'outD')
#ar = ev3.MediumMotor('outB')

cl = ev3.ColorSensor()

cl.mode='RGB-RAW'

speed = 200

#ar.run_to_abs_pos(position_sp=0)

while robotFunctions.get_closest_color([cl.value(i) for i in range(3)]) == Color.WHITE:
    move.drive(9.5, 0, '', speed)

Sound.beep()
