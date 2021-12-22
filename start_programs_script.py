import sys
import time
import micros_new_OneWire.math_new_micros_OneWire as mathNewOneWire

import micros_chip
import micros_new_OneWire.math_new_micros_OneWire as mathNewOneWire


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
        self.writeKAndBButton.clicked.connect(self.writeMem)
        self.writeOTPButton.clicked.connect(self.writeEN2)
        self.writeEN2Button.clicked.connect(self.writeEN2)
        self.startButton.clicked.connect(self.startRead)

    def workVdd(self):
        print("Start VDD")
        servis_method.all_vdd(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk'), saveOption)
        print("FINISH VDD")

    def readTemp(self):
        list_temp = []
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            basic_commands_onewire.form_temp_cod_not_active(iterator_mk)
        time.sleep(2)
        #servis_method.sleep_slave_1(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk'), 3000)
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            temp_cod = basic_commands_onewire.read_temp_active(iterator_mk)
            if temp_cod[8] == servis_method.test_crc(temp_cod[0], temp_cod[1], temp_cod[2], temp_cod[3], temp_cod[4],
                                                     temp_cod[5], temp_cod[6], temp_cod[7]):
            #if 1 == 1:
                temp = int(temp_cod[0]) | (int(temp_cod[1]) << 8)
                if temp >= 63488:
                    temp = -1 * (temp - 63488)
                list_temp.append("микросхема: " + str(iterator_mk) + "; COD: " + str(temp) + "; Temp: " + str(float(temp * 0.0625)))
            else:
                list_temp.append("ER")

        print(list_temp)


    def readOTP(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            print(iterator_mk)
            for i in range(31):
                print(str(i) + " : " + str(basic_commands_onewire.read_mem_new_micros_OneWire(iterator_mk, i)))


    def readID(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):

            # basic_commands_onewire.read_address(iterator_mk)
            # time.sleep(1)
            print(iterator_mk)
            address = ""
            for i in range(31, 39):
                address = address + str(basic_commands_onewire.read_mem_new_micros_OneWire(iterator_mk, i)) + " "
            print(address)

    def writeEN2(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            for i in range(40):
                print(i)
                basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 30, 179)
                time.sleep(1)
            print("30")

    def writeMem(self):
        list_chip = []
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            new_chip = micros_chip.Chip(iterator_mk)
            list_chip.append(new_chip)
            mathNewOneWire.coefficients(iterator_mk, new_chip)
            number_mem_in_chip = 0
            for data in getattr(new_chip, "k_list"):
                print(str(data) + " __ " + str(number_mem_in_chip))
                if data != 0:
                    basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, number_mem_in_chip, data)
                number_mem_in_chip += 1

            for data in getattr(new_chip, "b_list"):
                print(str(data) + " __ " + str(number_mem_in_chip))
                if data != 0:
                    basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, number_mem_in_chip, data)
                number_mem_in_chip += 1

            z = getattr(new_chip, "z")
            print(str(z) + " __ " + str(number_mem_in_chip))
            if z != 0:
                basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, number_mem_in_chip, z)
            number_mem_in_chip += 1

            for data in getattr(new_chip, "m_list"):
                print(str(data) + " __ " + str(number_mem_in_chip))
                if data != 0:
                    basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, number_mem_in_chip, data)
                number_mem_in_chip += 1

            om1 = getattr(new_chip, "om1")
            print(str(om1) + " __ " + str(number_mem_in_chip))
            if om1 != 0:
                basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, number_mem_in_chip, om1)
            number_mem_in_chip += 1

            om2 = getattr(new_chip, "om2")
            print(str(om2) + " __ " + str(number_mem_in_chip))
            if om2 != 0:
                basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, number_mem_in_chip, om2)

            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 26, 2)  # делитель
            print("2 __ 26")

    def startRead(self):
        list_temp = []
        temp_mit = input()
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            basic_commands_onewire.form_temp_cod_not_active(iterator_mk)
        time.sleep(2)
        #servis_method.sleep_slave_1(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk'), 3000)
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            temp_cod = basic_commands_onewire.read_temp_active(iterator_mk)
            #if temp_cod[8] == servis_method.test_crc(temp_cod[0], temp_cod[1], temp_cod[2], temp_cod[3], temp_cod[4], temp_cod[5], temp_cod[6], temp_cod[7]):
            if 1 == 1:
                list_temp.append(temp_cod[0] | (temp_cod[1] << 8))
            else:
                list_temp.append("ER")
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            file_path_data = open('./data/' + str(iterator_mk) + '.txt', 'a')
            file_path_data.write(str(temp_mit) + " " + str(list_temp[iterator_mk - 1]))

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
