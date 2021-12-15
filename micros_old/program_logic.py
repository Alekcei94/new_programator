# -*- coding: utf-8 -*-
import os
import os.path
import time
from threading import Thread

from scipy import interpolate

import other_devices

'''
COMMANDS MICROCHIP
'''


# WRITE OTP MEMORY
def write_OTP_block():
    if check_click("Записать память ОТР?"):
        for i in range(get_number_start_chip(), get_number_finish_chip() + 1):
            calculation_ADDRESS_and_KOD(i)
            iter = 0
            while iter < 25:
                write_package(i, 1, 0, 0, 0, 0, 0, 0, 0, 0, textbox)
                time.sleep(1)
                iter += 1
                if check_mess_microchip():
                    break
            time.sleep(1)


# READ OTP MEMORY
def read_OTP_block():
    for i in range(get_number_start_chip(), get_number_finish_chip() + 1):
        give_me_OTP_address(i)


# WRITE MAIN ADDRESS CHIP
def write_address():
    if check_click("Записать основной адрес?"):
        for i in range(get_number_start_chip(), get_number_finish_chip() + 1):
            write_main_address(i)


# WRITE COEFFICIENT CHIP K AND B
def write_coefficient_k_and_b():
    if check_click("Записать коэффициенты К и В"):
        for i in range(get_number_start_chip(), get_number_finish_chip() + 1):
            calculation_coefficients(i)


# FINALY TEST ALL CHIP
def finally_test_all_chip():
    quentity_mk = get_number_start_chip() + get_number_finish_chip() - 1
    other_devices.work_spec(125)
    time.sleep(2400)
    i = 125
    while i >= -60:
        for step_200 in range(int(144 / quentity_mk)):
            list_temp = []
            port = get_number_start_chip()
            list_temp = check_real_temperature()
            print("List temp = " + str(list_temp))
            while list_temp is None:
                list_temp = check_real_temperature()
            for temp in list_temp:
                print("Step = " + str(step_200) + "; port = " + str(port) + "; temp chip = " + str(
                    temp) + "temp spec = " + str(i))
                file_text = open('../finally_test/' + str(port) + '.txt', 'a')
                file_text.write(str(temp) + '\n')
                port += 1
        i -= 2
        other_devices.work_spec(i)

    for i in range(get_number_start_chip(), get_number_finish_chip() + 1):
        file_path_data = open('../finally_test/' + str(i) + '.txt', 'r')
        list_data_file = []
        for line in file_path_data:
            list_data_file.append(float(line))
        for line in range(13, len(list_data_file) - 1):
            if list_data_file[line] < -200:
                continue
            if abs((list_data_file[line]) - (list_data_file[line + 1])) > 1.5 and (list_data_file[line]) <= (
                    list_data_file[line + 1]):
                print("Error work chip = " + str(i) + "; temp left = " + str(
                    list_data_file[line]) + ' temp last = ' + str(list_data_file[line + 1]) + '\n')
                file_text = open('../finally_test/ERROR_list.txt', 'a')
                file_text.write("Error work chip = " + str(i) + "; temp left = " + str(
                    list_data_file[line]) + ' temp last = ' + str(list_data_file[line + 1]) + '\n')
    print("Test finished!!!!")


# WRITE DATA IN FILE
def read_temperature_and_write_data_file(textbox):
    global path_in_data
    if check_click("Начать измерения?"):
        temperature_list = get_list_temperature()
        for i in range(len(temperature_list)):
            # work_termostrim(temperature_list[i])
            other_devices.work_spec(temperature_list[i])
            if i == 0:
                for j in range(8):
                    # time.sleep(4800)
                    print("Time passed " + str(j * 10) + " minutes. Temperature = " + str(
                        temperature_list[i]) + "Full time = 80 minutes.")
                    time.sleep(600)
            if i < 5 and i > 0:
                for j in range(4):
                    print("Time passed " + str(j * 10) + " minutes. Temperature = " + str(
                        temperature_list[i]) + "Full time = 40 minutes.")
                    time.sleep(600)
            # time.sleep(2400)
            if i == 5:
                # time.sleep(3600)
                for j in range(6):
                    print("Time passed " + str(j * 10) + " minutes. Temperature = " + str(
                        temperature_list[i]) + "Full time = 60 minutes.")
                    time.sleep(600)
            array_temperature = main_function_MIT(get_com_port_MIT(), form_array_list_port())
            list_line_binary = read_temperature()
            if list_line_binary == None:
                list_line_binary = read_temperature()
            port = get_number_start_chip()
            iterator = 0
            while True:
                time.sleep(0.5)
                flag_read = True
                for elem in list_line_binary:
                    if len(elem) == 0:
                        print("Double start read temperature")
                        flag_read = False
                        list_line_binary = read_temperature()
                if flag_read:
                    break
            write_temperature(array_temperature)
            for elem in list_line_binary:
                try:
                    if len(elem) == 0:
                        print("ERROR" + str(port))
                        port += 1
                        continue
                    real_temperature_12_bit = elem[4:len(elem)]
                    file_text = open(path_in_data + str(port) + '.txt', 'a')
                    file_text.write(
                        str(array_temperature[get_temperature_in_chip_on_MIT(array_temperature, port)]) + " " + str(
                            int(real_temperature_12_bit, 2)) + " " + str(elem) + '\n')
                    file_text.close()
                    port += 1
                    iterator += 1
                except:
                    port += 1
                    iterator += 1
        other_devices.work_spec(25)


