# from Arduino import Arduino
import serial
import time
from serial.tools import list_ports

# get current device port number
current_device = ""
port = list(list_ports.comports())
for p in port:
    if ("/dev/cu.usb" in p.device):
        print(p.device)
        current_device = p.device

nodeId = input("nodeId: ")
groupId = input("groupId: ")
memberNum = input("memberNum: ")

back_nodeId = -1
back_groupId = -1
back_memberNum = -1

key_nodeId = "nodeId-->"
key_groupId = "groupId-->"
key_memberNum = "memberNum-->"
key_toPython = "toPython-->"
# write data to arduino
def write_data():
    arduino.write(bytes((key_nodeId + nodeId), 'utf-8'))
    read_back()
    arduino.write(bytes((key_groupId + groupId), 'utf-8'))
    read_back()
    arduino.write(bytes((key_memberNum + memberNum), 'utf-8'))
    read_back()

def read_back():
    time.sleep(1)
    data = arduino.readline().decode('utf-8').rstrip()
    if (data):
        if (key_toPython in data):
            data = data.replace(key_toPython, "")
            print(data)
            if (key_nodeId in data):
                back_nodeId = data.replace(key_nodeId, "")
                if (not compare(nodeId, back_nodeId)):
                    write_data()
            elif (key_groupId in data):
                back_groupId = data.replace(key_groupId, "")
                if (not compare(groupId, back_groupId)):
                    write_data()
            elif (key_memberNum in data):
                back_memberNum = data.replace(key_memberNum, "")
                if (not compare(memberNum, back_memberNum)):
                    write_data()

def compare(a, b):
    if (a != b):
        return 0
    else:
        return 1

# print(arduino)
def read_serial():
    while(1):
        write_data()
        data = arduino.readline().decode('utf-8').rstrip()
        if (data):
            print(data)
            # if (key_toPython in data):
            #     print(data.replace(key_toPython, ""))

# init board
arduino = serial.Serial(current_device, 115200, timeout=0.1)

read_serial()