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


class Analog_Chip:

    def __init__(self):
        # TODO реализовать адекватный конструктор
        print("Объект создан")

    # def workVdd(self):
    #     print('\n' + "Производиться управлене питанием, ожидайте.")
    #     if not servis_method.all_vdd(save_options.SaveOption()):
    #         print('\n' + "Не удалось выполнить настройку питания. Проверте источник напряжения.")
    #     else:
    #         if getattr(save_options.SaveOption(), "voltage_state"):
    #             print('\n' + "Питание включено.")
    #         else:
    #             print('\n' + "Питание выключено.")


    def readTemp(self):
        list_temp = []
        if not helper_methods.power_check(save_options.SaveOption()):
            return
        try:
            print("Чтение температурного кода.")
            logger.write_log("Чтение температурного кода.", 0)
            list_IC = getattr(save_options.SaveOption(), 'list_IC')
            for iterator_mk in list_IC:
                basic_commands_onewire.form_temp_cod_not_active(iterator_mk)
                logger.write_log("Формирование температурного кода в микросхеме " + str(iterator_mk), 0)
            time.sleep(0.5)
            for iterator_mk in list_IC:
                temp_cod = basic_commands_onewire.read_temp_active(iterator_mk)
                temp = int(temp_cod[0]) | (int(temp_cod[1]) << 8)
                list_temp.append("микросхема: " + str(iterator_mk) + "; COD: " + str(temp))
                logger.write_log("чтение температурного кода в микросхеме " + str(iterator_mk) + " микросхема: "
                                 + str(iterator_mk) + "; COD: " + str(temp), 0)
            print(list_temp)
        except:
            logger.write_log("Произошла ошибка в чтении температурного кода.", 0)
            print('\n' + "Не удалось считать температурный код.")


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
            if not helper_methods.action_check():
                return
            if not helper_methods.power_check(save_options.SaveOption()):
                return
            logger.write_log("Запись EN", 0)
            list_IC = getattr(save_options.SaveOption(), 'list_IC')
            for iterator_mk in list_IC:
                print(f'микросхема {iterator_mk}')
                en = basic_commands_onewire.read_mem_new_micros_OneWire(iterator_mk, 30)
                en1 = en[0] + 1  # EN
                print(str(en[0]) + " _ " + str(en1))
                basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 30,
                                                                    en1)  # если 204 и 242 в одной посылке, то + 5
                basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 39, 128)
        except:
            logger.write_log("Запись EN не выполенно", 0)


    def writeMem(self):
        if not helper_methods.action_check():
            return
        if not helper_methods.power_check(save_options.SaveOption()):
            return
        list_chip = []
        logger.write_log("Запись памяти", 0)
        print("Запись памяти")
        list_IC = getattr(save_options.SaveOption(), 'list_IC')
        print(list_IC)
        for iterator_mk in list_IC:
            logger.write_log("Запись памяти в микросхему " + str(iterator_mk), 0)
            print(f'Микросхема : {iterator_mk}')
            # new_chip = micros_chip.Chip(iterator_mk)
            # list_chip.append(new_chip)
            path_to_file = '../data/' + str(iterator_mk) + '.txt'
            TM = TMD.TMD(tm_type='analog', xy_path=path_to_file, annealing_step=0.001, maximum_gap=100,
                         num_points_total=9, kind='cubic',
                         annealing_multiplier=20, left_mutation=-20, right_mutation=20, min_code=100)
            list_m, list_k, list_b, z = TM.execute_point_optimization()
            ddd, standard_deviation, absolute_deviation = utility.plot_graph(TM, (list_m, list_k, list_b, z),
                                                                             plot=False)
            z_te = []
            for i in z:
                if i >= 0:
                    z_te.append(0)
                else:
                    z_te.append(1)
            print(standard_deviation)
            if standard_deviation > 10:
                print("Перезапусти меня")
                exit(0)
            z_te.reverse()
            z1 = int(''.join(str(e) for e in z_te), 2)
            list_m = [round(i / 16) for i in list_m]

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
            if list_k[1] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 1, list_k[1])
            if list_k[2] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 2, list_k[2])
            if list_k[3] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 3, list_k[3])
            if list_k[4] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 4, list_k[4])
            if list_k[5] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 5, list_k[5])
            if list_k[6] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 6, list_k[6])
            if list_k[7] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 7, list_k[7])
            #
            # if list_k[8] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 31, list_k[8])
            # if list_k[9] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 34, list_k[9])
            #
            # basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 31, 32)
            # basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 34, 32)
            #
            # B
            if list_b[0] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 8, list_b[0])
            if list_b[1] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 9, list_b[1])
            if list_b[2] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 10, list_b[2])
            if list_b[3] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 11, list_b[3])
            if list_b[4] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 12, list_b[4])
            if list_b[5] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 13, list_b[5])
            if list_b[6] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 14, list_b[6])
            if list_b[7] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 15, list_b[7])
            #
            # if list_b[8] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 32, list_b[8])
            # if list_b[9] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 35, list_b[9])
            #
            # M
            if list_m[0] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 17, list_m[0])
            if list_m[1] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 18, list_m[1])
            if list_m[2] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 19, list_m[2])
            if list_m[3] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 20, list_m[3])
            if list_m[4] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 21, list_m[4])
            if list_m[5] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 22, list_m[5])
            if list_m[6] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 23, list_m[6])
            # if list_m[7] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 33, list_m[7])
            # if list_m[8] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 36, list_m[8])
            #
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 33, 255)
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 36, 255)
            #
            # Z1
            if z1 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 16, z1)
            # Z2
            # if z2 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 37, z2)
            #
            # OM1
            if om1 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 24, om1)
            # OM2
            if om2 != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 25, om2)
        print("Конец записи данных в микросхемы.")
        logger.write_log("Конец записи данных в микросхемы.", 0)


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


    def write3V(self):
        if not helper_methods.action_check():
            return
        if not helper_methods.power_check(save_options.SaveOption()):
            return
        print(f'Перевод микросхем в 3.3 Вольта')
        list_IC = getattr(save_options.SaveOption(), 'list_IC')
        for iterator_mk in list_IC:
            logger.write_log("Перевод микросхемы " + str(iterator_mk) + "в 3.3 Вольта", 0)
            print(f'Перевод микросхемы {iterator_mk} в 3.3 Вольта')
            en = basic_commands_onewire.read_mem_new_micros_OneWire(iterator_mk, 30)
            print(str(en[0]) + " _ " + str(en[0] + 2))
            en1 = en[0] + 2
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 30, en1)
        print(f'Конец перевода микросхем в 3.3 Вольта')


    def saveArchive(self):
        other_functions.main_save_archive("13")


    def presetting(self):
        try:
            if not helper_methods.action_check():
                return
            if not helper_methods.power_check(save_options.SaveOption()):
                return
            logger.write_log("Предварительная настройка", 0)
            print("Предварительная настройка")
            list_IC = getattr(save_options.SaveOption(), 'list_IC')
            for iterator_mk in list_IC:
                print(f'микросхема {iterator_mk}')
                en = basic_commands_onewire.read_mem_new_micros_OneWire(iterator_mk, 30)
                en1 = en[0] + 4  # циклический режим
                print(str(en[0]) + " _ " + str(en1))
                basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 28, 1)  # ANALOG 7 -
                basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 30,
                                                                    en1)  # если 204 и 242 в одной посылке, то + 5
                basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 27, 255)
        except:
            logger.write_log("Предварительная настройка не выполена", 0)