def get_mid_number_array_temperature(array_temperature):
    sum = 0
    size = len(array_temperature) - 1
    for i in range(len(array_temperature) - 1):
        sum += array_temperature[i]
    total = sum / size
    total = round(total, 2)
    return total


def work_new_path():
    if check_click("Загрузили новую партию микросхем?"):
        new_file_main_address()
        new_parth_temp()
        f = open('../data/file_error.txt', 'w')
        f.close()


'''
END COMMANDS MICROCHIP
'''
'''
FORM ADDRESS FILE
'''


def form_address_file():
    if check_click(
            "Запистаь все адреса микросхем в файл?" + "\n" + "ВАЖНО. Данная функция необходима только при работе с новой партией."):
        str = read_address()
        f = open('../data/address.txt', 'w')
        for i in str:
            f.write(i + '\n')
        f.close


def check_address():
    str = read_address()
    str_check = []
    f = open('./address.txt', 'r')
    for i in f:
        str_check.append(i)
    for i in range(len(str)):
        if str[i] != str_check[i]:
            print(str[i] + " --> " + str_check[i])


'''
END FORM ADDRESS FILE
'''

'''
TEST BLOCK 
'''


def check_real_temperature():
    form_temperature_in_all_chips()
    if not check_mess_microchip():
        return
    time.sleep(3)
    list_temp = []
    for i in range(get_number_start_chip(), get_number_finish_chip() + 1):
        time.sleep(0.3)
        try:
            list_temp.append(give_real_temperature(i))
        except:
            list_temp.append(-999)
            print('chip ' + str(i) + ' no work')
    return list_temp


def give_real_temperature(number_chip):
    command = 2
    parameters = 0  # ? OR 2
    write_package(number_chip, command, parameters, 0, 0, 0, 0, 0, 0, 0, textbox)
    for i in range(25):
        time.sleep(0.3)
        bit_in_chip = ser.readlines()
        print(str(bit_in_chip))
        if len(bit_in_chip) > 0:
            break
    new_byte = (str(bit_in_chip)[6:len(bit_in_chip) - 5])
    if len(new_byte) == 0:
        print('Chip ' + str(number_chip) + ' : ' + 'no temperature' + '\n')
    temperature = 1
    if new_byte[0] == '1':
        temperature = -1
        test = []
        for iter_bit in range(1, len(new_byte)):
            if new_byte[iter_bit] == "1":
                test.append('0')
            else:
                test.append('1')
        str_test = "".join(test)
        temperature = temperature * int(str_test, 2) * 0.0625
        print(temperature)
    else:
        temperature = temperature * int(new_byte, 2) * 0.0625
        print(temperature)
    return temperature


'''
BLOCK VERIFICATION WORK CHIPS
'''


# VERIFICATION CHIPS
def verification_chips():
    global max_current
    write_package(255, 1, 0, 0, 0, 0, 0, 0, 0, 0, textbox)
    time.sleep(0.5)
    for i in range(get_number_start_chip(), get_number_finish_chip() + 1):
        # print (i)
        write_package(i, 1, 1, 0, 0, 0, 0, 0, 0, 0, textbox)
        time.sleep(0.5)
        current = block_check_current_chip(i)
        if current >= max_current:
            continue
        current_array = []
        thread_current = Thread(target=form_temperature_in_all_chips, args=())
        for j in range(16):
            if j == 4:
                thread_current.start()
            current_array.append(block_check_current_chip(i))
            time.sleep(0.2)
        thread_current.join()
        print(current_array)
        if max(current_array) >= max_current:
            print("ERROR current chip " + str(i) + " = " + str(current))
        write_package(i, 1, 0, 0, 0, 0, 0, 0, 0, 0, textbox)
        time.sleep(0.5)
    write_package(255, 1, 0, 0, 0, 0, 0, 0, 0, 0, textbox)


'''
END BLOCK VERIFICATION WORK CHIPS 
'''

'''
BLOCK WRITE REZ
'''


# WRITE REZ
def write_REZ(binary_cod):
    switch_case = {
        23: 0,
        22: 1,
        21: 2,
        20: 3,
        19: 4,
        18: 5,
        17: 6,
        16: 7,
        15: 8,
        14: 9,
        13: 10,
        12: 11,
        11: 12,
    }
    for i in range(4, 16):
        if binary_cod[i] == "1":
            print(str(28 - i))
            try:
                data_1 = switch_case[28 - i]
                print(data_1)
                return data_1
            except:
                print('Error REZ not True in chip ' + str(number_chip) + '\n')


'''
END BLOCK WRITE REZ
'''

'''
BLOCK SAVE ARCHIVE
'''

'''
END BLOCK SAVE ARCHIVE
'''

'''
BLOCK WRITE COEFFICIENTS
'''


# MAIN COEFFICIENT CALCULATION METHOD
def calculation_coefficients(number_chip):
    x_list_in_file, y_list_in_file = readFile(str(number_chip))

    k, b = get_k_and_b(x_list_in_file, y_list_in_file)

    k_ideal, b_ideal = get_ideal_k_and_b()
    k_real = round(float(k_ideal / k), 4)
    b_real = round((-1 * ((k_ideal / k) * b) + b_ideal), 0)

    write_coefficient(k_real, b_real, number_chip)


