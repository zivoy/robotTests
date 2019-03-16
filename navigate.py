import robotFunctions
from ev3dev.ev3 import Sound
from time import sleep

posOfCir = ['right', 'left', 'right', 'left']
stageLength = 10

def flipPlace(val):
    if val == 'right':
        return 'left'
    else:
        return 'right'


robot = robotFunctions.robotHandler('outA', 'outD', 'outB')

robot.ar.position = 0

process = robot.scan()

gCount = 0
for i,j in process:
    if i == 'green':
        i+=1

if gCount == len(process):
    Sound.speak("good to go, all green").wait()

#TODO handle first green
def goRover():
    drove=0
    stages=4
    while stages>0:
        inputType, inputFeed = robot.scanHandler()
        if inputType == 'circle':
            robot.turnAroundSensor()
            toEdge = robot.circleNavigate() #TODO <--- do something with this
            drove =0
            stages-=1
            continue
        else:
            drive_distance=2
            robot.drive(drive_distance, 0, '', 100)
            drove+=drive_distance

        if drove >= stageLength:
            drove=0
            stages-=1
            continue

        '''
        for i in inputFeed:
            if i == 'gray':
                stages-=1
                drove=0
                break
        '''

goRover()
toEnd = robot.toWall()
robot.getIntoPos(toEnd)
sleep(5)
posOfCir = [flipPlace(i) for i in posOfCir]
goRover()
toEnd = robot.toWall()
robot.getIntoPos(toEnd, True)
