import robotFunctions
from ev3dev.ev3 import Sound, Leds
from time import sleep

posOfCir = ['right', 'left', 'right', 'left']
stageLength = 10
green_area = 20

def flip_place(val):
    if val == 'right':
        return 'left'
    else:
        return 'right'


robot = robotFunctions.RobotHandler('outA', 'outD', 'outB')

robot.ar.position = 0

def all_green():
    process = robot.scan(200)
    gCount = 0
    for i, j in process:
        if i == 'green':
            gCount += 1

    if gCount == len(process):
        Leds.set_color(Leds.RIGHT, Leds.GREEN)
        Leds.set_color(Leds.LEFT, Leds.GREEN)
        Sound.speak("good to go, all green").wait()
        Leds.all_off()
        return True
    else:
        return False


def go_rover():
    drove = -green_area
    stage_count = 0
    while stage_count < len(posOfCir):

        input_type, input_feed = robot.scan_handler()

        if input_type == 'circle':
            robot.turn_around_sensor(posOfCir[stage_count])
            to_edge = robot.circle_navigate(posOfCir[stage_count])  # TODO: <--- do something with this
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
            if i == 'grey':
                stages-=1
                drove=0
                break
        '''

all_green()#needdsd handeling?
go_rover()
toEnd = robot.to_wall()
robot.get_into_pos(toEnd)
while not all_green():
    distance_to_walls = []
    for i in range(3):
        robot.drive(0, 90, 'right', 100)
        distance_to_walls.append(robot.to_wall())

sleep(5)
posOfCir = [flip_place(i) for i in posOfCir]
go_rover()
toEnd = robot.to_wall()
robot.get_into_pos(toEnd, True)
