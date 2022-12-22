from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QMovie

from PyQt5.QtCore import QThread, pyqtSignal

from UI import Ui_MainWindow
from main import main

class WorkerThread(QThread):
    success_trigger = pyqtSignal(bool)
    msg_trigger = pyqtSignal(str)
    finished = pyqtSignal()
    port = ""
    node_id = ""
    group_id = ""
    member_num = ""
    def __init__(self, port, node_id, group_id, member_num):
        super().__init__()
        self.main = main()
        self.port = port
        self.node_id = node_id
        self.group_id = group_id
        self.member_num = member_num

    def run(self):
        try:
            self.main.nodeId=int(self.node_id)
            self.main.groupId=int(self.group_id)
            self.main.memberNum=int(self.member_num)
            self.main.current_device=self.port
            self.main.setup_serial()
            self.main.data_selector()
            b_node_id = self.main.back_nodeId
            b_group_id = self.main.back_groupId
            b_member_num = self.main.back_memberNum
            successMessage = (f"Node Id: {b_node_id}\nGroup Id: {b_group_id}\nMember Num: {b_member_num}")
            self.success_trigger.emit(True)
            self.msg_trigger.emit(successMessage)
        except Exception as msg:
            self.success_trigger.emit(False)
            self.msg_trigger.emit(str(msg))
        finally:
            self.finished.emit()

class MainWindow_controller(QtWidgets.QMainWindow, QThread):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.main = main()
        self.ui.setupUi(self)
        self.setup_control()
        #讀取Port
        ports = main.scan_port()
        for p in ports:
            # print(str(p))
            self.ui.cbPort.addItem(str(p), str(p.device))
        self.movie = QMovie("loading.gif")
        self.ui.loading.setMovie(self.movie)
        self.movie.start()
        self.ui.loading.hide()

    def startThread(self):
        port = self.ui.cbPort.currentData()
        node_id = self.ui.txtNodeId.toPlainText()
        group_id = self.ui.txtGroupId.toPlainText()
        member_num = self.ui.txtMemberNum.toPlainText()
        self.work = WorkerThread(port, node_id, group_id, member_num)
        self.ui.loading.show()
        self.work.start()
        self.work.success_trigger.connect(self.success_trigger)
        self.work.msg_trigger.connect(self.msg_trigger)
        self.work.finished.connect(self.threadFinished)

    def success_trigger(self, success):
        self.success = success

    def msg_trigger(self, msg):
        self.msg = msg

    def threadFinished(self):
        self.ui.loading.hide()
        if self.success:
            QMessageBox.information(None, 'Success', self.msg)
        else:
            QMessageBox.critical(None, '錯誤', self.msg)

    def setup_control(self):
        # TODO
        self.ui.btnWrite.clicked.connect(
            self.startThread)

    #未另外指派執行緒的寫法
    def write(self):
        port = self.ui.cbPort.currentData()
        node_id = self.ui.txtNodeId.toPlainText()
        group_id = self.ui.txtGroupId.toPlainText()
        member_num = self.ui.txtMemberNum.toPlainText()
        try:
            # print(node_id, group_id, member_num)
            if node_id=="" or group_id=="" or member_num=="":
                QMessageBox.warning(None, '警告', '數值不得為空')
                return
            self.main.current_device=port
            self.main.nodeId=int(node_id)
            self.main.groupId=int(group_id)
            self.main.memberNum=int(member_num)
            self.main.setup_serial()
            self.main.data_selector()
            b_node_id = self.main.back_nodeId
            b_group_id = self.main.back_groupId
            b_member_num = self.main.back_memberNum
            successMessage = (f"Node Id: {b_node_id}\nGroup Id: {b_group_id}\nMember Num: {b_member_num}")
            QMessageBox.information(None, 'Success', successMessage)
        except Exception as msg:
            print(msg)
            QMessageBox.critical(None, '錯誤', str(msg))
        finally:
            self.ui.loading.setVisible(False)
            self.movie.stop()