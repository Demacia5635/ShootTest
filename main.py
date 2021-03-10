
import threading
from networktables import NetworkTables

cond = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

NetworkTables.initialize(server='10.56.35.2')
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()

print("Connected!")

table = NetworkTables.getTable('SmartDashboard')

global mList
global addComma
addComma = False
mList = "{\n\t\"Positions\" : [\n"

def saveToList():
    mList += formatData(table.getNumber("Distance", -1), table.getNumber("Velocity", 1), table.getNumber("Angle", 1))

def formatData(distance, velocity, angle):
    distance1 = int(distance)
    if distance1 % 50 > 25:
        dis = distance1 + 50 - (distance1 % 50)
    else:
        dis = distance1 - distance1 % 50
    return "\t\t{\n\t\t\t\"Distance\" : \"" + dis + "\",\n\t\t\t\"Velocity\" : \"" + velocity +\
           "\",\n\t\t\t\"Angle\" : \"" + angle + "\"\n\t\t}"

while True:
    i = input("Press Enter to save, Enter 0 to shoot, 1 to stop")
    if i == "0":
        table.putBoolean("Shoot", True)
    elif i == "1":
        break
    else:
        if addComma:
            mList += ",\n"
        else:
            addComma = True
        saveToList()
        table.putBoolean("NextPos", True)
mList += "\n\t]\n}"
file = open("Positions.json", "w")
file.write(mList)
file.close()
