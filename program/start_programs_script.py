import sys
import time
import micros_new_OneWire.math_new_micros_OneWire as mathNewOneWire

import micros_chip
import micros_new_OneWire.math_new_micros_OneWire as mathNewOneWire
import micros_new_Analog.math_new_analog as mathAnalog
import logger
import other.other_functions as other_functions

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication

import save_options
import servis_method

import basic_commands_onewire
import test_ckc_analog
import test_clc

import mathem.TMD as TMD
import mathem.utility as utility


class ConfigurationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ConfigurationWindow, self).__init__()
        uic.loadUi('./ui/Setting.ui', self)
        self.show()


class Commands_Window_OneWire_New_Analog(QtWidgets.QMainWindow):
    global saveOption

    def __init__(self):
        print("Микрос 13")
        super(Commands_Window_OneWire_New_Analog, self).__init__()
        uic.loadUi('./ui/commands_OneWire_New.ui', self)
        self.show()
        self.vddButton.clicked.connect(self.workVdd)
        self.readTempButton.clicked.connect(self.readTemp)
        self.readAddressButton.clicked.connect(self.readID)
        self.readOTPButton.clicked.connect(self.readOTP)
        self.writeKAndBButton.clicked.connect(self.writeMem)
        self.writeOTPButton.clicked.connect(self.writeEN)
        self.writeEN2Button.clicked.connect(self.writeEN)
        self.startButton.clicked.connect(self.startRead)

    def workVdd(self):
        print('\n' + "Производиться управлене питанием, ожидайте.")
        if not servis_method.all_vdd(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk'), saveOption):
            print('\n' + "Не удалось выполнить настройку питания. Проверте источник напряжения.")
        else:
            if getattr(saveOption, "voltage_state"):
                print('\n' + "Питание включено.")
            else:
                print('\n' + "Питание выключено.")

    def readTemp(self):
        list_temp = []
        try:
            logger.write_log("Чтение температурного кода.", 0)
            for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
                basic_commands_onewire.form_temp_cod_not_active(iterator_mk)
                logger.write_log("Формирование температурного кода в микросхеме " + str(iterator_mk), 0)
            time.sleep(0.5)
            for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
                temp_cod = basic_commands_onewire.read_temp_active(iterator_mk)
                temp = int(temp_cod[0]) | (int(temp_cod[1]) << 8)
                list_temp.append("микросхема: " + str(iterator_mk) + "; COD: " + str(temp))
                logger.write_log("чтение температурного кода в микросхеме " + str(iterator_mk) + "микросхема: " +
                                 str(iterator_mk) + "; COD: " + str(temp), 0)
            print(list_temp)
        except:
            logger.write_log("Произошла ошибка в чтении температурного кода.", 0)
            print('\n' + "Не удалось считать температурный код.")



    def readOTP(self):
        try:
            logger.write_log("Чтение памяти микросхем", 0)
            print("Чтение памяти микросхем")
            for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
                logger.write_log("Чтение памяти микросхемы " + str(iterator_mk), 0)
                print(f' Микросхема: {iterator_mk}')
                for i in range(40):
                    print(str(i) + " : " + str(basic_commands_onewire.read_mem_new_micros_OneWire(iterator_mk, i)))
        except:
            logger.write_log("Произошла ошибка в чтении памяти микросхем", 0)
            print('\n' + "Произошла ошибка в чтении памяти микросхем.")


    def readID(self):
        logger.write_log("Чтение адреса", 0)
        # for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
        #     print(iterator_mk)
        #     address = ""
        #     for i in range(31, 39):
        #         address = address + str(basic_commands_onewire.read_mem_new_micros_OneWire(iterator_mk, i)) + " "
        #     print(address)
        print("В данной серии нет такой команды")

    def writeEN(self):
        try:
            logger.write_log("Запись EN", 0)
            for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
                en = basic_commands_onewire.read_mem_new_micros_OneWire(iterator_mk, 30)
                en1 = en[0] + 1 # EN
                # en1 = en[0] + 4 # циклический режим
                #en1 = en[0] + 5 # циклический режим + EN
                print(str(en[0]) + " _ " + str(en1))
                basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 28, 1)  # ANALOG 7 -
                time.sleep(2)
                basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 30, en1)  # если 204 и 242 в одной посылке, то + 5
                time.sleep(2)
                # basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 27, 255)
                # time.sleep(2)
                # basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 39, 128)
                # time.sleep(2)
        except:
            logger.write_log("Запись EN не выполенно", 0)


    def writeMem(self):
        list_chip = []
        logger.write_log("Запись памяти", 0)
        print("Запись памяти")
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            logger.write_log("Запись памяти в микросхему " + str(iterator_mk), 0)
            print(f'Микросхема : {iterator_mk}')
            # new_chip = micros_chip.Chip(iterator_mk)
            # list_chip.append(new_chip)
            path_to_file = '../data/' + str(iterator_mk) + '.txt'
            TM = TMD.TMD(tm_type='analog', xy_path=path_to_file, annealing_step=0.001, maximum_gap=100,
                         num_points_total=9, kind='cubic',
                         annealing_multiplier=20, left_mutation=-20, right_mutation=20, min_code=100)
            list_m, list_k, list_b, z = TM.execute_point_optimization()
            ddd, standard_deviation, absolute_deviation = utility.plot_graph(TM, (list_m, list_k, list_b, z), plot=False)
            print(standard_deviation)
            if standard_deviation > 10:
                print("Перезапусти меня")

            z.reverse()
            z1 = int(''.join(str(e) for e in z), 2)
            list_m = [round(i/16) for i in list_m]

            str_bin_om = bin(int(TM.minimum))[2:].zfill(16)
            om2 = int(str_bin_om[:8], 2)  # Старшие биты
            om1 = int(str_bin_om[8:], 2)  # Младшие биты

            print("Z " + str(z1))
            print("B " + str(list_b))
            print("K " + str(list_k))
            print("M " + str(list_m))
            print("OM1 " + str(om1))
            print("OM2 " + str(om2))

            logger.write_log("Запись памяти в микросхему " + str(iterator_mk) + "; Z = "
                             + str(z1) + " M = " + str(list_m) + " K = " + str(list_k)
                             + " B = " + str(list_b) + " OM = " + str(TM.minimum)
                             + " OM1 (младший) = " + str(om1) + " OM2 (старший) = " + str(om2), 0)

            # list_m = [18, 33, 42, 62, 75, 83, 90]
            # list_k = [40, 49, 58, 64, 80, 101, 125, 148]
            # list_b = [9, 4, 5, 13, 44, 93, 155, 220]
            # om1 = 209
            # om2 = 243
            # z1 = 252

            # K
            if list_k[0] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 0, list_k[0])
            time.sleep(2)
            if list_k[1] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 1, list_k[1])
            time.sleep(2)
            if list_k[2] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 2, list_k[2])
            time.sleep(2)
            if list_k[3] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 3, list_k[3])
            time.sleep(2)
            if list_k[4] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 4, list_k[4])
            time.sleep(2)
            if list_k[5] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 5, list_k[5])
            time.sleep(2)
            if list_k[6] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 6, list_k[6])
            time.sleep(2)
            if list_k[7] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 7, list_k[7])
            time.sleep(2)
            #
            # if list_k[8] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 31, list_k[8])
            # time.sleep(2)
            # if list_k[9] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 34, list_k[9])
            # time.sleep(2)
            #
            # basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 31, 32)
            # time.sleep(2)
            # basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 34, 32)
            # time.sleep(2)
            #
            # B
            if list_b[0] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 8, list_b[0])
            time.sleep(2)
            if list_b[1] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 9, list_b[1])
            time.sleep(2)
            if list_b[2] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 10, list_b[2])
            time.sleep(2)
            if list_b[3] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 11, list_b[3])
            time.sleep(2)
            if list_b[4] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 12, list_b[4])
            time.sleep(2)
            if list_b[5] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 13, list_b[5])
            time.sleep(2)
            if list_b[6] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 14, list_b[6])
            time.sleep(2)
            if list_b[7] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 15, list_b[7])
            time.sleep(2)
            #
            # if list_b[8] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 32, list_b[8])
            # time.sleep(2)
            # if list_b[9] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 35, list_b[9])
            # time.sleep(2)
            #M
            if list_m[0] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 17, list_m[0])
            time.sleep(2)
            if list_m[1] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 18, list_m[1])
            time.sleep(2)
            if list_m[2] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 19, list_m[2])
            time.sleep(2)
            if list_m[3] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 20, list_m[3])
            time.sleep(2)
            if list_m[4] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 21, list_m[4])
            time.sleep(2)
            if list_m[5] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 22, list_m[5])
            time.sleep(2)
            if list_m[6] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 23, list_m[6])
            time.sleep(2)
            # if list_m[7] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 33, list_m[7])
            # time.sleep(2)
            # if list_m[8] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 36, list_m[8])
            # time.sleep(2)
            #
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 33, 255)
            time.sleep(2)
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 36, 255)
            time.sleep(2)
            #
            #Z1
            if z1 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 16, z1)
            time.sleep(2)
            #Z2
            # if z2 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 37, z2)
            # time.sleep(2)
            #
            #OM1
            if om1 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 24, om1)
            time.sleep(2)
            #OM2
            if om2 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 25, om2)
            time.sleep(2)
        print("Конец записи данных в микросхемы.")
        logger.write_log("Конец записи данных в микросхемы.", 0)


    def startRead(self):
        print("Чтение температурного кода")
        temp_mit = input()
        dict = {}
        for i in range(32):
            print("step = " + str(i))
            list_temp = []
            for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
                basic_commands_onewire.form_temp_cod_not_active(iterator_mk)
            time.sleep(0.5)
            for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
                temp_cod = basic_commands_onewire.read_temp_active(iterator_mk)
                if dict.get(iterator_mk) is None:
                    dict[iterator_mk] = [temp_cod[0] | (temp_cod[1] << 8)]
                else:
                    dict.get(iterator_mk).append(temp_cod[0] | (temp_cod[1] << 8))
                list_temp.append(temp_cod[0] | (temp_cod[1] << 8))
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            list_temp = dict.get(iterator_mk)
            average_cod = round(sum(list_temp) / len(list_temp))
            file_path_data = open('./data/' + str(iterator_mk) + '.txt', 'a')
            file_path_data.write(str(temp_mit) + " " + str(average_cod) + "\n")
            file_path_data.close()
        print("Конец чтения температурного кода")


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
            for i in range(40):
                print(str(i) + " : " + str(basic_commands_onewire.read_mem_new_micros_OneWire(iterator_mk, i)))


    def readID(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
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
            time.sleep(2)

    def write3V(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            en = basic_commands_onewire.read_mem_new_micros_OneWire(iterator_mk, 30)
            print(str(en[0]) + " _ " + str(en[0] + 2))
            en1 = en[0] + 2
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 30, en1)
            time.sleep(2)

    def writeMem(self):
        list_chip = []
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            print("Chip : " + str(iterator_mk))
            new_chip = micros_chip.Chip(iterator_mk)
            list_chip.append(new_chip)
            # test_clc.clc(iterator_mk, new_chip)
            # #mathNewOneWire.coefficients(iterator_mk, new_chip)
            # number_mem_in_chip = 0
            # list_k = getattr(new_chip, "k_list")
            # list_b = getattr(new_chip, "b_list")
            # list_m = getattr(new_chip, "m_list")
            # om1 = getattr(new_chip, "om1")
            # om2 = getattr(new_chip, "om2")
            # z1 = getattr(new_chip, "z")
            # print("K")
            # print(list_k)
            # print("B")
            # print(list_b)
            # print("M")
            # print(list_m)
            # print("Z")
            # print(z1)

            path_to_file = './data/' + str(iterator_mk) + '.txt'
            TM = TMD.TMD(tm_type='10', xy_path=path_to_file, annealing_step=0.001, maximum_gap=100,
                         num_points_total=9, kind='cubic',
                         annealing_multiplier=20, left_mutation=-20, right_mutation=20, min_code=100)
            list_m, list_k, list_b, z = TM.execute_point_optimization()
            z.reverse()
            z1 = int(''.join(str(e) for e in z), 2)
            list_m = [round(i / 16) for i in list_m]
            binCodeEleOM = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            x = int(TM.minimum)  # -64 10micros
            i = 0
            while i < 16:
                y = str(x % 2)
                binCodeEleOM[i] = str(int(y))
                i = i + 1
                x = int(x / 2)

            om1 = binCodeEleOM[:8]
            om2 = binCodeEleOM[8:]

            print("Z " + str(z1))
            print("B " + str(list_b))
            print("K " + str(list_k))
            print("M " + str(list_m))
            print("OM1 " + str(int(str(''.join(om1))[::-1], 2)))
            print("OM2 " + str(int(str(''.join(om2))[::-1], 2)))

            # K
            if list_k[0] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 0, list_k[0])
            time.sleep(2)
            if list_k[1] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 1, list_k[1])
            time.sleep(2)
            if list_k[2] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 2, list_k[2])
            time.sleep(2)
            if list_k[3] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 3, list_k[3])
            time.sleep(2)
            if list_k[4] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 4, list_k[4])
            time.sleep(2)
            if list_k[5] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 5, list_k[5])
            time.sleep(2)
            if list_k[6] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 6, list_k[6])
            time.sleep(2)
            if list_k[7] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 7, list_k[7])
            time.sleep(2)

            # # B
            #list_b[7] = list_b[7]
            if list_b[0] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 8, list_b[0])
            time.sleep(2)
            if list_b[1] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 9, list_b[1])
            time.sleep(2)
            if list_b[2] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 10, list_b[2])
            time.sleep(2)
            if list_b[3] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 11, list_b[3])
            time.sleep(2)
            if list_b[4] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 12, list_b[4])
            time.sleep(2)
            if list_b[5] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 13, list_b[5])
            time.sleep(2)
            if list_b[6] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 14, list_b[6])
            time.sleep(2)
            if list_b[7] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 15, list_b[7])
            time.sleep(2)

            # Z1
            if z1 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 16, z1)
            time.sleep(2)


            # #M
            if list_m[0] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 17, list_m[0])
            time.sleep(2)
            if list_m[1] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 18, list_m[1])
            time.sleep(2)
            if list_m[2] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 19, list_m[2])
            time.sleep(2)
            if list_m[3] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 20, list_m[3])
            time.sleep(2)
            if list_m[4] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 21, list_m[4])
            time.sleep(2)
            if list_m[5] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 22, list_m[5])
            time.sleep(2)
            if list_m[6] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 23, list_m[6])
            time.sleep(2)

            # OM1
            if om1 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 24, om1)
            time.sleep(2)
            # OM2
            if om2 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 25, om2)
            time.sleep(2)


            # Del
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 26, 2)
            time.sleep(2)

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
logger.write_log('\n' + "Запуск программы" + '\n' + "---------------", 0)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    # w.show_CommandsWindow()
    sys.exit(app.exec_())