# METHOD OF RECORDING THE COEFFICIENTS OF K AND B IN CHIP
def write_coefficient(coefK, coefB, number_chip):
    try:
        print('Chip = ' + str(number_chip) + ' coefK = ' + str(coefK) + ' coefB = ' + str(coefB) + '\n')
        bin_code_coef_b = []
        bin_code_corf_k = []

        x = int(coefB)
        bin_code_ele_b = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        i = 0
        if coefB < 0:
            bin_code_ele_b[13] = 1
            x = x * (-1)
        else:
            bin_code_ele_b[13] = 0
        n = ""
        while x > 0:
            y = str(x % 2)
            if i < 13:
                bin_code_ele_b[i] = int(y)
                i = i + 1
            else:
                break
            x = int(x / 2)
        coef_b_text = ""
        for z in bin_code_ele_b:
            bin_code_coef_b.append(z)
            coef_b_text = coef_b_text + str(z)
        print("b = " + coef_b_text)

        x = float(coefK)
        bin_code_ele_k = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        int_x = int(x)
        i = 10
        while i < 13:
            y = str(int_x % 2)
            bin_code_ele_k[i] = int(y)
            i = i + 1
            int_x = int(int_x / 2)
        int_y = float(coefK) - int(coefK)
        i = 9
        while i >= 0:
            z = int_y * 2
            bin_code_ele_k[i] = int(z)
            int_y = float(z) - int(z)
            i = i - 1
        coefk_k = ""
        for ele in bin_code_ele_k:
            coefk_k = coefk_k + str(ele)
            bin_code_corf_k.append(ele)
        print("k = " + coefk_k)

        pacet = []
        for i in range(0, 13):
            pacet.append(bin_code_corf_k[i])
        for i in range(0, 14):
            pacet.append(bin_code_coef_b[i])

        # enable 1
        pacet.append(1)
        for i in range(4):
            pacet.append(0)
        text = ""
        iterat = 0
        win_test = []
        for i in range(len(pacet) + 1):
            if iterat < 8:
                text = text + str(pacet[i])
                iterat = iterat + 1
            else:
                not_invers = list(text)
                nul = 7
                invers = ""
                for j in range(8):
                    invers = invers + not_invers[nul]
                    nul -= 1
                win_test.append(int(invers, 2))
                text = ""
                if i != 32:
                    text = text + str(pacet[i])
                iterat = 1
        write_package(number_chip, 3, win_test[0], win_test[1], win_test[2], win_test[3], 0, 0, 0, 0, textbox)
        iterator_command = 0
        while True:
            time.sleep(0.5)
            say_black_box = ser.readlines()
            print(say_black_box)
            if iterator_command >= 10:
                iterator_command = 0
                write_package(number_chip, 3, win_test[0], win_test[1], win_test[2], win_test[3], 0, 0, 0, 0, textbox)
            if len(say_black_box) == 0:
                iterator_command += 1
            elif "OK" in str(say_black_box):
                break
            elif "ER" in str(say_black_box):
                print('Error coefficient K and B not write in chip ' + str(number_chip) + '\n')
                break
    except:
        print("Микросхема " + str(number_chip) + " не запрограмммировалась.")


# GET COEFFICIENTS K AND B
def get_k_and_b(x_list_in_file, y_list_in_file):
    x_1 = x_list_in_file[0]
    y_1 = y_list_in_file[0]
    x_2 = x_list_in_file[-1]
    y_2 = y_list_in_file[-1]
    k = float((y_1 - y_2)) / float((x_1 - x_2))
    b = y_2 - k * x_2
    return k, b


# LAST SQUARES OPTIMIZATION METHOD
def min_kv(x_list_interval, y_list_interval):
    summa_x = 0
    kv_sum_x = 0
    summa_y = 0
    sum_x_y_proizv = 0
    for i in range(len(x_list_interval)):
        summa_x = summa_x + x_list_interval[i]
        kv_sum_x = kv_sum_x + (x_list_interval[i] * x_list_interval[i])
        summa_y = summa_y + y_list_interval[i]
        sum_x_y_proizv = sum_x_y_proizv + (x_list_interval[i] * y_list_interval[i])
    delta = (kv_sum_x * len(x_list_interval)) - (summa_x * summa_x)
    delta_k = (sum_x_y_proizv * len(x_list_interval)) - (summa_y * summa_x)
    delta_b = (kv_sum_x * summa_y) - (sum_x_y_proizv * summa_x)

    coef_k = float(delta_k / delta)
    coef_b = float(delta_b / delta)

    return coef_k, coef_b


# get cubic interpolation coordinates [KOD temperature]
def interpol(xlist_test, ylist_test):
    tck = interpolate.splrep(xlist_test, ylist_test)
    temperature = xlist_test[0]
    stop_step = xlist_test[len(xlist_test) - 1]
    step = 0.01
    interval_y = []
    interval_x = []
    while temperature < stop_step:
        interval_x.append(round(temperature, 2))
        interval_y.append(interpolate.splev(temperature, tck))
        temperature = temperature + step
    return interval_x, interval_y


# READ FILE AND GET KOD TEMPERATURE
def readFile(number_chip):
    global path_in_data
    try:
        file_path_data = open(path_in_data + str(number_chip) + '.txt', 'r')
        say = []
        kod_list = []
        t_list = []
        for line in file_path_data:
            say = line.split(' ')
            if len(say) == 3:
                kod_list.append(float(say[0]))
                t_list.append(float(say[1]))
        file_path_data.close()
        return kod_list, t_list
    except:
        pass


