import sys
import time
import micros_new_OneWire.math_new_micros_OneWire as mathNewOneWire

import micros_chip
import micros_new_OneWire.math_new_micros_OneWire as mathNewOneWire
import micros_new_Analog.math_new_analog as mathAnalog


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


class Commands_Window_OneWire_New_Analog(QtWidgets.QMainWindow):
    global saveOption

    def __init__(self):
        print("Micros Analog")
        super(Commands_Window_OneWire_New_Analog, self).__init__()
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

            temp = int(temp_cod[0]) | (int(temp_cod[1]) << 8)
            # if temp >= 63488:
            #     temp = -1 * (temp - 63488)
            #list_temp.append("микросхема: " + str(iterator_mk) + "; COD: " + str(temp) + "; Temp: " + str(float(temp * 0.0625)))
            list_temp.append("микросхема: " + str(iterator_mk) + "; COD: " + str(temp))

        print(list_temp)


    def readOTP(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            print(iterator_mk)
            for i in range(40):
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
            en = basic_commands_onewire.read_mem_new_micros_OneWire(iterator_mk, 30)
            print(str(en[0]) + " _ " + str(en[0] + 5))
            en1 = en[0] + 5
            # # basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 28, 1)  # ANALOG 7 -
            # # time.sleep(6)
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 30, en1)  # если 204 и 242 в одной посылке, то + 5
            time.sleep(6)
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 27, 255)
            time.sleep(6)
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 39, 128)
            time.sleep(6)


    def writeMem(self):
        list_chip = []
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            print("Chip : " + str(iterator_mk))
            new_chip = micros_chip.Chip(iterator_mk)
            list_chip.append(new_chip)
            mathAnalog.coefficients(iterator_mk, new_chip)
            number_mem_in_chip = 0
            list_k = getattr(new_chip, "k_list")
            list_b = getattr(new_chip, "b_list")
            list_m = getattr(new_chip, "m_list")
            om1 = getattr(new_chip, "om1")
            om2 = getattr(new_chip, "om2")
            z1 = getattr(new_chip, "z")
            z2 = getattr(new_chip, "z2")

            # if len(list_k) != 10:
            #     print("Error, len(list_k) != 10 ")
            #     break
            # if len(list_b) != 10:
            #     print("Error, len(list_b) != 10 ")
            #     break
            # if len(list_m) != 9:
            #     print("Error, len(list_m) != 9 ")
            #     break

            # K
            if list_k[0] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 0, list_k[0])
            time.sleep(6)
            if list_k[1] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 1, list_k[1])
            time.sleep(6)
            if list_k[2] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 2, list_k[2])
            time.sleep(6)
            if list_k[3] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 3, list_k[3])
            time.sleep(6)
            if list_k[4] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 4, list_k[4])
            time.sleep(6)
            if list_k[5] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 5, list_k[5])
            time.sleep(6)
            if list_k[6] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 6, list_k[6])
            time.sleep(6)
            if list_k[7] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 7, list_k[7])
            time.sleep(6)
            # if list_k[8] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 31, list_k[8])
            # time.sleep(6)
            # if list_k[9] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 34, list_k[9])
            # time.sleep(6)
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 31, 255)
            time.sleep(6)
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 34, 255)
            time.sleep(6)

            # # B
            if list_b[0] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 8, list_b[0])
            time.sleep(6)
            if list_b[1] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 9, list_b[1])
            time.sleep(6)
            if list_b[2] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 10, list_b[2])
            time.sleep(6)
            if list_b[3] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 11, list_b[3])
            time.sleep(6)
            if list_b[4] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 12, list_b[4])
            time.sleep(6)
            if list_b[5] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 13, list_b[5])
            time.sleep(6)
            if list_b[6] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 14, list_b[6])
            time.sleep(6)
            if list_b[7] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 15, list_b[7])
            time.sleep(6)
            # if list_b[8] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 32, list_b[8])
            # time.sleep(6)
            # if list_b[9] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 35, list_b[9])
            # time.sleep(6)

            # #M
            if list_m[0] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 17, list_m[0])
            time.sleep(6)
            if list_m[1] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 18, list_m[1])
            time.sleep(6)
            if list_m[2] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 19, list_m[2])
            time.sleep(6)
            if list_m[3] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 20, list_m[3])
            time.sleep(6)
            if list_m[4] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 21, list_m[4])
            time.sleep(6)
            if list_m[5] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 22, list_m[5])
            time.sleep(6)
            if list_m[6] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 23, list_m[6])
            time.sleep(6)
            # if list_m[7] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 33, list_m[7])
            # time.sleep(6)
            # if list_m[8] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 36, list_m[8])
            # time.sleep(6)
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 33, 255)
            time.sleep(6)
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 36, 255)
            time.sleep(6)

            #Z1
            if z1 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 16, z1)
            time.sleep(6)
            #Z2
            # if z2 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 37, z2)
            # time.sleep(6)

            #OM1
            if om1 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 24, om1)
            time.sleep(6)
            #OM2
            if om2 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 25, om2)
            time.sleep(6)


    def startRead(self):
        list_temp = []
        temp_mit = input()
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            basic_commands_onewire.form_temp_cod_not_active(iterator_mk)
        time.sleep(2)
        #servis_method.sleep_slave_1(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk'), 3000)
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            temp_cod = basic_commands_onewire.read_temp_active(iterator_mk)
            list_temp.append(temp_cod[0] | (temp_cod[1] << 8))
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            file_path_data = open('./data/' + str(iterator_mk) + '.txt', 'a')
            file_path_data.write(str(temp_mit) + " " + str(list_temp[iterator_mk - 1]) + "\n")

