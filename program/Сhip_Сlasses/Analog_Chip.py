import time

import program.logger as logger
import program.basic_commands_onewire as basic_commands_onewire
import program.save_options as save_options
import program.mathem.TMD as TMD
import program.mathem.utility as utility
import program.other.other_devices as other_devices
import program.other.mit as mit
import program.other.other_functions as other_functions


class Analog_Chip:
    type = 13

    # def workVdd(self):
    #     print('\n' + "Производиться управлене питанием, ожидайте.")
    #     if not servis_method.all_vdd(save_options.SaveOption()):
    #         print('\n' + "Не удалось выполнить настройку питания. Проверте источник напряжения.")
    #     else:
    #         if getattr(save_options.SaveOption(), "voltage_state"):
    #             print('\n' + "Питание включено.")
    #         else:
    #             print('\n' + "Питание выключено.")

    def readTemp(self, iterator_mk):
        temp_cod = basic_commands_onewire.read_temp_active(iterator_mk)
        temp = int(temp_cod[0]) | (int(temp_cod[1]) << 8)
        logger.write_log("чтение температурного кода в микросхеме " + str(iterator_mk) + " микросхема: "
                         + str(iterator_mk) + "; COD: " + str(temp), 0)
        return "микросхема: " + str(iterator_mk) + "; COD: " + str(temp)

    def readMem(self, iterator_mk):
        logger.write_log("Чтение памяти микросхемы " + str(iterator_mk), 0)
        print(f' Микросхема: {iterator_mk}')
        list_mem = []
        for i in range(40):
            mem = basic_commands_onewire.read_mem_new_micros_OneWire(iterator_mk, i)
            list_mem.append(mem)
        logger.write_log("Чтение памяти микросхемы " + str(iterator_mk) + " " + list_mem, 0)
        print(f"Чтение памяти микросхемы: {iterator_mk} ; память {list_mem}")

    def readID(self, iterator_mk):
        logger.write_log("Чтение адреса микросхемы " + str(iterator_mk) + " микросхема: "
                         + str(iterator_mk) + "; В данной микросхеме нет адреса.", 0)
        return "микросхема: " + str(iterator_mk) + "; В данной микросхеме нет адреса."

    def writeEN(self, iterator_mk):
        if other_functions.smart_mode_check():
            if not other_functions.read_file_and_check_run_function(iterator_mk, 3):
                print(f"Микросхема под номером {iterator_mk} не может выполнить данную функцию, \n так как не "
                      f"выолднены предидущие итерации")
                logger.write_log("Микросхема под номером " + str(iterator_mk) + "не может выполнить данную функцию, "
                                                                                "так как не выолднены предидущие "
                                                                                "итерации", 0)
                return
        print(f'микросхема {iterator_mk}')
        en = basic_commands_onewire.read_mem_new_micros_OneWire(iterator_mk, 30)
        en1 = en[0] + 1  # EN
        print(str(en[0]) + " _ " + str(en1))
        basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 30, en1)
        basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 39, 128)

        other_functions.write_file_in_run_function(iterator_mk, 5)

    def writeMem(self, iterator_mk):
        if other_functions.smart_mode_check():
            if not other_functions.read_file_and_check_run_function(iterator_mk, 2):
                print(f"Микросхема под номером {iterator_mk} не может выполнить данную функцию, \n так как не "
                      f"выолднены предидущие итерации")
                logger.write_log("Микросхема под номером " + str(iterator_mk) + "не может выполнить данную функцию, "
                                                                                "так как не выолднены предидущие "
                                                                                "итерации", 0)
                return
        logger.write_log("Запись памяти в микросхему " + str(iterator_mk), 0)
        print(f'Микросхема : {iterator_mk}')
        path_to_file = '../data/' + str(iterator_mk) + '.txt'
        TM = TMD.TMD(tm_type='analog', xy_path=path_to_file, annealing_step=0.001, maximum_gap=100,
                     num_points_total=9, kind='cubic',
                     annealing_multiplier=20, left_mutation=-20, right_mutation=20, min_code=100)
        list_m, list_k, list_b, z = TM.execute_point_optimization()
        ddd, standard_deviation, absolute_deviation = utility.plot_graph(TM, (list_m, list_k, list_b, z),
                                                                         plot=False)
        print(TM.interpol(-29.9))
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

        logger.write_log("Запись памяти в микросхему " + str(iterator_mk) + "; Z = "
                         + str(z1) + " M = " + str(list_m) + " K = " + str(list_k)
                         + " B = " + str(list_b) + " OM = " + str(TM.minimum)
                         + " OM1 (младший) = " + str(om1) + " OM2 (старший) = " + str(om2), 0)

        # K
        if list_k[0] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 0, list_k[0])
        if list_k[1] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 1, list_k[1])
        if list_k[2] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 2, list_k[2])
        if list_k[3] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 3, list_k[3])
        if list_k[4] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 4, list_k[4])
        if list_k[5] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 5, list_k[5])
        if list_k[6] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 6, list_k[6])
        if list_k[7] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 7, list_k[7])
        # if list_k[8] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 31, list_k[8])
        # if list_k[9] != 0: basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 34, list_k[9])
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

        other_functions.write_file_in_run_function(iterator_mk, 3)

    def startRead(self, iterator_mk):
        self.read_temp_and_write_in_file(save_options.SaveOption())

    def write3V(self, iterator_mk):
        if not other_functions.power_check(save_options.SaveOption()):
            return
        if not other_functions.action_check():
            return
        print(f'Перевод микросхем в 3.3 Вольта')
        list_IC = getattr(save_options.SaveOption(), 'list_IC')
        for iterator_mk in list_IC:
            if other_functions.smart_mode_check():
                if not other_functions.read_file_and_check_run_function(iterator_mk, 3):
                    print(f"Микросхема под номером {iterator_mk} не может выполнить данную функцию, \n так как не "
                          f"выолднены предидущие итерации")
                    return
            logger.write_log("Перевод микросхемы " + str(iterator_mk) + "в 3.3 Вольта", 0)
            print(f'Перевод микросхемы {iterator_mk} в 3.3 Вольта')
            en = basic_commands_onewire.read_mem_new_micros_OneWire(iterator_mk, 30)
            print(str(en[0]) + " _ " + str(en[0] + 2))
            en1 = en[0] + 2
            basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 30, en1)
            other_functions.write_file_in_run_function(iterator_mk, 4)
        print(f'Конец перевода микросхем в 3.3 Вольта')

    def saveArchive(self, iterator_mk):
        other_functions.main_save_archive("13")

    def presetting(self, iterator_mk):
        en = basic_commands_onewire.read_mem_new_micros_OneWire(iterator_mk, 30)
        en1 = en[0] + 4  # циклический режим
        print(str(en[0]) + " _ " + str(en1))
        basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 28, 1)  # ANALOG 7 -
        basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 30,
                                                            en1)  # если 204 и 242 в одной посылке, то + 5
        basic_commands_onewire.write_mem_new_micros_OneWire(iterator_mk, 27, 255)

    # Запись в файл.
    def read_temp_and_write_in_file(self, iterator_mk):
        saveOption = save_options.SaveOption()
        temp_mit = mit.main_function_MIT(saveOption)
        list_IC = getattr(saveOption, 'list_IC')
        dict = {}
        for iterator_mk in list_IC:
            for i in range(32):
                print(f'step = {i}; mk = {iterator_mk}')
                time.sleep(0.05)
                temp_cod = basic_commands_onewire.read_temp_active(iterator_mk)
                print(temp_cod)
                if len(temp_cod) < 2:
                    continue
                if dict.get(iterator_mk) is None:
                    dict[iterator_mk] = [temp_cod[0] | (temp_cod[1] << 8)]
                else:
                    dict.get(iterator_mk).append(temp_cod[0] | (temp_cod[1] << 8))
        for iterator_mk in list_IC:
            temp = 0
            # TODO так не должно быть. Необходимо убрать костыль
            if 1 <= iterator_mk <= 6:
                temp = temp_mit[0]
            elif 7 <= iterator_mk <= 12:
                temp = temp_mit[1]
            elif 13 <= iterator_mk <= 16:
                temp = temp_mit[2]
            list_temp = dict.get(iterator_mk)
            for i in range(len(list_temp)):
                try:
                    list_temp.remove(65535)
                except:
                    break
            if len(list_temp) == 0:
                logger.write_log(
                    "Проблемы в микросхеме номер: " + str(iterator_mk) + ", длина массива измеренных значений равна 0",
                    0)
                continue
            last_average = sum(list_temp) / len(list_temp)
            index = None
            while True:
                flag = True
                for i in list_temp:
                    average = other_functions.sum_list(list_temp.index(i), list_temp)
                    if abs(average - last_average) > 7:
                        index = list_temp.index(i)
                        last_average = average
                        logger.write_log("Данные измерений при температуре " + str(temp) + "; микросхема номер "
                                         + str(iterator_mk) + "; Удалено значение = " + str(i), 0)
                        flag = False
                        break
                if flag:
                    break
                list_temp.pop(index)

            average_cod = round(sum(list_temp) / len(list_temp))
            logger.write_log("Данные измерений при температуре " + str(temp) + "; микросхема номер "
                             + str(iterator_mk) + "; коды = min:" + str(min(list_temp)) + " ave_cod:" + str(average_cod)
                             + " max:" + str(max(list_temp)) + " len:" + str(len(list_temp))
                             + " list_temp: " + str(list_temp), 0)
            file_path_data = open('../data/' + str(iterator_mk) + '.txt', 'a')
            file_path_data.write(str(temp) + " " + str(average_cod) + "\n")
            file_path_data.close()