'''
END BLOCK WRITE COEFFICIENTS
'''

'''
BLOCK READ OTP
'''


def give_me_OTP_address(port):
    global path_in_address_all_memory_otp_in_one_chip
    file_text = open(path_in_address_all_memory_otp_in_one_chip + str(port) + '.txt', 'w')
    file_text.close()
    command = 9
    for i in range(256):
        print('\n')
        print(i)
        bit_address = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
        bit_kod = str(bin(i))
        bit_kod = list(bit_kod[2:len(bit_kod)])
        iterator = len(bit_kod) + 2
        for k in bit_kod:
            bit_address[iterator] = k
            iterator -= 1
        byte = ""
        iterator = 0
        package = []
        for bit in bit_address:
            if iterator == 7:
                byte += str(bit)
                package.append(int(byte[::-1], 2))
                byte = ""
                iterator = 0
            else:
                byte += str(bit)
                iterator += 1
        time.sleep(0.1)
        write_package(port, command, package[0], package[1], 0, 0, 0, 0, 0, 0, textbox)
        iterator_break = 0
        flag_stop = True
        while flag_stop:
            time.sleep(0.1)
            all_lines = ser.readline()
            print(all_lines)
            if len(all_lines.split(" ")) == 2 or iterator_break == 20:
                break
            if iterator_break == 10:
                write_package(port, command, package[0], package[1], 0, 0, 0, 0, 0, 0, textbox)
            iterator_break += 1
        if iterator_break == 20:
            print("ERROR")
            break
        form_KOD(all_lines, int(i), port)


def form_KOD(all_lines, address, port):
    list = all_lines.split(" ")
    low = list[0]
    high = list[1]
    result_array = []
    for i in range(len(high) - 2):
        result_array.append(high[i])
    for i in range(len(low) - 2):
        result_array.append(low[i])
    kod = ""
    for i in range(4, len(high)):
        kod += str(high[i])
    print(int(kod, 2))
    write_File_All_ADDRESS_In_One_Chip(address, kod, port)


def write_File_All_ADDRESS_In_One_Chip(address, kod, port):
    global path_in_address_all_memory_otp_in_one_chip
    file_text = open(path_in_address_all_memory_otp_in_one_chip + str(port) + '.txt', 'a')
    file_text.write(str(address) + " | " + str(kod) + '\n')
    file_text.close()


'''
END BLOCK READ OTP
'''

'''
BLOCK CHECK OTP AND WRITE BITS
'''


def read_file_writer(number_chip):
    global path_in_address_all_memory_otp_in_one_chip_write
    file_path_data = open(path_in_address_all_memory_otp_in_one_chip_write + str(number_chip) + '.txt', 'r')
    text_in_file = []
    for line in file_path_data:
        text_in_file.append(line)
    file_path_data.close()
    return text_in_file


def read_file(number_chip):
    global path_in_address_all_memory_otp_in_one_chip
    file_path_data = open(path_in_address_all_memory_otp_in_one_chip + str(number_chip) + '.txt', 'r')
    text_in_file = []
    for line in file_path_data:
        text_in_file.append(line)
    file_path_data.close()
    return text_in_file


def main_check_OTP_memory(number_chip, flag_final_test):
    writer_file = read_file_writer(number_chip)
    data_file = read_file(number_chip)
    if len(writer_file) != len(data_file):
        print("ERROR")
        return
    for iterator_line in range(len(writer_file)):
        line_writer = writer_file[iterator_line].split(' | ')
        line_data = data_file[iterator_line].split(' | ')
        byte_data = str(line_data[1])
        byte_data = byte_data[:12]
        byte_writer = str(line_writer[1])
        byte_writer = byte_writer[11:23]
        byte_writer = byte_writer[::-1]
        value = ""
        address_memory = str(line_writer[0])
        for iterator in range(len(byte_writer)):
            if byte_writer[iterator] != byte_data[iterator]:
                value += byte_writer[iterator]
            else:
                value += "0"
        value_int = int(value, 2)
        flag_result = True
        if value_int != 0:
            if not flag_final_test:
                print(" Микросхема " + str(number_chip) + " ошибка записи ячейки памяти " + str(
                    int(address_memory)) + "\n")
                file_er = open('../data/file_error.txt', 'a')
                file_er.write(" Микросхема " + str(number_chip) + " ошибка записи ячейки памяти " + str(
                    int(address_memory)) + "\n")
                file_er.close()
                write_OTP(int(address_memory), int(value, 2), number_chip, False)
                time.sleep(0.5)
                flag_result = False
            else:
                file_er = open('../data/file_error.txt', 'a')
                file_er.write(" Микросхема " + str(number_chip) + " память ОТП записанна не корректно" + "\n")
                file_er.close()
                flag_result = False
        return flag_result


'''
END BLOCK CHECK OTP AND WRITE BITS
'''

'''
BLOCK WRITE OTP
'''


