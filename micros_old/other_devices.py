import time

import visa as visa


def read_current_yokogawa():
    return "0.254"


# REGOL
def read_current_regol():
    rm = visa.ResourceManager()
    lst = rm.list_resources('?*')
    my_instrument = rm.open_resource(lst[0])

    my_instrument.write(":MEAS:CURR?")
    current_variable = my_instrument.read()
    return float(current_variable)


def work_spec(temperature):
    rm = visa.ResourceManager()
    lst = rm.list_resources()
    print(lst)
    my_instrument = rm.open_resource(lst[0])
    my_instrument.write('01,MODE,CONSTANT')
    my_instrument.write('01,TEMP,S' + str(temperature))


# my_instrument.write('01,TEMP,S129')
def work_termostrim(temperature):
    rm = visa.ResourceManager()
    lst = rm.list_resources()
    print(lst)
    for name_connection_device in lst:
        match = re.findall('GPIB\d+::\d+::INSTR', name_connection_device)
        if match:
            break
    my_instrument = rm.open_resource(match[0])
    if temperature < 20:
        my_instrument.write('SETN 2')
    elif temperature < 35:
        my_instrument.write('SETN 1')
    else:
        my_instrument.write('SETN 0')
    time.sleep(5)
    commands = "SETP " + str(temperature)
    my_instrument.write(commands)
    time.sleep(5)


def block_check_current_chip(i):
    global max_current
    name_source = get_number_source()
    if "1" in str(name_source):
        current = read_current_yokogawa()
    elif "2" in str(name_source):
        current = read_current_regol()
    else:
        print("ERROR NOT WORK CONNECTION SOURCE!")
    if current >= max_current:
        print("ERROR current MAX limit " + str(i) + " " + '\n')
    return current
