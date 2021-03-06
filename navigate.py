import robotFunctions
from robotFunctions import Color
from robotFunctions import Direction as Dir
from ev3dev.ev3 import Sound, Leds
from time import sleep

posOfCir = [Dir.RIGHT, Dir.LEFT, Dir.RIGHT, Dir.LEFT]
stageLength = [51, 67, 67, 57]

robot_to_front = 4
green_area = toCn(16)

robot = robotFunctions.RobotHandler('outA', 'outD', 'outB')

robot.ar.position = 0

def toCn(val):
    return val*2.5


def all_green():
    process = robot.scan(200)
    g_count = 0
    for i, j in process:
        if i == Color.GREEN:
            g_count += 1

    if g_count == len(process):
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
        print(input_type, input_feed)
        if input_type == 'circle':
            to_edge = robot.circle_navigate(posOfCir[stage_count])  # TODO: <--- do something with this
            drove = 0
            stage_count += 1
            continue
        else:
            drive_distance = 2
            robot.drive(drive_distance, 0, '', 100)
            drove += drive_distance

        if drove >= stageLength[stage_count]:
            drove = 0
            stage_count += 1
            continue

        '''
        for i in inputFeed:
            if i == Color.GREY:
                stages-=1
                drove=0
                break
        '''


def park():
    robot.drive(0, 180, Dir.RIGHT, 150)
    front_wall = robot.to_wall() - robot_to_front
    keep_gap = 5
    robot.drive(-front_wall + keep_gap, speed=150)
    robot.drive(0, 90, Dir.RIGHT, 150)
    left_wall = robot.to_wall() - robot_to_front
    robot.drive(0, 180, Dir.LEFT, 150)
    right_wall = robot.to_wall() - robot_to_front
    left_w = True

    if right_wall < left_wall:
        robot.drive(0, 180, Dir.RIGHT, 150)
        left_w = False
    _, input_feed = robot.scan_handler()

    while ((-8, Color.GREEN) not in input_feed) and ((8, Color.GREEN) not in input_feed):
        robot.drive(-2, speed=40)
        _, input_feed = robot.scan_handler()

    robot.stop_running()
    turn_dir = Dir.LEFT if left_w else Dir.RIGHT
    orientation = robot.get_orientation()
    robot.drive(0, 180 - orientation, turn_dir, 50)
    all_green()


all_green()
go_rover()
park()
robot.gy.mode = 'GYRO-CAL'
robot.gy.mode = 'GYRO-ANG'
sleep(5)
posOfCir = [~i for i in posOfCir]
go_rover()
park()