def calculation_ADDRESS_and_KOD(port):
    global path_in_address_all_memory_otp_in_one_chip_write
    try:
        x_list_in_file, y_list_in_file = readFile(port)
        all_x_in_interpol, all_y_in_interpol = interpol(x_list_in_file, y_list_in_file)
        # not TRUE
        k, b = get_k_and_b(x_list_in_file, y_list_in_file)
        # k, b = min_kv(all_x_in_interpol, all_y_in_interpol)
        k_line_kod = -16
        b_line_kod = 2047
        k_ideal, b_ideal = get_ideal_k_and_b()
        k_real = round(float(k_ideal / k), 4)
        b_real = -1 * ((k_ideal / k) * b) + b_ideal
        kod, address = form_array_in_read_file(all_x_in_interpol, all_y_in_interpol, x_list_in_file, y_list_in_file,
                                               k_real, b_real, k_line_kod, b_line_kod)
        kod, address = check_formed_array(kod, address)
        kod, address = check_formed_array_2(kod, address)
        iterator_array_kod_and_address = 0
        start_address = form_array_full_address_start_or_finish(address[0])
        finish_address = form_array_full_address_start_or_finish(address[-1])
        file_text = open(path_in_address_all_memory_otp_in_one_chip_write + str(port) + '.txt', 'w')
        file_text.close()
        iterator = 0
        while iterator <= 255:
            time.sleep(0.1)
            if iterator == 0:
                y_address = 0
                y_kod = 15
                write_OTP(int(y_address), int(y_kod), port, True)
            elif iterator < start_address:
                y_address = iterator
                y_kod = 15
                write_OTP(int(y_address), int(y_kod), port, True)
            elif iterator > finish_address:
                y_address = iterator
                y_kod = 3039
                write_OTP(int(y_address), int(y_kod), port, True)
            else:
                y_address = address[iterator_array_kod_and_address]
                y_kod = kod[iterator_array_kod_and_address] + 18
                # ~+16 #Ожидаемая ошибка средняя ошибка 5 кодов. Максимальное отклонение 7. Важно! Данный график находиться выше на ошибку. Необходимо прибавить к числу данную ошибку!
                if y_kod > 3039:
                    y_kod = 3039
                if y_kod < 15:
                    y_kod = 15
                write_OTP(int(y_address), int(y_kod), port, True)
                iterator_array_kod_and_address = iterator_array_kod_and_address + 1
            print("Chip = " + str(port) + " ADDRESS  = " + str(iterator) + " KOD = " + str(y_kod))
            iterator += 1
        for i in range(3):
            give_me_OTP_address(port)
            flag_chek_mem = main_check_OTP_memory(port, False)
            if flag_chek_mem:
                break

        give_me_OTP_address(port)
        check_number_file_otp_mem(port)
    except:
        print("Chip " + str(port) + " not work.")


def check_number_file_otp_mem(number_file):
    path_1 = 'C:/main_programs_micros/address/all_address_otp_in_one_chip_write_'
    path_2 = 'C:/main_programs_micros/address/all_address_otp_in_one_chip_'
    number_1 = form_file_write_1(path_1, number_file)
    number_2 = form_file_write_2(path_2, number_file)
    print(number_1)
    print(number_2)
    for i in range(len(number_1)):
        test = number_1[i]
        if int(test) != -999:
            if int(test[::-1], 2) != int(number_2[i], 2):
                print("Error line = " + str(i) + " in chip = " + str(number_file) + " DATA " + test[::-1] + " __ " +
                      number_2[i])
                file_er = open('../data/file_error.txt', 'a')
                file_er.write(
                    "Error line = " + str(i) + " in chip = " + str(number_file) + " DATA " + test[::-1] + " __ " +
                    number_2[i] + "\n")
                file_er.close()


def form_file_write_1(path, i):
    data_file_start = []
    try:
        f_start = open(path + str(i) + '.txt', 'r')
        for line in f_start:
            data_file_start.append(line[-14:-2])
    except:
        data_file_start.append('-999')

    return data_file_start


def form_file_write_2(path, i):
    data_file_start = []
    try:
        f_start = open(path + str(i) + '.txt', 'r')
        for line in f_start:
            if len(line) > 7:
                data_file_start.append(line[-13:len(line)])
    except:
        data_file_start.append('-999')

    return data_file_start


def form_array_in_read_file(x_list_interpol, y_list_interpol, x_list_in_file, y_list_in_file, k_real, b_real, k, b):
    kod_array = []
    address_array = []
    size = len(x_list_in_file)
    for i in range(size - 1, 0, -1):
        print(" start temperature = " + str(x_list_in_file[i]) + " finish temperature = " + str(x_list_in_file[i - 1]))
        start_address = give_me_address_in_255(y_list_in_file[i], k_real, b_real)
        finish_address = give_me_address_in_255(y_list_in_file[i - 1], k_real, b_real)
        minus = int(finish_address) - int(start_address)
        step_temperature = abs(round(((abs(x_list_in_file[i]) - abs(x_list_in_file[i - 1])) / minus), 2))
        temperature = x_list_in_file[i]
        kod_address = round(y_list_in_file[i], 0)
        for j in range(minus):
            kod = int(temperature * k + b)
            kod_array.append(kod)
            address = int(kod_address * k_real + b_real)
            bin_address = str(bin(address))
            test = bin_address[2:len(bin_address) - 1]
            address = int(test, 2)
            address_array.append(address)
            print(" kod = " + str(kod) + " address = " + str(address) + " temperature = " + str(
                temperature) + " step = " + str(step_temperature) + " kod_address = " + str(kod_address))
            temperature = round((temperature - step_temperature), 2)
            try:
                index_int = x_list_interpol.index(temperature)
                kod_address = round(y_list_interpol[index_int], 0)
            except:
                continue
    return kod_array, address_array


