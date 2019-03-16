import robotFunctions
from ev3dev.ev3 import Sound
from time import sleep

posOfCir = ['right', 'left', 'right', 'left']
stageLength = 10


def flip_place(val):
    if val == 'right':
        return 'left'
    else:
        return 'right'


robot = robotFunctions.RobotHandler('outA', 'outD', 'outB')

robot.ar.position = 0

process = robot.scan()

gCount = 0
for i, j in process:
    if i == 'green':
        i += 1

if gCount == len(process):
    Sound.speak("good to go, all green").wait()


# TODO handle first green
def go_rover():
    drove = 0
    stage_count = 0
    while stage_count < len(posOfCir):

        input_type, input_feed = robot.scan_handler()

        if input_type == 'circle':
            robot.turn_around_sensor()
            to_edge = robot.circle_navigate(posOfCir[stage_count])  # TODO <--- do something with this
            drove = 0
            stage_count += 1
            continue
        else:
            drive_distance = 2
            robot.drive(drive_distance, 0, '', 100)
            drove += drive_distance

        if drove >= stageLength:
            drove = 0
            stage_count += 1
            continue

        '''
        for i in inputFeed:
            if i == 'gray':
                stages-=1
                drove=0
                break
        '''


go_rover()
toEnd = robot.to_wall()
robot.get_into_pos(toEnd)
sleep(5)
posOfCir = [flip_place(i) for i in posOfCir]
go_rover()
toEnd = robot.to_wall()
robot.get_into_pos(toEnd, True)
