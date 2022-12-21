# from Arduino import Arduino
import serial
import time
from serial.tools import list_ports

# get current device port number
current_device = ""
port = list(list_ports.comports())
for p in port:
    if ("/dev/cu.usb" in p.device):
        print("device: " + p.device)
        current_device = p.device

data_set_status = 0

nodeId = int(input("nodeId: "))
groupId = int(input("groupId: "))
memberNum = int(input("memberNum: "))

key_nodeId = "nodeId-->"
key_groupId = "groupId-->"
key_memberNum = "memberNum-->"
key_toPython = "toPython-->"

# write data to arduino
def write_data(select):
    back_nodeId = 253
    back_groupId = 253
    back_memberNum = 253
    if (select == 1):
        print("nodeId: " + str(nodeId))
        print("python: " + key_nodeId + str(nodeId))
        print("waiting", end="")
        while (back_nodeId != nodeId):
            print(".", end="")
            arduino.write((key_nodeId + str(nodeId)).encode())
            back_nodeId = read_back(nodeId, key_nodeId)
        print("<<< nodeId set! >>>\n")
    elif (select == 2):
        print("groupId: " + str(groupId))
        print("python: " + key_groupId + str(groupId))
        print("waiting", end="")
        while (back_groupId != groupId):
            print(".", end="")
            arduino.write((key_groupId + str(groupId)).encode())
            back_groupId = read_back(groupId, key_groupId)
        print("<<< groupId set! >>>\n")
    elif (select == 3):
        print("memberNum: " + str(memberNum))
        print("python: " + key_memberNum + str(memberNum))
        print("waiting", end="")
        while (back_memberNum != memberNum):
            print(".", end="")
            arduino.write((key_memberNum + str(memberNum)).encode())
            back_memberNum = read_back(memberNum, key_memberNum)
        print("<<< memberNum set! >>>\n")
    elif (nodeId == back_nodeId) and (groupId == back_groupId) and (memberNum == back_memberNum):
        data_set_status = 1

def read_back(origin, key):
    time.sleep(1)
    # print(str(origin) + ": " + str(back))
    data = arduino.readline().decode('utf-8').rstrip()
    if (data):
        if (key_toPython in data):
            data = data.replace(key_toPython, "")
            print("arduino: " + data)
            if (key in data):
                back = data.replace(key, "")
                print(str(origin) + ", " + back)
                return int(back)
                # if (not compare(origin, back)):
                #     write_data()

# def compare(a, b):
#     if (a != b):
#         return 0
#     else:
#         return 1

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

def data_selector():
    select = 0
    while(data_set_status != 1):
        print("1. nodeId\t 2. groupId\t3. memberNum")
        select = input("please select: ")
        if (select == "1"):
            print("writing nodeID...")
        elif (select == 2):
            print("writing groupID...")
        elif (select == 3):
            print("writing memberNum...")
        write_data(int(select))

# arduino.write(bytes(("BasicData-->"), 'utf-8'))
while (1):
    # print("in")
    data = arduino.readline().decode('utf-8').rstrip()
    if ("StartDataWrite-->" in data): 
    # if (1): 
        print("Start Writing Data to Arduino...")
        # read_serial()
        data_selector()
        # write_data()
        print("SUCCESS")
    else: 
        if (data):
            print(data)