def give_me_address_in_255(kod, k_test, b_test):
    address_12_bit = kod * k_test + b_test
    print(address_12_bit)
    address_12_bit = str(bin(int(address_12_bit)))
    address_bit = list(address_12_bit[2:len(address_12_bit)])
    print(address_bit)
    if len(address_bit) > 8:
        for i in range(4):
            del address_bit[len(address_bit) - 1]
    address_255 = ""
    for i in address_bit:
        address_255 += str(i)
    address = int(address_255, 2)
    return address


def check_formed_array(kod, address):
    iterator = 0
    flag = True
    while True:
        if iterator > len(kod) - 2:
            break
        top_address = form_array_full_address_start_or_finish(address[iterator])
        bottom_address = form_array_full_address_start_or_finish(address[iterator + 1])
        if top_address == bottom_address:
            flag = False
            del kod[iterator + 1]
            del address[iterator + 1]
        iterator += 1
    if flag:
        kod, address = check_formed_array(kod, address)
    return kod, address


def check_formed_array_2(kod, address):
    iterator = 0
    while True:
        if iterator > len(kod) - 2:
            break
        top_address = form_array_full_address_start_or_finish(address[iterator])
        bottom_address = form_array_full_address_start_or_finish(address[iterator + 1])
        minus = bottom_address - top_address
        if minus > 1:
            step = (kod[iterator + 1] - kod[iterator]) / minus
            new_kod = kod[iterator]
            new_address = top_address
            for i in range(minus - 1):
                new_address += 1
                new_kod += step
                kod.insert(iterator + 1 + i, new_kod)
                address.insert(iterator + 1 + i, new_address << 3)
        iterator += 1
    return kod, address


def give_me_address_in_25_test(kod):
    address_12_bit = str(bin(int(kod)))
    address_bit = list(address_12_bit[2:len(address_12_bit)])
    if len(address_bit) > 8:
        for i in range(4):
            del address_bit[len(address_bit) - 1]
    address_255 = ""
    for i in address_bit:
        address_255 += str(i)
    address = int(address_255, 2)
    return address


# METHOD OF RECORDING THE COEFFICIENTS OF K AND B IN THE CHIP
def write_OTP(address, kod, port, textbox, flag_write_file):
    global path_in_address_all_memory_otp_in_one_chip_write
    if flag_write_file:
        file_text = open(path_in_address_all_memory_otp_in_one_chip_write + str(port) + '.txt', 'a')
    command = 8
    bit_address = str(bin(address))
    bit_address = list(bit_address[2:len(bit_address)])
    if len(bit_address) == 12:
        del bit_address[-1]
    bit_address = form_array_full_address(bit_address)
    bit_kod = str(bin(kod))
    bit_kod = list(bit_kod[2:len(bit_kod)])
    bin_code = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    iterator = 0
    for bit in bit_address:
        bin_code[iterator] = int(bit)
        iterator = iterator + 1
    iterator = len(bit_kod) + 10
    for bit in bit_kod:
        bin_code[iterator] = int(bit)
        iterator = iterator - 1
    print(bin_code)
    byte = ""
    iterator = 0
    package = []
    for bit in bin_code:
        if iterator == 7:
            byte += str(bit)
            package.append((int(byte[::-1], 2)))
            byte = ""
            iterator = 0
        else:
            byte += str(bit)
            iterator += 1
    print_bin_code = str(bin_code)[1:len(str(bin_code)) - 1].split(", ")
    if flag_write_file:
        file_text.write(str(address) + " | " + str(''.join(print_bin_code)) + "\n")
        file_text.close()
    write_package(port, command, package[0], package[1], package[2], 0, 0, 0, 0, 0, textbox)
    iterator_command = 0
    while True:
        # ~time.sleep(0.5)
        time.sleep(0.25)
        say_black_box = ser.readlines()
        print(say_black_box)
        if iterator_command >= 10:
            iterator_command = 0
            write_package(port, command, package[0], package[1], package[2], 0, 0, 0, 0, 0, textbox)
        if len(say_black_box) == 0:
            iterator_command += 1
        elif "OK" in str(say_black_box):
            break
        elif "ER" in str(say_black_box):
            print("ERROR OTP MAMMARY IN CHIP = " + str(port) + '\n')
            break


def form_array_full_address(bit_address):
    array_byte_address = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if len(bit_address) <= 8:
        iterator = 2 + len(bit_address)
    else:
        iterator = len(bit_address) - 1
    for i in bit_address:
        array_byte_address[iterator] = i
        iterator = iterator - 1
    # print(array_byte_address)
    test = ""
    bit_address = array_byte_address[::-1]
    for i in range(len(bit_address)):
        test = test + str(int(bit_address[i]))
    return array_byte_address


def form_array_full_address_start_or_finish(address):
    start_address = bin(address)
    start_address = list(start_address[2:len(start_address)])
    array_byte_address = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if len(start_address) <= 8:
        iterator = 2 + len(start_address)
    else:
        iterator = len(start_address) - 1
    for i in start_address:
        array_byte_address[iterator] = i
        iterator = iterator - 1
    # print(array_byte_address)
    test = ""
    bit_address = array_byte_address[::-1]
    for i in range(len(bit_address)):
        test = test + str(int(bit_address[i]))
    test = test[0:len(test) - 3]
    return int(test, 2)


'''
END BLOCK WRITE OTP
'''

'''
BLOCK WRITE MAIN ADDRESS
'''


