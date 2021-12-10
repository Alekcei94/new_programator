import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication

import save_options
import servis_method

import basic_commands_onewire


class ConfigurationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ConfigurationWindow, self).__init__()
        uic.loadUi('./ui/Setting.ui', self)
        self.show()


class Commands_Window_OneWire_New(QtWidgets.QMainWindow):
    global saveOption

    def __init__(self):
        super(Commands_Window_OneWire_New, self).__init__()
        uic.loadUi('./ui/commands_OneWire_New.ui', self)
        self.show()
        self.vddButton.clicked.connect(self.workVdd)
        self.readTempButton.clicked.connect(self.readTemp)
        self.readAddressButton.clicked.connect(self.readID)
        self.readOTPButton.clicked.connect(self.readOTP)
        self.writeKAndBButton.clicked.connect(self.writeEN2)
        self.writeOTPButton.clicked.connect(self.writeEN2)
        self.writeEN2Button.clicked.connect(self.writeEN2)

    def workVdd(self):
        servis_method.all_vdd(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk'), saveOption)

    def readTemp(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            basic_commands_onewire.form_temp_cod_not_active(iterator_mk)
        servis_method.sleep_slave_1(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk'), 3000)
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            basic_commands_onewire.read_temp_active(iterator_mk)

    def readOTP(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            print("not work")
            print(iterator_mk)

    def readID(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            basic_commands_onewire.read_address(iterator_mk)

    def writeEN2(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            print("not work")


class Commands_Window_OneWire_Old(QtWidgets.QMainWindow):
    global saveOption

    def __init__(self):
        super(Commands_Window_OneWire_Old, self).__init__()
        uic.loadUi('./ui/commandsOneWireOld.ui', self)
        self.show()
        self.vddButton.clicked.connect(self.workVdd)
        self.readTempButton.clicked.connect(self.readTemp)
        self.readAddressButton.clicked.connect(self.readID)
        self.readOTPButton.clicked.connect(self.readOTP)
        self.writeREZButton.clicked.connect(self.writeREZ)
        self.writeAddressButton.clicked.connect(self.writeID)
        self.writeKAndBButton.clicked.connect(self.writeID)
        self.writeOTPButton.clicked.connect(self.writeOTP)
        self.writeEN2Button.clicked.connect(self.writeEN2)

    def workVdd(self):
        servis_method.all_vdd(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk'), saveOption)
        servis_method.start_stack_execution()

    def readTemp(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            basic_commands_onewire.form_temp_cod_not_active(iterator_mk)
        servis_method.sleep_slave_1(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk'), 3000)
        # main.start_stack_execution()
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            basic_commands_onewire.read_temp_active(iterator_mk)

    def readOTP(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            iterator_step = 0
            servis_method.all_vdd(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk'), saveOption)
            while iterator_step < 256:
                basic_commands_onewire.read_otp_address(iterator_mk, iterator_step)
                iterator_step += 1
            print("new mk")

            servis_method.all_vdd(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk'), saveOption)

    def writeREZ(self):
        # Рализовать чтение всех данных с мк и передача его в метод массивом
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            basic_commands_onewire.write_REZ(iterator_mk)

    def writeID(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            basic_commands_onewire.write_ID(iterator_mk)

    def writeOTP(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            print("not work")

    def readID(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            basic_commands_onewire.read_address(iterator_mk)

    def writeEN2(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            print("not work")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('./ui/Main.ui', self)
        self.setWindowTitle('MainWindow')
        type_mk = getattr(saveOption, "type_mk")
        if type_mk == 1:  # 1 - старый OneWire; ;
            self.comands.clicked.connect(self.show_CommandsWindow_OneWire_Old)
        elif type_mk == 2:  # 2 - старый SPI;
            print()
        elif type_mk == 3 or type_mk == 6:  # 3 - новый OneWire_10; 6 - новый OneWire_ANALOG
            self.comands.clicked.connect(self.show_CommandsWindow_OneWire_New)
        elif type_mk == 4:  # 4 - новый SPI;
            print()
        elif type_mk == 5:  # 5 - новый ???;
            print()
        else:
            print("ERROR type_mk")
            pass

        self.options.clicked.connect(self.show_ConfigurationWindow)

    def show_ConfigurationWindow(self):
        self.w1 = ConfigurationWindow()
        self.w1.show()

    # Старый OneWire
    def show_CommandsWindow_OneWire_Old(self):
        self.w1 = Commands_Window_OneWire_Old()
        self.w1.show()

    # Новый OneWire
    def show_CommandsWindow_OneWire_New(self):
        self.w1 = Commands_Window_OneWire_New()
        self.w1.show()


saveOption = save_options.SaveOption()
voltage_state = False
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    # w.show_CommandsWindow()
    sys.exit(app.exec_())
