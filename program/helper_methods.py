import time
import other.mit as mit
import other.other_devices as other_devices
import logger
import basic_commands_onewire

def read_temp_and_write_in_file(saveOption):
    temp_mit = mit.main_function_MIT(saveOption)
    dict = {}
    for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
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
    for iterator_mk in range(getattr(saveOption, 'first_mk'), getattr(saveOption, 'last_mk') + 1):
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