# переделать записи в файл
# SET ADDRESS
def set_address(number_chip):
    global path_all_address

    number_family = get_number_series()
    type_of_party = get_number_part()

    number_family = int(number_family)
    full_ID = []
    if number_family == 1:
        bin_name = form_ADDRESS_SN(0)
        full_ID = write_CRC(0, type_of_party)
        # file_text = open(path_all_address + 'BMK_GEN.list', 'a')
        # file_text.write("40" + " " + str(int(type_of_party)) + " " + str(bin_name) + " " + str(full_ID) + "\n")
        # file_text.close()
    elif number_family == 2:
        bin_name = form_ADDRESS_SN(1)
        full_ID = write_CRC(1, type_of_party)
        # file_text = open(path_all_address + 'BMK_DIODE.list', 'a')
        # file_text.write("41" + " " + str(int(type_of_party)) + " " + str(bin_name) + " " + str(full_ID) + "\n")
        # file_text.close()
    elif number_family == 3:
        bin_name = form_ADDRESS_SN(2)
        full_ID = write_CRC(2, type_of_party)
        # file_text = open(path_all_address + 'CUSTOM_GEN.list', 'a')
        # file_text.write("6" + " " + str(int(type_of_party)) + " " + str(bin_name) + " " + str(full_ID) + "\n")
        # file_text.close()
    elif number_family == 4:
        bin_name = form_ADDRESS_SN(3)
        full_ID = write_CRC(3, type_of_party)
        # file_text = open(path_all_address + 'CUSTOM_DIODE.list', 'a')
        # file_text.write("7" + " " + str(int(type_of_party)) + " " + str(bin_name) + " " + str(full_ID) + "\n")
        # file_text.close()
    elif number_family == 5:
        bin_name = form_ADDRESS_SN(4)
        full_ID = write_CRC(4, type_of_party)
        # file_text = open(path_all_address + 'TEST_SAMPLE.list', 'a')
        # file_text.write(
        #     "173" + " " + type_of_party[:len(type_of_party) - 1] + " " + str(int(bin_name)) + " " + str(full_ID) + "\n")
        # file_text.close()
    else:
        print('Chip ' + str(number_chip) + ' incorrect value entered.')
    return full_ID


# WRITE IN FILE FULL ADDRESS
def form_ADDRESS_SN(series_chip):
    global path_all_address
    bin_name = 0
    name_file = ["BMK_GEN", "BMK_DIODE", "CUSTOM_GEN", "CUSTOM_DIODE", "TEST_SAMPLE"]
    file_text = open(path_all_address + name_file[series_chip] + '.list', 'r')
    all_lines = file_text.readlines()
    file_text.close()
    if len(all_lines) == 0:
        return bin_name
    else:
        last_line = all_lines[-1].split(" ")
        bin_name = int(last_line[2]) + 1
    return bin_name


# FORM CRC8 AND WRITE FULL ADDRESS IN CHIP
def write_CRC(number_file, type_of_party):
    global path_all_address
    crc = [0, 0, 0, 0, 0, 0, 0, 0]
    ishod = ""
    code = []
    # print(type_of_party)
    for i in range(56):
        code.append(0)
    name_file = ["BMK_GEN", "BMK_DIODE", "CUSTOM_GEN", "CUSTOM_DIODE", "TEST_SAMPLE"]
    collection_dec_code_in_file = [40, 41, 6, 7, 173]
    file_text = open(path_all_address + name_file[number_file] + '.list', 'r')
    all_lines = file_text.readlines()
    file_text.close()
    if len(all_lines) == 0:
        fam = list(bin(int(collection_dec_code_in_file[number_file])))
        sn = list(bin(int(0)))
        party = list(type_of_party)
    else:
        last_line = all_lines[-1].split(" ")
        fam = list(bin(int(collection_dec_code_in_file[number_file])))
        sn = list(bin(int(last_line[2]) + 1))
        party = list(type_of_party)
    pace_address_sir = ""
    number_bit = 7 + 2  # 0 and 1 bit ("0b") 7+2
    for i in range(2, len(fam)):
        code[number_bit - i] = int(fam[int(len(fam)) + 1 - i])
    number_bit = 11
    for i in range(4):
        code[number_bit - i] = int(party[3 - i])
    number_bit = 55 + 2
    for i in range(2, len(sn)):
        code[number_bit - i] = int(sn[int(len(sn)) + 1 - i])
    step_i = [7, 15, 23, 31, 39, 47, 55]
    for i in step_i:
        number_i = i
        for j in range(8):
            if crc[0] == code[number_i - j]:
                x = 0
            else:
                x = 1
            crc[0] = crc[1]
            crc[1] = crc[2]
            if crc[3] == x:
                crc[2] = 0
            else:
                crc[2] = 1
            if crc[4] == x:
                crc[3] = 0
            else:
                crc[3] = 1
            crc[4] = crc[5]
            crc[5] = crc[6]
            crc[6] = crc[7]
            crc[7] = x
    for i in crc:
        pace_address_sir = pace_address_sir + str(i)
        ishod = ishod + str(i)
    for i in range(56):
        pace_address_sir = pace_address_sir + str(code[55 - i])
    iterator = 0
    pace_list = list(pace_address_sir)
    pace = ""
    full_pace_chr = []
    col_pace_data = 0
    number_element_list = 62
    pace = pace + str(pace_list[63])
    while True:
        iterator = iterator + 1
        if iterator > 7:
            pace_address = int(pace, 2)
            full_pace_chr.append(pace_address)
            col_pace_data = col_pace_data + 1
            if col_pace_data == 8:
                break
            pace = ""
            iterator = 0
            pace = pace + str(pace_list[number_element_list])
            number_element_list = number_element_list - 1
        else:
            pace = pace + str(pace_list[number_element_list])
            number_element_list = number_element_list - 1
    return full_pace_chr


