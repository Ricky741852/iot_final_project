# from Arduino import Arduino
import serial
import time
from serial.tools import list_ports

class main():
    # get current device port number
    current_device = ""
    arduino = serial.Serial()

    # select = 0
    data_set_status = 0

    nodeId = -1#int(input("nodeId: "))
    groupId = -1#int(input("groupId: "))
    memberNum = -1#int(input("memberNum: "))

    back_nodeId = 253
    back_groupId = 253
    back_memberNum = 253

    key_nodeId = "nodeId-->"
    key_groupId = "groupId-->"
    key_memberNum = "memberNum-->"
    key_toPython = "toPython-->"

    def setup_serial(self):
        # init board
        self.arduino = serial.Serial(self.current_device, 115200, timeout=0.1)

    def scan_port():
        ports = list(list_ports.comports())
        return ports

    def clear_buf(self):
        for i in range(5):
            data = self.arduino.readline().decode('utf-8').rstrip()

    # write data to arduino
    def write_data(self, select):
        self.clear_buf()
        if (select == 1):
            print("nodeId: " + str(self.nodeId))
            # print("python: " + key_nodeId + str(nodeId))
            # print("waiting", end="")
            while (self.back_nodeId != self.nodeId):
                # print(".", end="")
                self.arduino.write((self.key_nodeId + str(self.nodeId) + '\n').encode())                
                self.back_nodeId = self.read_back(self.key_nodeId)
            print("<<< nodeId set! >>>")
        elif (select == 2):
            print("groupId: " + str(self.groupId))
            # print("python: " + key_groupId + str(groupId))
            # print("waiting", end="")
            while (self.back_groupId != self.groupId):
                # print(".", end="")
                self.arduino.write((self.key_groupId + str(self.groupId) + '\n').encode())
                self.back_groupId = self.read_back(self.key_groupId)
            print("<<< groupId set! >>>")
        elif (select == 3):
            print("memberNum: " + str(self.memberNum))
            # print("python: " + key_memberNum + str(memberNum))
            # print("waiting", end="")
            while (self.back_memberNum != self.memberNum):
                # print(".", end="")
                self.arduino.write((self.key_memberNum + str(self.memberNum) + '\n').encode())
                self.back_memberNum = self.read_back(self.key_memberNum)
            print("<<< memberNum set! >>>")

    def read_back(self, key):
        b_value = 0
        time.sleep(2)
        # print(str(origin) + ": " + str(back))
        data = self.arduino.readline().decode('utf-8').rstrip()
        if (data):
            # print(data)
            if (self.key_toPython in data):
                data = data.replace(self.key_toPython, "")
                # print("arduino: " + data)
                if (key in data):
                    back = data.replace(key, "")
                    # print(str(origin) + ", " + back)
                    b_value = int(back)
                    # print(back)
        return b_value


    def data_selector(self):
        # print("1. nodeId\t 2. groupId\t3. memberNum\t4. end")
        # select = input("please select: ")
        for i in range(1, 5):
            # if (str(i) == "1"):
            #     print("writing nodeId...")
            # elif (str(i) == "2"):
            #     print("writing groupId...")
            # elif (str(i) == "3"):
            #     print("writing memberNum...")
            # elif (str(i) == "4"):
            #     print("exit")
                # break
            self.write_data(i)

    # arduino.write(bytes(("BasicData-->"), 'utf-8'))
    # while (1):
    #     # print("in")
    #     data = arduino.readline().decode('utf-8').rstrip()
    #     if ("StartDataWrite-->" in data): 
    #     # if (1): 
    #         print("Start Writing Data to Arduino...")
    #         # read_serial()
    #         data_selector()
    #         # write_data()
    #         print("SUCCESS")
    #     else: 
    #         if (data):
    #             print(data)