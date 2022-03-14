import datetime
import os
import shutil
import program.other.mit as mit
import time
import program.basic_commands_onewire as basic_commands_onewire
import program.helper_methods as helper_methods
import program.logger as logger


# Сохранение данных в архив
# version_mk - входные данные версия микросхемы. (10, 11, 12, 13)
def main_save_archive(version_mk):
    now = datetime.datetime.now()
    form_path = str(now.day) + "_" + str(now.month) + "_" + str(now.year)
    try:
        os.mkdir("../archive/" + str(version_mk) + "/" + form_path)
    except:
        print("Создать директорию не удалось " + str(os.getcwd()))
    path_data_archive = "../archive/" + str(version_mk) + "/" + form_path + "/data/"
    path_address_archive = "../archive/" + str(version_mk) + "/" + form_path + "/microchip_life/"
    path_finaly_test_archive = "../archive/" + str(version_mk) + "/" + form_path + "/logger/"
    try:
        os.mkdir(path_data_archive)
        os.mkdir(path_address_archive)
        os.mkdir(path_finaly_test_archive)
    except:
        print("Создать директорию не удалось")

    list_file_data = os.listdir("../data/")
    for i in list_file_data:
        shutil.copyfile("../data/" + i, path_data_archive + i)
        os.remove("../data/" + i)
    list_file_finaly_test = os.listdir("../logger/")
    for i in list_file_finaly_test:
        shutil.copyfile("../logger/" + i, path_finaly_test_archive + i)
        os.remove("../logger/" + i)
    list_file_data = os.listdir("../microchip_life/")
    for i in list_file_data:
        shutil.copyfile("../microchip_life/" + i, path_address_archive + i)
        os.remove("../microchip_life/" + i)

# Запись в файл.
# TODO Данная функция должна быть не тут.
def read_temp_and_write_in_file(saveOption):
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
                "Проблемы в микросхеме номер: " + str(iterator_mk) + ", длина массива измеренных значений равна 0", 0)
            continue
        last_average = sum(list_temp) / len(list_temp)
        index = None
        while True:
            flag = True
            for i in list_temp:
                average = helper_methods.sum_list(list_temp.index(i), list_temp)
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