'''
END BLOCK WRITE MAIN ADDRESS
'''

'''
BLOCK ACCESSORY
'''


# GET LIST TEMPERATURE
def get_list_temperature():
    global path
    if os.path.exists(path):
        file_config = open(path, 'r')
        iterator = 0
        number_start_chip = []
        for line in file_config:
            if iterator == 9:
                number_start_chip = line
            iterator += 1
        file_config.close()
        temperature_list = [int(x) for x in number_start_chip.split(", ")]
        return temperature_list
    else:
        return 0


# GET NUMBER SOURCE
def get_number_source():
    global path
    if os.path.exists(path):
        file_config = open(path, 'r')
        iterator = 0
        number_start_chip = []
        for list in file_config:
            if iterator == 8:
                number_start_chip = int(list)
            iterator += 1
        file_config.close()
        return number_start_chip
    else:
        return 0


# GET THE CHECK CHIP RESPONSE FLAG 'OK'
def check_mess_microchip():
    global ser
    time.sleep(0.5)
    say_black_box = ser.readlines()
    print(say_black_box)
    if 'OK' in str(say_black_box):
        return True
    return False


# GET NUMBER PART
def get_number_part():
    global path
    if os.path.exists(path):
        file_config = open(path, 'r')
        iterator = 0
        for list in file_config:
            if iterator == 6:
                number_part = list
            iterator += 1
        file_config.close()
        return number_part
    else:
        return 0


# GET NUMBER SERIES
def get_number_series():
    global path
    if os.path.exists(path):
        file_config = open(path, 'r')
        iterator = 0
        for list in file_config:
            if iterator == 7:
                number_series = int(list)
            iterator += 1
        file_config.close()
        return number_series
    else:
        return 0


# GET NUMBER START CHIP
def get_number_start_chip():
    global path
    if os.path.exists(path):
        file_config = open(path, 'r')
        iterator = 0
        number_start_chip = []
        for list in file_config:
            if iterator == 1:
                number_start_chip = int(list)
            iterator += 1
        file_config.close()
        return number_start_chip
    else:
        return 0


# GET NUMBER FINISH CHIP
def get_number_finish_chip():
    global path
    if os.path.exists(path):
        file_config = open(path, 'r')
        iterator = 0
        for list in file_config:
            if iterator == 2:
                number_finish_chip = int(list)
            iterator += 1
        file_config.close()
        return number_finish_chip
    else:
        return 0


# GET NUMBER COM PORT MICROCHIP
def get_com_port_microchip1():
    if os.path.exists(path):
        file_config = open(path, 'r')
        iterator = 0
        for list in file_config:
            if iterator == 0:
                com_port_data = int(list)
            iterator += 1
        file_config.close()
        return com_port_data
    else:
        return 0


# GET NUMBER START MIT
def get_number_start_MIT():
    global path
    if os.path.exists(path):
        file_config = open(path, 'r')
        iterator = 0
        for list in file_config:
            if iterator == 4:
                number_start_MIT = int(list)
            iterator += 1
        file_config.close()
        return number_start_MIT
    else:
        return 0


# GET NUMBER FINISH MIT
def get_number_finish_MIT():
    global path
    if os.path.exists(path):
        file_config = open(path, 'r')
        iterator = 0
        for list in file_config:
            if iterator == 5:
                number_finish_MIT = int(list)
            iterator += 1
        file_config.close()
        return number_finish_MIT
    else:
        return 0


# GET NUMBER COM PORT MIT


# FORM AND GET IDEAL CORFFICIENT K AND B
def get_ideal_k_and_b():
    x_1 = -60
    y_1 = 3280
    x_2 = 125
    y_2 = 784
    k = float((y_1 - y_2)) / float((x_1 - x_2))
    b = y_2 - k * x_2
    return k, b


def new_file_main_address():
    global path_in_data
    f = open(path_in_data + 'address.txt', 'w')
    f.close()


def new_parth_temp():
    global path_in_data
    f = open(path_in_data + 'temperature.temp', 'w')
    f.close()


def write_temperature(array_temperature):
    global path_in_data
    f = open(path_in_data + 'temperature.temp', 'a')
    for temperature in array_temperature:
        f.write(str(temperature) + ' ')
    f.write('\n')
    f.close()


'''
END BLOCK ACCESSORY
'''

# GLOBAL VARIABLE
parameter = 0  # ON/OFF SOURCE MICROCHIP
path_in_address_all_memory_otp_in_one_chip = '../address/all_address_otp_in_one_chip_'
path_in_address_all_memory_otp_in_one_chip_write = '../address/all_address_otp_in_one_chip_write_'
path_in_data = '../data/'
path_all_address = '../listing_file/'
path_map_mit_ports = '../configuration/map_MIT_and_chip.txt'
time_sleep_MIT = 40  # SECOND STEP MIT
max_current = 0.4  # CURRENT
var = 0  # PARAMETER SOURCE
ser = 0  # SERIAL PORT
