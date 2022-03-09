import time
import other.mit as mit
import other.other_devices as other_devices
import logger
import basic_commands_onewire

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
            logger.write_log("Проблемы в микросхеме номер: " + str(iterator_mk) + ", длина массива измеренных значений равна 0", 0)
            continue
        last_average = sum(list_temp) / len(list_temp)
        index = None
        while True:
            flag = True
            for i in list_temp:
                average = sum_list(list_temp.index(i), list_temp)
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

def sleep_in_time(saveOption, temp):
    while True:
        flag = True
        temp_mit = mit.main_function_MIT(saveOption)
        print(f'Температура на МИТ {temp_mit[0]}, {temp_mit[1]}, {temp_mit[2]}, температура на SPEC {temp}')
        for i in temp_mit:
            if not (temp - 2) <= i <= (temp + 2):
                flag = False
                other_devices.work_spec(temp)
                break
        if flag:
            break

def action_check():
    check = input("Подтвердите действие." + "\n")
    if check == "y":
        return True
    return False

def sum_list(iterator, y):
    new_x = list(y)
    new_x.pop(iterator)
    return sum(new_x)/len(new_x)
