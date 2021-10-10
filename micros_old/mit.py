
# GET TEMPERATURE WITH MIT8
# transfer ['2:1.32012E+01B '] -> 13.20
def get_temperature_with_mit(lineBinary):
    number_full_name = str(lineBinary).split(':')
    number_all = number_full_name[1].split('B')
    number = number_all[0].split('E')
    temperature = float(number[0]) * (10 ** int(number[1]))
    print(number_full_name[0] + " Temperature = " + str(round(temperature, 2)))
    return round(temperature, 2)


# MAIN FUNCTION WORK MIT8
'''
def main_function_MIT(number_COM_port_MIT, list_port_mit):
    global time_sleep_MIT
    ser = serial.Serial('COM' + str(number_COM_port_MIT), 9600, timeout=0)
    ser.close()
    ser.open()
    ser.isOpen()
    flag = False
    main_temperature = []
    for i in range(len(list_port_mit)):
        main_temperature.append(0)
    array_temperature = []
    iterator = list_port_mit[0]
    flag2 = False
    while True:
        line_binary = ser.readlines()
        time.sleep(2)
        if (len(str(line_binary)) < 22) and (len(str(line_binary)) > 15) and ('E+' in str(line_binary)) and ('B ' in str(line_binary)):
            if (str(list_port_mit[0]) + ':') in str(line_binary) and not flag:
                array_temperature.append( get_temperature_with_mit( line_binary ) )
                print("start read MIT")
                flag = True
            if flag:
                if (str(list_port_mit[iterator]) + ':') in str(line_binary):
                    array_temperature.append(get_temperature_with_mit(line_binary))
                    #print(iterator)
                    #print(list_port_mit[len(list_port_mit)-1])
                    iterator += 1
                    if iterator >= list_port_mit[len(list_port_mit)-1]:
                        iterator = 0
                        print(main_temperature)
                        print(array_temperature)
                        if flag2:
                            print("Finish point")
                            break
                        if check_MIT(main_temperature, array_temperature):
                            time.sleep(750)
                            flag2 = True
                            array_temperature = []
                        else:
                            time.sleep(time_sleep_MIT)
                            main_temperature = form_main_array(main_temperature, array_temperature)
                            array_temperature = []

    return array_temperature
'''
'''
def main_function_MIT(number_COM_port_MIT, list_port_mit):
    global time_sleep_MIT
    ser = serial.Serial('COM' + str(number_COM_port_MIT), 9600, timeout=0)
    ser.close()
    ser.open()
    ser.isOpen()
    flag = False
    main_temperature = []
    for i in range(len(list_port_mit)):
        main_temperature.append(0)
    array_temperature = []
    iterator = list_port_mit[0]
    flag2 = False
    while True:
        line_binary = ser.readlines()
        time.sleep(2)
        if (len(str(line_binary)) < 22) and (len(str(line_binary)) > 15) and ('E+' in str(line_binary)) and ('B ' in str(line_binary)):
	        #print("start read MIT")
            if (str(list_port_mit[0]) + ':') in str(line_binary) and not flag:
                array_temperature.append( get_temperature_with_mit( line_binary ) )
                flag = True
            if flag:
                if (str(list_port_mit[iterator]) + ':') in str(line_binary):
                    array_temperature.append(get_temperature_with_mit(line_binary))
                    #print(iterator)
                    #print(list_port_mit[len(list_port_mit)-1])
                    iterator += 1
                    if iterator >= list_port_mit[len(list_port_mit)-1]:
                        iterator = 0
                        print(main_temperature)
                        print(array_temperature)
                        if flag2:
                            print("Finish point")
                            break
                        #for timer in range(4):
						#    now = datetime.datetime.now()
						#    print("Until temperature reading is left " + str((4-timer)*10) + " minutes. Current time - " + str(now.hour) + ":" + str(now.minute))
						#    time.sleep(600)
                        flag2 = True
                        array_temperature = []
    return array_temperature
'''


def main_function_MIT(number_COM_port_MIT, list_port_mit):
    global time_sleep_MIT
    ser = serial.Serial('COM' + str(number_COM_port_MIT), 9600, timeout=0)
    ser.close()
    ser.open()
    ser.isOpen()
    flag = False
    main_temperature = []
    for i in range(len(list_port_mit)):
        main_temperature.append(0)
    array_temperature = []
    iterator = list_port_mit[0]
    flag2 = False
    while True:
        line_binary = ser.readlines()
        time.sleep(1.5)
        # test_temp_MIT = str(line_binary)
        # print("DATA MIT " + str(line_binary))
        # print((len(line_binary) >= 1) and ('E' in str(line_binary)) and ('B ' in str(line_binary)))
        # print(int(temp_MIT[-4] + temp_MIT[-3]))
        # print(test_temp_MIT[test_temp_MIT.find("-")+1 : test_temp_MIT.find("B")])
        # ~if (len(str(line_binary)) < 22) and (len(str(line_binary)) > 15) and ('E' in str(line_binary)) and ('B ' in str(line_binary)):
        if (len(line_binary) >= 1) and ('E' in str(line_binary)) and ('B ' in str(line_binary)):

            # print("DATA MIT " + str(line_binary))
            if (str(list_port_mit[0]) + ':') in str(line_binary) and not flag:
                array_temperature.append(get_temperature_with_mit(line_binary))
                flag = True
            if flag:
                # print(int(line_binary[0].split(':')[0]))
                if (str(list_port_mit[iterator]) + ':') in str(line_binary):
                    array_temperature.append(get_temperature_with_mit(line_binary))
                    # print(iterator)
                    # print(list_port_mit[len(list_port_mit)-1])
                    iterator += 1
                    if iterator >= list_port_mit[len(list_port_mit) - 1]:
                        iterator = 0
                        print(main_temperature)
                        print(array_temperature)
                        if flag2:
                            print("Finish point")
                            break
                        # for timer in range(4):
                        #    now = datetime.datetime.now()
                        #    print("Until temperature reading is left " + str((4-timer)*10) + " minutes. Current time - " + str(now.hour) + ":" + str(now.minute))
                        #    time.sleep(600)
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
    global path_map_mit_ports
    file_text = open(path_map_mit_ports, 'r')
    hash_map_number_chip_and_port_mit = {}
    for line in file_text:
        number_chip_and_number_port_mit = line.split(':')
        hash_map_number_chip_and_port_mit[int(number_chip_and_number_port_mit[0])] = int(
            number_chip_and_number_port_mit[1])
    file_text.close()
    list_port_mit = []
    for i in range(get_number_start_MIT(), get_number_finish_MIT() + 1):
        # list_port_mit.append(hash_map_number_chip_and_port_mit.get(i))
        list_port_mit.append(i)
    return list_port_mit
