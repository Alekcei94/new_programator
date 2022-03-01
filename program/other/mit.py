import time

import serial


# GET TEMPERATURE WITH MIT8
# transfer ['2:1.32012E+01B '] -> 13.20
def get_temperature_with_mit(lineBinary):
    number_full_name = str(lineBinary).split(':')
    number_all = number_full_name[1].split('B')
    number = number_all[0].split('E')
    temperature = float(number[0]) * (10 ** int(number[1]))
    print(number_full_name[0] + " Temperature = " + str(round(temperature, 2)))
    return round(temperature, 2)


def main_function_MIT(save_options):
    ser = serial.Serial('COM' + str(getattr(save_options, "com_port_mit")), 9600, timeout=0)
    ser.close()
    ser.open()
    ser.isOpen()
    flag = False
    list_port_mit = []
    for i in range(getattr(save_options, "first_mit"), getattr(save_options, "last_mit") + 1):
        list_port_mit.append(i)
    array_temperature = []
    iterator = list_port_mit[0]
    flag2 = False
    while True:
        line_binary = ser.readlines()
        time.sleep(1.5)
        if (len(line_binary) >= 1) and ('E' in str(line_binary)) and ('B ' in str(line_binary)):
            if (str(list_port_mit[0]) + ':') in str(line_binary) and not flag:
                array_temperature.append(get_temperature_with_mit(line_binary))
                flag = True
            if flag:
                if (str(list_port_mit[iterator]) + ':') in str(line_binary):
                    array_temperature.append(get_temperature_with_mit(line_binary))
                    iterator += 1
                    if iterator >= list_port_mit[len(list_port_mit) - 1]:
                        iterator = 0
                        print(array_temperature)
                        if flag2:
                            print("Finish point")
                            break
                        flag2 = True
                        array_temperature = []
    return array_temperature


def form_main_array(main_temperature, array_temperature):
    for i in range(len(main_temperature)):
        main_temperature[i] = array_temperature[i]
    return main_temperature


def check_MIT(main_temperature, array_temperature):
    for i in range(len(main_temperature)):
        if round(main_temperature[i], 1) != round(array_temperature[i], 1):
            return False
    return True


def form_array_list_port():
    file_text = open('../configuration/map_MIT_and_chip.txt', 'r')
    hash_map_number_chip_and_port_mit = {}
    for line in file_text:
        number_chip_and_number_port_mit = line.split(':')
        hash_map_number_chip_and_port_mit[int(number_chip_and_number_port_mit[0])] = int(
            number_chip_and_number_port_mit[1])
    file_text.close()
    list_port_mit = []
    for i in range(getattr(save_options, "first_mit"), getattr(save_options, "last_mit") + 1):
        list_port_mit.append(i)
    return list_port_mit


def get_temperature_in_chip_on_MIT(array_temperature, port):
    file = open('../configuration/map_MIT_and_chip.txt', 'r')
    for line in file:
        if int(line.split(':')[0]) == port:
            return int(line.split(':')[1]) - 1
    return 999