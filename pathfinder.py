import robotFunctions
from robotFunctions import Color
from robotFunctions import Direction as Dir
from time import sleep

robot = robotFunctions.RobotHandler('outA', 'outD', 'outB')

start_length = 20

robot.drive(start_length)
robot.ar.run_to_abs_pos(posi)

max_drive = 150
drove = 0
drive_dist = 2

while True:
    if robotFunctions.get_closest_color(robot.return_colors()) == Color.BLUE:
        break
    else:
        robot.drive(drive_dist, speed=400)
        drove += drive_dist
    if drove > max_drive:
        break

typeIn, feed = robot.scan_handler()
def driveFor():
    while typeIn == 'clear':
        robot.drive(drive_dist, speed=250)
        typeIn, feed = robot.scan_handler()

while typeIn!= 'green'
    driveFor()
    typeIn, feed = robot.scan_handler()
    if typeIn == 'circle':
        pos_of_err = feed[0][0]
        scan_ran = range((pos_of_err-1)*10, (pos_of_err+1)*10, 5)
        blues = []
        for i in scan_ran:
            robot.ar.run_to_abs_pos(position_sp=i, speed_sp=150)
            sleep(.01)
            blues.append(robotFunctions.get_closest_color(robot.return_colors()))
        robot.circle_navigate(Dir.RIGHT)

