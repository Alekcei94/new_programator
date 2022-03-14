import time

import program.servis_method as servis_method
import program.helper_methods as helper_methods
import program.logger as logger
import program.basic_commands_onewire as basic_commands_onewire
import program.save_options as save_options
import program.mathem.TMD as TMD
import program.mathem.utility as utility
import program.other.other_devices as other_devices
import program.other.other_functions as other_functions


class OneWire_Chip:

    def __init__(self):
        # TODO реализовать адекватный конструктор
        print("Объект создан")

    # def workVdd(self):
    #     print("Start VDD")
    #     servis_method.all_vdd(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk'), saveOption)
    #     print("FINISH VDD")

    def readTemp(self):
        list_temp = []
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            basic_commands_onewire.form_temp_cod_not_active(iterator_mk)
        time.sleep(2)
        # servis_method.sleep_slave_1(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk'), 3000)
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            temp_cod = basic_commands_onewire.read_temp_active(iterator_mk)
            if temp_cod[8] == servis_method.test_crc(temp_cod[0], temp_cod[1], temp_cod[2], temp_cod[3], temp_cod[4],
                                                     temp_cod[5], temp_cod[6], temp_cod[7]):
                temp = int(temp_cod[0]) | (int(temp_cod[1]) << 8)
                if temp >= 63488:
                    temp = -1 * (temp - 63488)
                list_temp.append(
                    "микросхема: " + str(iterator_mk) + "; COD: " + str(temp) + "; Temp: " + str(float(temp * 0.0625)))
            else:
                list_temp.append("ER")

        print(list_temp)

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

    def write3V(self):
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            en = basic_commands_onewire.read_mem_new_micros_OneWire(iterator_mk, 30)
            print(str(en[0]) + " _ " + str(en[0] + 2))
            en1 = en[0] + 2
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 30, en1)

    def writeMem(self):
        list_chip = []
        for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
            print("Chip : " + str(iterator_mk))
            new_chip = micros_chip.Chip(iterator_mk)
            list_chip.append(new_chip)

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
            if list_k[1] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 1, list_k[1])
            if list_k[2] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 2, list_k[2])
            if list_k[3] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 3, list_k[3])
            if list_k[4] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 4, list_k[4])
            if list_k[5] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 5, list_k[5])
            if list_k[6] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 6, list_k[6])
            if list_k[7] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 7, list_k[7])

            # # B
            if list_b[0] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 8, list_b[0])
            if list_b[1] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 9, list_b[1])
            if list_b[2] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 10, list_b[2])
            if list_b[3] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 11, list_b[3])
            if list_b[4] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 12, list_b[4])
            if list_b[5] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 13, list_b[5])
            if list_b[6] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 14, list_b[6])
            if list_b[7] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 15, list_b[7])

            # Z1
            if z1 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 16, z1)

            # M
            if list_m[0] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 17, list_m[0])
            if list_m[1] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 18, list_m[1])
            if list_m[2] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 19, list_m[2])
            if list_m[3] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 20, list_m[3])
            if list_m[4] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 21, list_m[4])
            if list_m[5] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 22, list_m[5])
            if list_m[6] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 23, list_m[6])

            # OM1
            if om1 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 24, om1)
            # OM2
            if om2 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 25, om2)

            # Del
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 26, 2)

    def readMem(self):
        if not helper_methods.power_check(save_options.SaveOption()):
            return
        try:
            logger.write_log("Чтение памяти микросхем", 0)
            print("Чтение памяти микросхем")
            list_IC = getattr(save_options.SaveOption(), 'list_IC')
            for iterator_mk in list_IC:
                logger.write_log("Чтение памяти микросхемы " + str(iterator_mk), 0)
                print(f' Микросхема: {iterator_mk}')
                mem_str = ""
                for i in range(40):
                    mem = basic_commands_onewire.read_mem_new_micros_OneWire(iterator_mk, i)
                    print(str(i) + " : " + str(mem))
                    mem_str += " " + str(mem)
                logger.write_log("Чтение памяти микросхемы " + str(iterator_mk) + " " + mem_str, 0)
        except:
            logger.write_log("Произошла ошибка в чтении памяти микросхем", 0)
            print('\n' + "Произошла ошибка в чтении памяти микросхем.")

    def startRead(self):
        if not helper_methods.power_check(save_options.SaveOption()):
            return
        print("Старт измерений")
        logger.write_log("Старт измерений", 0)
        list_IC = getattr(save_options.SaveOption(), 'list_IC')
        list_temp_spec = getattr(save_options.SaveOption(), 'list_temperature')
        print(f'Список температур {list_temp_spec}')
        logger.write_log("Список температур " + str(list_temp_spec), 0)
        for temp_spec in list_temp_spec:
            other_devices.work_spec(temp_spec)
            helper_methods.sleep_in_time(save_options.SaveOption(), temp_spec)
            for i in range(2):
                print(f'Осталось {20 - i * 10} минут, температура {temp_spec}')
                time.sleep(600)
            other_functions.read_temp_and_write_in_file(save_options.SaveOption())
            logger.write_log("", 0)
        print("Конец чтения температурного кода")
        logger.write_log("Конец измерений", 0)

    def saveArchive(self):
        other_functions.main_save_archive("13")

    def presetting(self):
        print("Данной функции нет в данной микросхеме")