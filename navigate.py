import robotFunctions
from ev3dev.ev3 import Sound

robot = robotFunctions.robotHandler('outA', 'outD', 'outB')

robot.ar.position = 0

process = robot.scan()

gCount = 0
for i,j in process:
    if i == 'green':
        i+=1

if gCount == len(process):
    Sound.speak("good to go, all green").wait()

while True:
    inputType, inputFeed = robot.scanHandler()
    if inputType == 'circle':
        robot.turnAroundSensor()
        robot.circleNavigate()
    else:
        robot.drive(2, 0, '', 100)
