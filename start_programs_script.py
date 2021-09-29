import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication
import save_options

import main


class ConfigurationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ConfigurationWindow, self).__init__()
        uic.loadUi('./ui/config.ui', self)
        self.show()


class CommandsWindow(QtWidgets.QMainWindow):
    global saveOption

    def __init__(self):
        super(CommandsWindow, self).__init__()
        uic.loadUi('./ui/commands.ui', self)
        self.show()
        self.VddButton.clicked.connect(self.workVdd)
        self.ReadTempButton.clicked.connect(self.readTemp)
        self.ReadOTPButton.clicked.connect(self.readOTP)
        self.WriteREZButton.clicked.connect(self.writeREZ)
        self.WriterIDButton.clicked.connect(self.writeID)
        self.WriteOTPButton.clicked.connect(self.writeOTP)
        self.ReadIDButton.clicked.connect(self.readID)
        self.WriteEn2Button.clicked.connect(self.writeEN2)

    def workVdd(self):
        flag = main.all_vdd(getattr(saveOption, 'voltage_state'), getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk'))
        setattr(saveOption, 'voltage_state', flag)
        print(getattr(saveOption, 'voltage_state'))
        main.start_stack_execution()

    def readTemp(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk')+1):
            main.form_temp_cod_not_activ(iterator_mk)
        main.sleep_slave_1(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk'), 3000)
        #main.start_stack_execution()
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk')+1):
            main.read_temp_activ(iterator_mk)

    def readOTP(self):

        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk')+1):
            iterator_step = 0
            flag = main.all_vdd(getattr(saveOption, 'voltage_state'), getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk'))
            setattr(saveOption, 'voltage_state', flag)
            while iterator_step < 256:
                main.read_otp_address(iterator_mk, iterator_step)
                iterator_step += 1
            print("new mk")
            flag = main.all_vdd(getattr(saveOption, 'voltage_state'), getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk'))
            setattr(saveOption, 'voltage_state', flag)


    def writeREZ(self):
        print("not work")

    def writeID(self):
        print("not work")

    def writeOTP(self):
        print("not work")

    def readID(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk')+1):
            main.read_address(iterator_mk)

    def writeEN2(self):
        print("not work")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('./ui/main.ui', self)
        self.setWindowTitle('MainWindow')
        self.comands.clicked.connect(self.show_CommandsWindow)
        # self.options.clicked.connect(self.show_ConfigurationWindow)

    # def show_ConfigurationWindow(self):
    #     self.w1 = ConfigurationWindow()
    #     self.w1.show()

    def show_CommandsWindow(self):
        self.w1 = CommandsWindow()
        self.w1.show()


saveOption = save_options.SaveOption()
voltage_state = False
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    # w.show_CommandsWindow()
    sys.exit(app.exec_())