class Commands_Window_OneWire_New_10(QtWidgets.QMainWindow):
    global saveOption

    def __init__(self):
        print("Micros 10")
        super(Commands_Window_OneWire_New_10, self).__init__()
        uic.loadUi('./ui/commands_OneWire_New.ui', self)
        self.show()
        self.vddButton.clicked.connect(self.workVdd)
        self.readTempButton.clicked.connect(self.readTemp)
        self.readAddressButton.clicked.connect(self.readID)
        self.readOTPButton.clicked.connect(self.readOTP)
        self.writeKAndBButton.clicked.connect(self.writeMem)
        self.writeOTPButton.clicked.connect(self.write3V)
        self.writeEN2Button.clicked.connect(self.writeEN2)
        #self.startButton.clicked.connect(self.startRead)

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
            for i in range(41):
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
            en = basic_commands_onewire.read_mem_new_micros_OneWire(iterator_mk, 30)
            print(str(en[0]) + " _ " + str(en[0] + 1))
            en1 = en[0] + 1
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 30, en1)
            time.sleep(6)

    def write3V(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            en = basic_commands_onewire.read_mem_new_micros_OneWire(iterator_mk, 30)
            print(str(en[0]) + " _ " + str(en[0] + 1))
            en1 = en[0] + 2
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 30, en1)
            time.sleep(6)

    def writeMem(self):
        list_chip = []
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            print("Chip : " + str(iterator_mk))
            new_chip = micros_chip.Chip(iterator_mk)
            list_chip.append(new_chip)
            mathNewOneWire.coefficients(iterator_mk, new_chip)
            number_mem_in_chip = 0
            list_k = getattr(new_chip, "k_list")
            list_b = getattr(new_chip, "b_list")
            list_m = getattr(new_chip, "m_list")
            om1 = getattr(new_chip, "om1")
            om2 = getattr(new_chip, "om2")
            z1 = getattr(new_chip, "z")

            # K
            if list_k[0] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 0, list_k[0])
            time.sleep(6)
            if list_k[1] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 1, list_k[1])
            time.sleep(6)
            if list_k[2] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 2, list_k[2])
            time.sleep(6)
            if list_k[3] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 3, list_k[3])
            time.sleep(6)
            if list_k[4] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 4, list_k[4])
            time.sleep(6)
            if list_k[5] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 5, list_k[5])
            time.sleep(6)
            if list_k[6] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 6, list_k[6])
            time.sleep(6)
            if list_k[7] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 7, list_k[7])
            time.sleep(6)

            # # B
            if list_b[0] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 8, list_b[0])
            time.sleep(6)
            if list_b[1] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 9, list_b[1])
            time.sleep(6)
            if list_b[2] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 10, list_b[2])
            time.sleep(6)
            if list_b[3] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 11, list_b[3])
            time.sleep(6)
            if list_b[4] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 12, list_b[4])
            time.sleep(6)
            if list_b[5] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 13, list_b[5])
            time.sleep(6)
            if list_b[6] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 14, list_b[6])
            time.sleep(6)
            if list_b[7] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 15, list_b[7])
            time.sleep(6)

            # Z1
            if z1 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 16, z1)
            time.sleep(6)


            # #M
            if list_m[0] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 17, list_m[0])
            time.sleep(6)
            if list_m[1] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 18, list_m[1])
            time.sleep(6)
            if list_m[2] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 19, list_m[2])
            time.sleep(6)
            if list_m[3] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 20, list_m[3])
            time.sleep(6)
            if list_m[4] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 21, list_m[4])
            time.sleep(6)
            if list_m[5] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 22, list_m[5])
            time.sleep(6)
            if list_m[6] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 23, list_m[6])
            time.sleep(6)

            # OM1
            if om1 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 24, om1)
            time.sleep(6)
            # OM2
            if om2 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 25, om2)
            time.sleep(6)

            # Del
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 26, 2)

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
        if type_mk == 1:  # 1 - старый OneWire;
            self.comands.clicked.connect(self.show_CommandsWindow_OneWire_Old)
        elif type_mk == 2:  # 2 - старый SPI;
            print()
        elif type_mk == 3:  # 3 - новый OneWire_10; 6 - новый OneWire_ANALOG
            self.comands.clicked.connect(self.show_CommandsWindow_OneWire_New)
        elif type_mk == 4:  # 4 - новый SPI;
            print()
        elif type_mk == 5:  # 5 - новый ???;
            print()
        elif type_mk == 6:
            self.comands.clicked.connect(self.show_CommandsWindow_OneWire_Analog)
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
        self.w1 = Commands_Window_OneWire_New_10()
        self.w1.show()
    # новый Аналог
    def show_CommandsWindow_OneWire_Analog(self):
        self.w1 = Commands_Window_OneWire_New_Analog()
        self.w1.show()


saveOption = save_options.SaveOption()
voltage_state = False
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    # w.show_CommandsWindow()
    sys.exit(app.exec_())
