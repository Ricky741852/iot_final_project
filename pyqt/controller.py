from PyQt5 import QtWidgets, QtGui, QtCore

from UI import Ui_MainWindow

from PyQt5.QtWidgets import QMessageBox

from main import main

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.main = main()
        self.ui.setupUi(self)
        self.setup_control()
        #讀取Port
        ports = main.scan_port()
        for p in ports:
            print(str(p))
            self.ui.cbPort.addItem(str(p), str(p.device))

    def setup_control(self):
        # TODO
        self.ui.btnWrite.clicked.connect(self.write)

    def write(self):
        node_id = self.ui.txtNodeId.toPlainText()
        group_id = self.ui.txtGroupId.toPlainText()
        member_num = self.ui.txtMemberNum.toPlainText()
        print(node_id, group_id, member_num)
        if node_id=="" or group_id=="" or member_num=="":
            QMessageBox.warning(None, '警告', '數值不得為空')
            return
        try:
            self.main.nodeId=int(node_id)
            self.main.groupId=int(group_id)
            self.main.memberNum=int(member_num)
            self.main.current_device=self.ui.cbPort.currentData()
            self.main.setup_serial()
            self.main.data_selector()
            b_node_id = self.main.back_nodeId
            b_group_id = self.main.back_groupId
            b_member_num = self.main.back_memberNum
            successMessage = (f"Node Id: {b_node_id}\nGroup Id: {b_group_id}\nMember Num: {b_member_num}")
            QMessageBox.information(None, 'Success', successMessage)
        except Exception as msg:
            print(msg)
            QMessageBox.critical(None, '錯誤', '寫入失敗')