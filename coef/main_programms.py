# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
import os.path
import serial
import time
import pylab
import crc8
import numpy
import scipy
import visa
import datetime
import os
import shutil
import re
import matplotlib.pyplot as plt
from scipy import interpolate
from threading import Thread

'''
COMMANDS MICROCHIP
'''
# WRITE REZ AND ADDRESS
def write_rez_and_address(textbox):
	write_log('Команда записать рез и адрес ' + '\n', 0)
	write_rez(textbox)
	# give check rez
	time.sleep(5)
	write_address(textbox)
	# give check address

# USED VOLTAGE
def app_voltage(textbox, button_voltage):
	global parameter
	global ser
	write_log('Команда включить/отключить питание ' + '\n', 0)
	command_vdd = 1
	if parameter == 0:
		button_voltage.configure(bg='green')
		param_vdd = 1
		parameter = 1
	else:
		button_voltage.configure(bg='red')
		param_vdd = 0
		parameter = 0
	write_package(255, command_vdd, param_vdd, 0, 0, 0, 0, 0, 0, 0, textbox)
	if not check_mess_microchip():
		write_log('Неудалось выполнить команду включить/отклбчить питание ' + '\n', 1)
		textbox.insert(END, 'Error commands app voltage not used' + '\n')
		if parameter == 0:
			button_voltage.configure(bg='green')
			parameter = 1
		else:
			button_voltage.configure(bg='red')
			parameter = 0

# READ TEMPERATURE
def read_temperature(textbox):
	write_log('Команда считать температурный код ' + '\n', 0)
	time.sleep(0.5)
	form_temperature_in_all_chips(textbox)
	if not check_mess_microchip():
		return
	time.sleep(3)
	list_temperature = []
	for i in range(get_number_start_chip(), get_number_finish_chip() + 1):
		time.sleep(0.3)
		print(list_temperature)
		list_temperature.append(give_me_temperature_chip(textbox, i))
	write_log('Считывание температурного кода с микросхемы получен температырный код ' + str(list_temperature) + '\n', 1)
	return list_temperature

# READ MAIN ADDRESS CHIP
def read_address(textbox):
	global ser
	write_log('Команда считать основной адрес микросхем ' + '\n', 0)
	address_list = []
	command = 7
	for i in range(get_number_start_chip(), get_number_finish_chip() + 1):
		#write_package( i, command, 0, 0, 0, 0, 0, 0, 0, 0, textbox )
		for j in range(26):
			write_package( i, command, 0, 0, 0, 0, 0, 0, 0, 0, textbox )
			time.sleep( 0.5 )
			address = ser.readlines()
			print(address)
			if len(address) > 0:
				break
		if len(address) == 0:
			write_log('Считывание адреса с микросхемы номер ' + str(i) + ' неудалось ' +'\n', 1)
			address_list.append(str(i) + ':' + str(0))
			textbox.insert(END, "Chip " + str(i) + ' : ' + 'no address' + '\n')
		else:
			write_log('Считывание основного с микросхемы номер ' + str(i) + ' получили адрес '+ str(address) + '\n', 1)
			address_list.append(str(i) + ':' + str(address))
			textbox.insert(END, "Chip " + str(i) + ' : ' + str(address) + '\n')
	return address_list

# WRITE OTP MEMORY
def write_OTP_block(textbox):
	if check_click("Записать память ОТР?"):
		write_package( 255, 1, 0, 0, 0, 0, 0, 0, 0, 0, textbox )
		time.sleep(0.5)
		write_log('Команда записать память ОТП ' + '\n', 0)
		for i in range(get_number_start_chip(), get_number_finish_chip() + 1):
			#~write_package(i, 1, 1, 0, 0, 0, 0, 0, 0, 0, textbox)
			#~
			iter = 0
			while iter<25:
				
				write_package(i, 1, 1, 0, 0, 0, 0, 0, 0, 0, textbox)
				time.sleep(1)
				iter += 1
				if check_mess_microchip():
					#print("Up voltage chip " + str(i))
					break
			
			#~time.sleep(0.5)
			#~time.sleep(0.1)
			time.sleep(2)
			calculation_ADDRESS_and_KOD(i, textbox)
			#~
			iter = 0
			while iter<25:
				
				write_package( i, 1, 0, 0, 0, 0, 0, 0, 0, 0, textbox )
				time.sleep(1)
				iter += 1
				if check_mess_microchip():
					#print("Down voltage chip " + str(i))
					break
			#~write_package( i, 1, 0, 0, 0, 0, 0, 0, 0, 0, textbox )
			time.sleep(1)
		write_package(255, 1, 0, 0, 0, 0, 0, 0, 0, 0, textbox)
		
		
# READ OTP MEMORY
def read_OTP_block(textbox):
	write_log('Команда считать память ОТП ' + '\n', 0)
	for i in range(get_number_start_chip(), get_number_finish_chip() + 1):
		give_me_OTP_address(i, textbox)

# WRITE MAIN ADDRESS CHIP
def write_address(textbox):
	textbox.insert(END, "Start write ADDRESS.")
	if check_click("Записать основной адрес?"):
		write_log('Команда записать основной адрес ' + '\n', 0)
		for i in range(get_number_start_chip(), get_number_finish_chip() + 1):
			write_main_address(i, textbox)
		textbox.insert(END, "Finish write ADDRESS.")

# WRITE ENABLE 2
def write_en_2(textbox):
	if check_click("Записать бит enable_2 ?"):
		write_log('Команда записать бить enable_2 '+ '\n', 0)
		for i in range(get_number_start_chip(), get_number_finish_chip() + 1):
			write_log('Команда записать бить enable_2 в микросхеме номер ' + str(i) + '\n', 1)
			write_package(i, 10, 0, 0, 0, 0, 0, 0, 0, 0, textbox)
			if not check_mess_microchip():
				write_log('Команда записать бить enable_2 не прошла в микросхеме номер '+ str(i) +'\n', 1)
				textbox.insert(END, 'Error, not write enable 2 in chip ' + str(i) + '\n')

# WRITE REZ
def write_rez(textbox):
	textbox.insert(END, "Start write REZ.")
	if check_click("записать rez?"):
		write_log('Команда записать rez '+ '\n', 0)
		form_temperature_in_all_chips(textbox)
		if not check_mess_microchip():
			return
		time.sleep(3)
		for i in range(get_number_start_chip(), get_number_finish_chip() + 1):
			time.sleep(0.5)
			binary_cod = give_me_temperature_chip(textbox, i)
			print(binary_cod)
			if len(binary_cod) < 12:
				textbox.insert(END, 'Error length binary_cod < 12 in chip = ' + str(i) + '\n')
			else:
				write_main_rez(textbox, binary_cod, i)
				if not check_mess_microchip():
					textbox.insert(END, 'Error not write REZ in chip ' + str(i) + '\n')
				else:
					textbox.insert( END, 'Chip write REZ ' + str( i ) + ' OK' + '\n' )
		textbox.insert(END, "Finish write REZ.")

# WRITE COEFFICIENT CHIP K AND B
def write_coefficient_k_and_b(textbox):
	if check_click("Записать коэффициенты К и В"):
		for i in range(get_number_start_chip(), get_number_finish_chip() + 1):
			calculation_coefficients(i, textbox)

# FINALY TEST ALL CHIP
def finaly_test_all_chip(textbox):
    work_spec(129)
    time.sleep(1800)
    for i in range(125, -75, 10):
        for step_200 in range(200):
            list_temp = []
            list_temp = read_temperature(textbox)
            port = get_number_start_chip()
            for temp in list_temp:
                new_byte = (str(temp)[6:len(temp)-5]) 
                if len( new_byte ) == 0:
                    textbox.insert( END, 'Chip ' + str( number_chip ) + ' : ' + 'no temperature' + '\n' )
                    port += 1
                    continue
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
                    real_temperature = temperature * int(str_test, 2) * 0.0625
                file_text = open('../finaly_test/' + str(port) + '.txt', 'a')
                file_text.write(str(real_temperature) + '\n')
                port += 1
        work_spec(i)
        

# WRITE DATA IN FILE
'''
def read_temperature_and_write_data_file(textbox):
	global path_in_data
	path_temperature_file = "C:/main_programs_micros/data/temperature.txt"
	#for i in range(8):
	if check_click("Начать измерения?"):
		temperature_list = get_list_temperature()
		for i in range(len(temperature_list)):
			work_termostrim(i, temperature_list)
			array_temperature = main_function_MIT(get_com_port_MIT(), form_array_list_port())
			list_line_binary = read_temperature(textbox)
			#if len(list_line_binary) == 0:
			#    list_line_binary = read_temperature(textbox)
			port = get_number_start_chip()
			iterator = 0
			while True:
				time.sleep(0.5)
				flag_read = True
				for elem in list_line_binary:
					if len( elem ) == 0:
						print("Double start read temperature")
						flag_read = False
						list_line_binary = read_temperature( textbox )
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
					#list_elem = list(elem)
					#for i in range(4, len(elem)):
					#    real_temperature_12_bit += str(list_elem[i])
					file_text = open(path_in_data + str(port) + '.txt', 'a')
					file_text.write(str(get_mid_number_array_temperature(array_temperature)) + " " + str(int(real_temperature_12_bit, 2)) + " " + str(elem) + '\n')
					file_text.close()
					port += 1
					iterator += 1
				except:
					port += 1
					iterator += 1
'''
def read_temperature_and_write_data_file(textbox):
	global path_in_data
	#for i in range(8):
	if check_click("Начать измерения?"):
		temperature_list = get_list_temperature()
		for i in range(len(temperature_list)):
			#work_termostrim(temperature_list[i])
			print("PAUSE.")
			raw_input()
			array_temperature = main_function_MIT(get_com_port_MIT(), form_array_list_port())
			list_line_binary = read_temperature(textbox)
			#if len(list_line_binary) == 0:
			#    list_line_binary = read_temperature(textbox)
			port = get_number_start_chip()
			iterator = 0
			while True:
				time.sleep(0.5)
				flag_read = True
				for elem in list_line_binary:
					if len( elem ) == 0:
						print("Double start read temperature")
						flag_read = False
						list_line_binary = read_temperature( textbox )
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
					#list_elem = list(elem)
					#for i in range(4, len(elem)):
					#    real_temperature_12_bit += str(list_elem[i])
					file_text = open(path_in_data + str(port) + '.txt', 'a')
					file_text.write(str(get_mid_number_array_temperature(array_temperature)) + " " + str(int(real_temperature_12_bit, 2)) + " " + str(elem) + '\n')
					file_text.close()
					port += 1
					iterator += 1
				except:
					port += 1
					iterator += 1
		work_termostrim(25)

def get_mid_number_array_temperature(array_temperature):
    sum = 0
    size = len(array_temperature)-1
    for i in range(len(array_temperature) - 1):
        sum += array_temperature[i]
    itog = sum/size
    itog = round(itog, 2)
    return itog
	
def work_new_parth():
	if check_click("Загрузили новую партию микросхем?"):
		new_parth_logger(0)
		new_parth_logger(1)
		new_file_main_address()
		new_parth_temp()
	
'''
END COMMANDS MICROCHIP
'''
'''
FORM ADDRESS FILE
'''

def form_address_file(textbox):
	if check_click("Запистаь все адреса микросхем в файл?" + "\n" + "ВАЖНО. Данная функция необходима только при работе с новой партией."):
		str = read_address(textbox)
		f = open('./address.txt', 'w')
		for i in str:
			f.write(i)
		f.close

def check_address(textbox):
	str = read_address(textbox)
	str_check = []
	f = open('./address.txt', 'r')
	for i in f:
		str_check.append(i)
		
	for i in range(len(str)):
		if str[i] != str_check[i] :
			print(str[i] + " --> " + str_check[i])
'''
END FORM ADDRESS FILE
'''

'''
TEST BLOCK 
'''
'''
def give_real_temperature(number_chip, textbox):
	global ser
	command = 2
	parameters = 0  # ? OR 2
	write_package(number_chip, command, parameters, 0, 0, 0, 0, 0, 0, 0, textbox )
	str_bit_in_chip = ""
	iterator_commands = 0
	for i in range( 25 ):
		if iterator_commands == 10:
			write_package( number_chip, command, parameters, 0, 0, 0, 0, 0, 0, 0 )
		time.sleep( 0.5 )
		bit_in_chip = ser.readlines()
		#print(bit_in_chip)
		if len( bit_in_chip ) > 0:
			#str_bit_in_chip = str( bit_in_chip )[2:len( str( bit_in_chip ) ) - 4]
			break
		iterator_commands += 1
	new_bit = (str(bit_in_chip)[6:len(bit_in_chip)-5])
	if len( bit_in_chip ) == 0:
		print('Chip ' + str( number_chip ) + ' : ' + 'no temperature' + '\n' )
		return 0
	temperature = 1
	if new_bit[0] == '1':
		temperature = -1
		test = []
		for iter_bit in range(1, len(new_bit)):
			if new_bit[iter_bit] == "1":
				test.append('0')
			else:
				test.append('1')
		str_test = "".join(test)
		return temperature * int( str_test, 2 ) * 0.0625
	textbox.insert( END, 'Chip ' + str( number_chip ) + ' : ' + str( temperature * int(new_bit, 2) * 0.0625) + '\n' )
	print(temperature * int(new_bit, 2) * 0.0625)
	return temperature * int(new_bit, 2) * 0.0625
'''
	
def check_real_temperature(textbox):
    form_temperature_in_all_chips( textbox )
    if not check_mess_microchip():
        return
    time.sleep( 3 )
    for i in range( get_number_start_chip(), get_number_finish_chip() + 1 ):
        time.sleep( 0.3 )
        try:
            give_real_temperature(i, textbox)
        except:
            print('chip ' + str(i) + ' no worck')

def give_real_temperature(number_chip, textbox):
	global ser
	command = 2
	parameters = 0  # ? OR 2
	bin_list = []  # number chip:bin code
	write_package( number_chip, command, parameters, 0, 0, 0, 0, 0, 0, 0, textbox )
	str_bit_in_chip = ""
	for i in range( 25 ):
		time.sleep( 0.5 )
		bit_in_chip = ser.readlines()
		print(str( bit_in_chip ))
		if len( bit_in_chip ) > 0:
			str_bit_in_chip = str( bit_in_chip )[2:len( str( bit_in_chip ) ) - 4]
			break
	new_byte = (str(bit_in_chip)[6:len(bit_in_chip)-5]) 
	if len( new_byte ) == 0:
		textbox.insert( END, 'Chip ' + str( number_chip ) + ' : ' + 'no temperature' + '\n' )
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
		print( temperature * int( str_test, 2 ) * 0.0625)
		textbox.insert( END, 'Chip ' + str( number_chip ) + ' : ' + str( temperature * int( str_test, 2 ) * 0.0625 ) + '\n' )
	else:
		print(temperature * int(new_byte, 2) * 0.0625)
		textbox.insert( END, 'Chip ' + str( number_chip ) + ' : ' + str( temperature * int(new_byte, 2) * 0.0625 ) + '\n' )
	

'''
BLOCK VERIFICATION WORK CHIPS
'''
# VERIFICATION CHIPS
def verification_chips(textbox):
    global max_current
    write_package( 255, 1, 0, 0, 0, 0, 0, 0, 0, 0, textbox )
    time.sleep(0.5)
    for i in range(get_number_start_chip(), get_number_finish_chip() + 1):
        #print (i)
        write_package(i, 1, 1, 0, 0, 0, 0, 0, 0, 0, textbox)
        time.sleep(0.5)
        current = block_check_current_chip(i, textbox)
        if current >= max_current:
            continue
        textbox.insert(END, "Current chip " + str(i) + " = " + str(current) + '\n')
        current_array = []
        thread_current = Thread(target=form_temperature_in_all_chips, args=(textbox,))
        for j in range(16):
            if j == 4:
                thread_current.start()
            current_array.append(block_check_current_chip(i, textbox))
            time.sleep(0.2)
        thread_current.join()
        print(current_array)
        if max(current_array) >= max_current:
            textbox.insert(END, "ERROR current chip " + str(i) + " = " + current)
        write_package( i, 1, 0, 0, 0, 0, 0, 0, 0, 0, textbox )
        time.sleep(0.5)
    write_package(255, 1, 0, 0, 0, 0, 0, 0, 0, 0, textbox)

def block_check_current_chip(i, textbox):
    global max_current
    name_source = get_number_source()
    #print(name_source)
    if "1" in str(name_source):
        current = read_current_yokogawa()
    elif "2" in str(name_source):
        current = read_current_regol()
    else:
        textbox.insert(END, "ERROR NOT WORK CONNECTION SOURCE!")
    if current >= max_current:
        textbox.insert(END, "ERROR current MAX limit " + str(i) + " " + '\n')
    return current

'''
END BLOCK VERIFICATION WORK CHIPS 
'''


'''
BLOCK SOURCE
'''
# YOKOGAWA
def read_current_yokogawa():
    print(var)
    return "0.254"

# REGOL
def read_current_regol():
    rm = visa.ResourceManager()
    lst = rm.list_resources( '?*' )
    #print(lst)
    my_instrument = rm.open_resource( lst[0] )
    #print(my_instrument)

    my_instrument.write(":MEAS:CURR?")
    current_variable = my_instrument.read()
    #print(str(current_variable))
    return float(current_variable)

'''
END BLOCK SOURCE
'''

'''
BLOCK TERMOSTRIM
'''
def work_spec(temperature):		
    rm = visa.ResourceManager()
    lst = rm.list_resources()
    print(lst)
    my_instrument = rm.open_resource(lst[0])
    my_instrument.write('01,MODE,CONSTANT')
    my_instrument.write('01,TEMP,S'+ str(temperature))
    
def work_termostrim(temperature):
    rm = visa.ResourceManager()
    lst = rm.list_resources()
    print(lst)
    for name_connection_device in lst:
	    match = re.findall('GPIB\d+::\d+::INSTR', name_connection_device) 
	    if match:
		    break
    #my_instrument = rm.open_resource(lst[12])
    my_instrument = rm.open_resource(match[0])
    #array_temperature = [-62, -32, -7, 20, 41, 62, 92, 127]
    #array_temperature = [41, 61, 91, 126]
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

'''
BLOCK WRITE REZ
'''
# WRITE REZ
def write_main_rez(textbox, binary_cod, number_chip):
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
            print(str(28-i))
            try:
                data_1 = switch_case[28-i]
                print(data_1)
                write_package(number_chip, 5, data_1, 0, 0, 0, 0, 0, 0, 0, textbox)
                break
            except:
                textbox.insert(END, 'Error REZ not True in chip ' + str(number_chip) + '\n')

'''
END BLOCK WRITE REZ
'''

'''
BLOCK SAVE ARCHIVE
'''

def main_save_archive():
	if check_click("Сохранить все данные в архив и удалить файлы в текущих папках?"):
		now = datetime.datetime.now()
		form_path = str(now.day) + "_" + str(now.month) + "_" + str(now.year)
		try:
			os.mkdir("../archive/" + form_path)
		except:
			print ("Создать директорию не удалось")
		path_data_archive = "../archive/" + form_path + "/data/"
		path_address_archive = "../archive/" + form_path + "/address/"
		try:
			os.mkdir(path_data_archive)
			os.mkdir(path_address_archive)
		except:
			print ("Создать директорию не удалось")

		list_file_data = os.listdir("../data/")
		for i in list_file_data:
			shutil.copyfile("../data/" + i, path_data_archive + i)
			os.remove("../data/" + i)
		list_file_address = os.listdir("../address/")
		for i in list_file_address:
			shutil.copyfile("../address/" + i, path_address_archive + i)
			os.remove("../address/" + i)
'''
END BLOCK SAVE ARCHIVE
'''

'''
BLOCK WRITE COEFFICIENTS
'''
# MAIN COEFFICIENT CALCULATION METHOD
def calculation_coefficients(number_chip, textbox):
    x_list_in_file, y_list_in_file = readFile(str(number_chip))

    #~all_x_in_interpol, all_y_in_interpol = interpol(x_list_in_file, y_list_in_file)
    k, b = get_k_and_b(x_list_in_file, y_list_in_file)
    #k, b = min_kv(all_x_in_interpol, all_y_in_interpol)

    k_ideal, b_ideal = get_ideal_k_and_b()
    k_real = round(float(k_ideal / k), 4)
    b_real = round((-1 * ((k_ideal / k) * b) + b_ideal), 0)

    write_coefficient(k_real, b_real, number_chip, textbox)

# METHOD OF RECORDING THE COEFFICIENTS OF K AND B IN CHIP
def write_coefficient(coefK, coefB, number_chip, textbox):
    textbox.insert(END, 'Chip = ' + str(number_chip) + ' coefK = ' + str(coefK) + ' coefB = ' + str(coefB) + '\n')
    print('Chip = ' + str(number_chip) + ' coefK = ' + str(coefK) + ' coefB = ' + str(coefB) + '\n')
    bin_code_coef_b = []
    bin_code_corf_k = []
    # for ele in coefB:
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
    print ("b = " + coef_b_text)

    # for ele in coefK:
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
    print ("k = " + coefk_k)

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
        time.sleep( 0.5 )
        say_black_box = ser.readlines()
        print(say_black_box)
        if iterator_command >= 10:
            iterator_command = 0
            write_package(number_chip, 3, win_test[0], win_test[1], win_test[2], win_test[3], 0, 0, 0, 0, textbox)
        if len( say_black_box ) == 0:
            iterator_command += 1
        elif "OK" in str( say_black_box ):
            break
        elif "ER" in str( say_black_box ):
            textbox.insert( END, 'Error coefficient K and B not write in chip ' + str( number_chip ) + '\n' )
            break


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
    kv_summ_x = 0
    summa_y = 0
    summ_x_y_proizv = 0
    for i in range(len(x_list_interval)):
        summa_x = summa_x + x_list_interval[i]
        kv_summ_x = kv_summ_x + (x_list_interval[i] * x_list_interval[i])
        summa_y = summa_y + y_list_interval[i]
        summ_x_y_proizv = summ_x_y_proizv + (x_list_interval[i] * y_list_interval[i])
    delta = (kv_summ_x * len(x_list_interval)) - (summa_x * summa_x)
    delta_k = (summ_x_y_proizv * len(x_list_interval)) - (summa_y * summa_x)
    delta_b = (kv_summ_x * summa_y) - (summ_x_y_proizv * summa_x)

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

# BUILD GRAPH
def build_graph(xlist_test1, ylist_test1):
    test_array = []
    for i in range(len(xlist_test1)):
        test_array.append(i)
    plt.axis([-10, 160, -10000, 10000])
    print(xlist_test1)
    print(test_array)
    print(ylist_test1)
    plt.plot(test_array, xlist_test1, color='red')
    plt.plot(test_array, ylist_test1, color='blue')
    plt.show()

'''
END BLOCK WRITE COEFFICIENTS
'''


'''
BLOCK READ OTP
'''
def give_me_OTP_address(port, textbox):
    global path_in_address_all_memory_otp_in_one_chip
    file_text = open(path_in_address_all_memory_otp_in_one_chip + str(port) + '.txt', 'w')
    file_text.close()
    command = 9
    for i in range(256):
        #time.sleep(0.8)
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
        #print(package)
        time.sleep(0.1)
        write_package(port, command, package[0], package[1], 0, 0, 0, 0, 0, 0, textbox)
        iterator_break = 0
        flag_stop = True
        while flag_stop:
            time.sleep(0.2)
            all_lines = ser.readline()
            print(all_lines)
            if len(all_lines.split(" ")) == 2 or iterator_break == 20:
                break
            if iterator_break == 10:
                write_package( port, command, package[0], package[1], 0, 0, 0, 0, 0, 0, textbox )
            iterator_break += 1
        if iterator_break == 20:
            print("ERROR")
            break
        form_KOD(all_lines, int(i), port)

def form_KOD(all_lines, address, port):
    list = all_lines.split(" ")
    low = list[0]
    high = list[1]
    #print(low)
    #print(high)
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

def write_File_All_ADDRESS_In_One_Chip (address, kod, port):
    global path_in_address_all_memory_otp_in_one_chip
    file_text = open( path_in_address_all_memory_otp_in_one_chip + str( port ) + '.txt', 'a' )
    # for i in range(acc.get_start_arduino_port(), acc.get_finish_arduino_port()+1):
    file_text.write( str( address ) + " | " + str( kod ) + '\n')
    file_text.close()

'''
END BLOCK READ OTP
'''

'''
BLOCK CHECK OTP AND WRITE BITS
'''
def read_file_writer(number_chip):
    global path_in_address_all_memory_otp_in_one_chip_write
    file_path_data = open(path_in_address_all_memory_otp_in_one_chip_write + str(number_chip) + '.txt', 'r' )
    text_in_file = []
    for line in file_path_data:
        text_in_file.append(line)
    file_path_data.close()
    return text_in_file

def read_file(number_chip):
    global path_in_address_all_memory_otp_in_one_chip
    file_path_data = open(path_in_address_all_memory_otp_in_one_chip + str(number_chip) + '.txt', 'r' )
    text_in_file = []
    for line in file_path_data:
        text_in_file.append(line)
    file_path_data.close()
    return text_in_file

def main_check_OTP_memory(number_chip, textbox):
    writer_file = read_file_writer(number_chip)
    data_file = read_file(number_chip)
    #print(len(writer_file))
    #print(len(data_file))
    if len(writer_file) != len(data_file):
        print("ERROR")
        return
    for iterator_line in range(len(writer_file)):
        line_writer = writer_file[iterator_line].split(' | ')
        line_data = data_file[iterator_line].split(' | ')
        byte_data = str(line_data[1])
        byte_data = byte_data[:12]
        #print(byte_data)
        byte_writer = str(line_writer[1])
        byte_writer = byte_writer[11:23]
        byte_writer = byte_writer[::-1]
        #print(byte_writer)
        value = ""
        address_memory = str(line_writer[0])
        for iterator in range(len(byte_writer)):
            if byte_writer[iterator] != byte_data[iterator]:
                value += byte_writer[iterator]
            else:
                value += "0"
        value_int = int( value, 2 )
        if value_int != 0:
            write_log(" Микросхема " + str(number_chip) + " память ОТП записанна не корректно ", 1)
            return
            #print(" ADDRESS = " + str(int(address_memory)) + " __ " + str(int(value_int)))
            #time.sleep(1)
            #write_OTP(int(address_memory), int(value, 2), number_chip, textbox, False)

'''
END BLOCK CHECK OTP AND WRITE BITS
'''


'''
BLOCK WRITE OTP
'''
def calculation_ADDRESS_and_KOD (port, textbox):
    global path_in_address_all_memory_otp_in_one_chip_write
    x_list_in_file, y_list_in_file = readFile(port)
    all_x_in_interpol, all_y_in_interpol = interpol(x_list_in_file, y_list_in_file)
    #print("TEST-->")
    #print(all_x_in_interpol)
    #print(all_y_in_interpol)
    #print("<--")
    # not TRUE
    k, b = get_k_and_b(x_list_in_file, y_list_in_file)
    #k, b = min_kv(all_x_in_interpol, all_y_in_interpol)
    k_line_kod = -16
    b_line_kod = 2047
    k_ideal, b_ideal = get_ideal_k_and_b()
    k_real = round(float(k_ideal / k), 4)
    b_real = -1 * ((k_ideal / k) * b) + b_ideal
    iterator = 0
    # address = []
    kod, address = form_array_in_read_file(all_x_in_interpol, all_y_in_interpol, x_list_in_file, y_list_in_file, k_real,
                                           b_real, k_line_kod, b_line_kod)
    kod, address = check_formed_array(kod, address)
    kod, address = check_formed_array_2(kod, address)
    iterator_array_kod_and_address = 0
    start_address = form_array_full_address_start_or_finish(address[0])
    finish_address = form_array_full_address_start_or_finish(address[-1])

    file_text = open( path_in_address_all_memory_otp_in_one_chip_write + str( port ) + '.txt', 'w')
    file_text.close()
    while iterator <= 255:
        #print("ADDRESS = " + str(iterator))
        #~time.sleep(0.3)
        time.sleep(0.1)
        # print(" Write address in " + str(iterator) + " line")
        if iterator == 0:
            y_address = 0
            y_kod = 15
            # print(str(form_array_full_address_start_or_finish(y_address)) + " __ " + str(int(y_kod)))
            #print(str(y_address) + " __ " + str(int(y_kod)))
            write_OTP(int(y_address), int(y_kod), port, textbox, True)
        elif iterator < start_address:
            y_address = iterator
            y_kod = 15
            # print(str(form_array_full_address_start_or_finish(y_address)) + " __ " + str(int(y_kod)))
            #print(str(y_address) + " __ " + str(int(y_kod)))
            write_OTP(int(y_address), int(y_kod), port, textbox, True)
        elif iterator > finish_address:
            y_address = iterator
            y_kod = 3039
            # print(str(form_array_full_address_start_or_finish(y_address)) + " __ " + str(int(y_kod)))
            #print(str(y_address) + " __ " + str(int(y_kod)))
            write_OTP(int(y_address), int(y_kod), port, textbox, True)
        else:
            y_address = address[iterator_array_kod_and_address]
            y_kod = kod[iterator_array_kod_and_address]+18#~+16 #Ожидаемая ошибка средняя ошибка 5 кодов. Максимальное отклонение 7. Важно! Данный график находиться выше на ошибку. Необходимо прибавить к числу данную ошибку!
            if y_kod > 3039:
                y_kod = 3039
            if y_kod < 15:
                y_kod = 15
            # print(str(form_array_full_address_start_or_finish(y_address)) + " __ " + str(int(y_kod)))
            #print(str(y_address) + " __ " + str(int(y_kod)))
            write_OTP(int(y_address), int(y_kod), port, textbox, True)
            iterator_array_kod_and_address = iterator_array_kod_and_address + 1
        print(" ADDRESS  = " + str(iterator) + " KOD = " + str(y_kod))
        textbox.insert(END, 'Chip ' + str(port) + ', address = ' + str(y_address) + ' : ' + 'KOD = ' + str(y_kod))
        iterator += 1	
    #give_me_OTP_address(port, textbox )
    #main_check_OTP_memory(port, textbox)

def form_array_in_read_file(x_list_interpol, y_list_interpol, x_list_in_file, y_list_in_file, k_real, b_real, k, b):
    kod_array = []
    address_array = []
    size = len(x_list_in_file)
    for i in range(size - 1, 0, -1):
        print(" start temperature = " + str(x_list_in_file[i]) + " finish temperature = " + str(x_list_in_file[i-1]))
        start_address = give_me_address_in_255(y_list_in_file[i], k_real, b_real)
        finish_address = give_me_address_in_255(y_list_in_file[i - 1], k_real, b_real)
        # print(" finish = " + str(finish_address) + " start = " + str(start_address))
        minus = int(finish_address) - int(start_address)
        step_temperature = abs(round(((abs(x_list_in_file[i]) - abs(x_list_in_file[i - 1])) / minus), 2))
        # print(" step temperature = " + str(step_temperature))
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
        # razn = len(address_bit) - 8
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
		#print(str(top_address) + " !!! " + str(bottom_address))
		if top_address == bottom_address:
			flag = False
			del kod[iterator + 1]
			del address[iterator + 1]
		iterator += 1
	if (flag == False):
		kod, address = check_formed_array(kod, address)
	return kod, address

def check_formed_array_2(kod, address):
    iterator = 0
    while True:
        if iterator > len(kod) - 2:
            break
        top_address = form_array_full_address_start_or_finish(address[iterator])
        bottom_address = form_array_full_address_start_or_finish(address[iterator + 1])
        #print(str(top_address) + " !!! " + str(bottom_address))
        minus = bottom_address - top_address
        if minus > 1:
            step = (kod[iterator + 1] - kod[iterator]) / minus
            #print(kod[iterator + 1])
            #print(kod[iterator])
            new_kod = kod[iterator]
            new_address = top_address
            for i in range(minus - 1):
                new_address += 1
                new_kod += step
                #print(str(new_address) + " _#_ " + str(new_kod))
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
    if flag_write_file == True:
        file_text = open( path_in_address_all_memory_otp_in_one_chip_write + str( port ) + '.txt', 'a')
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
    #print(package[0])
    #print(package[1])
    #print(package[2])
    print_bin_code = str(bin_code)[1:len(str(bin_code))-1].split(", ")
    if flag_write_file == True:
        file_text.write(str(address) + " | " + str(''.join(print_bin_code)) + "\n")
        file_text.close()
    write_package(port, command, package[0], package[1], package[2], 0, 0, 0, 0, 0, textbox)
    iterator_command = 0
    while True:
        #~time.sleep(0.5)
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
            textbox.insert(END, "ERROR OTP MAMMARY IN CHIP = " + str(port) + '\n')
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

def write_main_address(port, textbox):
    number_family = get_number_series()
    type_of_party = get_number_part()
    set_address(number_family, type_of_party, textbox, port)

# SET ADDRESS
def set_address(number_family, type_of_party, textbox, number_chip):
    global path_all_address
    number_family = int(number_family)
    if number_family == 1:
        bin_name = form_ADDRESS_SN(0)
        crc1 = write_CRC(0, type_of_party, textbox, number_chip)
        file_text = open(path_all_address + 'BMK_GEN.list', 'a')
        file_text.write("40" + " " + str(int(type_of_party)) + " " + str(bin_name) + " " + str(crc1) + "\n")
        file_text.close()
    elif number_family == 2:
        bin_name = form_ADDRESS_SN(1)
        crc1 = write_CRC(1, type_of_party, textbox, number_chip)
        file_text = open(path_all_address + 'BMK_DIODE.list', 'a')
        file_text.write("41" + " " + str(int(type_of_party)) + " " + str(bin_name) + " " + str(crc1) + "\n")
        file_text.close()
    elif number_family == 3:
        bin_name = form_ADDRESS_SN(2)
        crc1 = write_CRC(2, type_of_party, textbox, number_chip)
        file_text = open(path_all_address + 'CUSTOM_GEN.list', 'a')
        file_text.write("6" + " " + str(int(type_of_party)) + " " + str(bin_name) + " " + str(crc1) + "\n")
        file_text.close()
    elif number_family == 4:
        bin_name = form_ADDRESS_SN(3)
        crc1 = write_CRC(3, type_of_party, textbox, number_chip)
        file_text = open(path_all_address + 'CUSTOM_DIODE.list', 'a')
        file_text.write("7" + " " + str(int(type_of_party)) + " " + str(bin_name) + " " + str(crc1) + "\n")
        file_text.close()
    elif number_family == 5:
        bin_name = form_ADDRESS_SN(4)
        crc1 = write_CRC(4, type_of_party, textbox, number_chip)
        file_text = open(path_all_address + 'TEST_SAMPLE.list', 'a')
        file_text.write("173" + " " + type_of_party[:len(type_of_party)-1] + " " + str(int(bin_name)) + " " + str(crc1) + "\n")
        file_text.close()
    elif number_family == 6:
        return
    else:
        textbox.insert(END, 'Chip ' + str(number_chip) + ' incorrect value entered.')

# WRITE IN FILE FULL ADDRESS
def form_ADDRESS_SN(series_chip):
    global path_all_address
    bin_name = 0
    name_file = ["BMK_GEN", "BMK_DIODE", "CUSTOM_GEN", "CUSTOM_DIODE", "TEST_SAMPLE"]
    file_text = open(path_all_address + name_file[series_chip]+'.list', 'r')
    all_lines = file_text.readlines()
    file_text.close()
    if len(all_lines) == 0:
        return bin_name
    else:
        last_line = all_lines[-1].split(" ")
        bin_name = int(last_line[2])+1
    return bin_name

# FORM CRC8 AND WRITE FULL ADDRESS IN CHIP
def write_CRC(number_file, type_of_party, textbox, number_chip):
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
        sn = list(bin(int(last_line[2])+1))
        party = list(type_of_party)
    pace_address_sir = ""
    number_bit = 7 + 2 # 0 and 1 bit ("0b") 7+2
    one = ""
    for i in range(2, len(fam)):
        code[number_bit - i] = int(fam[int(len(fam))+1-i])
        one = one + str(code[number_bit - i])
    number_bit = 11
    for i in range(4):
        code[number_bit - i] = int(party[3-i])
        one = one + str(code[number_bit - i])
    number_bit = 55 + 2
    one = one + " "
    for i in range(2, len(sn)):
        code[number_bit - i] = int(sn[int(len(sn))+1-i])
        one = one + str(code[number_bit - i])
    one = one + " "
    step_i = [7, 15, 23, 31, 39, 47, 55]
    flag = True
    for i in step_i:
        number_i = i
        for j in range(8):
            one = one + str(code[number_i-j])
            if crc[0] == code[number_i-j]:
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
        pace_address_sir = pace_address_sir + str(code[55-i])
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
            # print (pace)
            if col_pace_data == 8:
                break
            pace = ""
            iterator = 0
            pace = pace + str(pace_list[number_element_list])
            number_element_list = number_element_list - 1
        else:
            pace = pace + str(pace_list[number_element_list])
            number_element_list = number_element_list - 1
    write_package(number_chip, 6, full_pace_chr[0], full_pace_chr[1], full_pace_chr[2], full_pace_chr[3], full_pace_chr[4], full_pace_chr[5], full_pace_chr[6], full_pace_chr[7], textbox)
    time.sleep(0.5)
    if not check_mess_microchip():
        textbox.insert(END, 'Error, not write address in chip ' + str(number_chip) + '\n')
    return ishod

'''
END BLOCK WRITE MAIN ADDRESS
'''


'''
BLOCK ACCESSORY
'''
# GET LIST TEMPERATURE
def get_list_temperature():
    global path
    if os.path.exists( path ):
        file_config = open( path, 'r' )
        iterator = 0
        number_start_chip = []
        for list in file_config:
            if iterator == 9:
                number_start_chip = list
            iterator += 1
        file_config.close()
        temperature_list = [int(x) for x in number_start_chip.split(", ")]
        return temperature_list
    else:
        return 0

# GET NUMBER SOURCE
def get_number_source():
    global path
    if os.path.exists( path ):
        file_config = open( path, 'r' )
        iterator = 0
        number_start_chip = []
        for list in file_config:
            if iterator == 8:
                number_start_chip = int( list )
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
def get_com_port_MIT():
    global path
    if os.path.exists(path):
        file_config = open(path, 'r')
        iterator = 0
        for list in file_config:
            if iterator == 3:
                com_port_data = int(list)
            iterator += 1
        file_config.close()
        return com_port_data
    else:
        return 0

# GET NUMBER COM PORT MICROCHIP AUTOMATIC
def get_com_port_microchip():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    result = []
    for port in ports:
        try:
            # print(port)
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

# Загрузить настроки
def load_file_options():
    global path
    data_file = []
    if os.path.exists(path):
        file_config = open(path, 'r')
        for line in file_config:
            data_file.append(line)
        file_config.close()
    if len(data_file) != 10:
        for i in range(10):
            data_file.append(0)
    return data_file

# SAVE CONFIGURATION
def save_file_options(options_windows, number_serii, number_part, number_com_por_microchip, number_start_chip, number_finish_chip,
                      number_com_port_mit, number_start_sensor, number_finish_sensor, variable_source, temperature_termostrim):
    global path
    file_save = open(path, 'w')
    if number_serii == '':
        number_serii = 0
    file_save.write(check_save_line(number_com_por_microchip) + '\n' + check_save_line(number_start_chip) + '\n'
                     + check_save_line(number_finish_chip) + '\n' + check_save_line(number_com_port_mit) + '\n'
                     + check_save_line(number_start_sensor) + '\n' + check_save_line(number_finish_sensor) + '\n'
                     + check_save_line(number_part) + '\n' + check_save_line(str(int(number_serii)+1)) + '\n'
                    + check_save_line(variable_source) + '\n' + check_save_line(temperature_termostrim))
    options_windows.destroy() 
    file_save.close()

# CHECK LINE AND SAVE IN FILE
def check_save_line(text):
    if '\n' in text:
        text = text.split('\n')[0]
    if len(text) == 0:
        return "0"
    return text

# FORM AND GET IDEAL CORFFICIENT K AND B
def get_ideal_k_and_b():
    x_1 = -60
    y_1 = 3280
    x_2 = 125
    y_2 = 784
    k = float((y_1 - y_2)) / float((x_1 - x_2))
    b = y_2 - k * x_2
    return k, b

# FORM USED COM PORT
def form_ser_com_port_chip():
    # ser = serial.Serial("COM" + str(get_com_port_microchip()), 115200, timeout=0)
    ser = serial.Serial(str(get_com_port_microchip()[0]), 115200, timeout=0)
    ser.close()
    ser.open()
    ser.isOpen()
    return ser

def check_click(text):
	answer = tkMessageBox.askokcancel(title="check", message=text)
	return answer
	
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
	
def check_read_temperature(k, b, x_kod):
	temperature = ((x_kod*k+b)-2047)/(-16)
	print(': -> ' + str(temperature))
	
	
'''
END BLOCK ACCESSORY
'''


'''
BLOCK MIT
'''
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
        #test_temp_MIT = str(line_binary)
        #print("DATA MIT " + str(line_binary))
        #print((len(line_binary) >= 1) and ('E' in str(line_binary)) and ('B ' in str(line_binary)))
			#print(int(temp_MIT[-4] + temp_MIT[-3]))
        #print(test_temp_MIT[test_temp_MIT.find("-")+1 : test_temp_MIT.find("B")])
        #~if (len(str(line_binary)) < 22) and (len(str(line_binary)) > 15) and ('E' in str(line_binary)) and ('B ' in str(line_binary)):
        if (len(line_binary) >= 1) and ('E' in str(line_binary)) and ('B ' in str(line_binary)):
            
            #print("DATA MIT " + str(line_binary))
            if (str(list_port_mit[0]) + ':') in str(line_binary) and not flag:
                array_temperature.append( get_temperature_with_mit( line_binary ) )
                flag = True
            if flag:
                #print(int(line_binary[0].split(':')[0]))
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
        hash_map_number_chip_and_port_mit[int(number_chip_and_number_port_mit[0])] = int(number_chip_and_number_port_mit[1])
    file_text.close()
    list_port_mit = []
    for i in range(get_number_start_MIT(), get_number_finish_MIT() + 1):
        #list_port_mit.append(hash_map_number_chip_and_port_mit.get(i))
        list_port_mit.append(i)
    return list_port_mit

'''
END BLOCK MIT
'''


'''
PACKAGE
'''
# FORM COMMANDS
def write_package(number_chip, command, data1, data2, data3, data4, data5, data6, data7, data8, textbox):
    tilda = 126
    commands = []
    for j in range(28):
        if j == 0:
            commands.append( tilda )
        elif j == 1:
            if number_chip > 15:
                commands.append( number_chip )
            else:
                commands.append( 0 )
                commands.append( number_chip )
        elif j == 2:
            if command > 15:
                commands.append( command )
            else:
                commands.append( 0 )
                commands.append( command )
        elif j == 3:
            if data1 > 15:
                commands.append( data1 )
            else:
                commands.append( 0 )
                commands.append( data1 )
        elif j == 4:
            if data2 > 15:
                commands.append( data2 )
            else:
                commands.append( 0 )
                commands.append( data2 )
        elif j == 5:
            if data3 > 15:
                commands.append( data3 )
            else:
                commands.append( 0 )
                commands.append( data3 )
        elif j == 6:
            if data4 > 15:
                commands.append( data4 )
            else:
                commands.append( 0 )
                commands.append( data4 )
        elif j == 7:
            if data5 > 15:
                commands.append( data5 )
            else:
                commands.append( 0 )
                commands.append( data5 )
        elif j == 8:
            if data6 > 15:
                commands.append( data6 )
            else:
                commands.append( 0 )
                commands.append( data6 )
        elif j == 9:
            if data7 > 15:
                commands.append( data7 )
            else:
                commands.append( 0 )
                commands.append( data7 )
        elif j == 10:
            if data8 > 15:
                commands.append( data8 )
            else:
                commands.append( 0 )
                commands.append( data8 )
        else:
            commands.append( 0 )
            commands.append( 0 )
    pac = ""
    for j in commands:
        pac += hex(j)[2:]
    crc32 = hex(calculateCRC32_Mpeg2(pac))
    crc32 = crc32[2:len(crc32) - 1]
    if len(crc32) < 8:
        sum_null = 8 - len(crc32)
        for i in range(sum_null):
            crc32 = '0' + crc32
    pac += crc32
    # textbox.insert(END, pac + '\n')
    # print(pac)
    push_pac_main_method(pac)

# CALCULATION CRC32
def calculateCRC32_Mpeg2(data):
    CRC32_mpeg2_table = [
        0x00000000, 0x04c11db7, 0x09823b6e, 0x0d4326d9, 0x130476dc, 0x17c56b6b,
        0x1a864db2, 0x1e475005, 0x2608edb8, 0x22c9f00f, 0x2f8ad6d6, 0x2b4bcb61,
        0x350c9b64, 0x31cd86d3, 0x3c8ea00a, 0x384fbdbd, 0x4c11db70, 0x48d0c6c7,
        0x4593e01e, 0x4152fda9, 0x5f15adac, 0x5bd4b01b, 0x569796c2, 0x52568b75,
        0x6a1936c8, 0x6ed82b7f, 0x639b0da6, 0x675a1011, 0x791d4014, 0x7ddc5da3,
        0x709f7b7a, 0x745e66cd, 0x9823b6e0, 0x9ce2ab57, 0x91a18d8e, 0x95609039,
        0x8b27c03c, 0x8fe6dd8b, 0x82a5fb52, 0x8664e6e5, 0xbe2b5b58, 0xbaea46ef,
        0xb7a96036, 0xb3687d81, 0xad2f2d84, 0xa9ee3033, 0xa4ad16ea, 0xa06c0b5d,
        0xd4326d90, 0xd0f37027, 0xddb056fe, 0xd9714b49, 0xc7361b4c, 0xc3f706fb,
        0xceb42022, 0xca753d95, 0xf23a8028, 0xf6fb9d9f, 0xfbb8bb46, 0xff79a6f1,
        0xe13ef6f4, 0xe5ffeb43, 0xe8bccd9a, 0xec7dd02d, 0x34867077, 0x30476dc0,
        0x3d044b19, 0x39c556ae, 0x278206ab, 0x23431b1c, 0x2e003dc5, 0x2ac12072,
        0x128e9dcf, 0x164f8078, 0x1b0ca6a1, 0x1fcdbb16, 0x018aeb13, 0x054bf6a4,
        0x0808d07d, 0x0cc9cdca, 0x7897ab07, 0x7c56b6b0, 0x71159069, 0x75d48dde,
        0x6b93dddb, 0x6f52c06c, 0x6211e6b5, 0x66d0fb02, 0x5e9f46bf, 0x5a5e5b08,
        0x571d7dd1, 0x53dc6066, 0x4d9b3063, 0x495a2dd4, 0x44190b0d, 0x40d816ba,
        0xaca5c697, 0xa864db20, 0xa527fdf9, 0xa1e6e04e, 0xbfa1b04b, 0xbb60adfc,
        0xb6238b25, 0xb2e29692, 0x8aad2b2f, 0x8e6c3698, 0x832f1041, 0x87ee0df6,
        0x99a95df3, 0x9d684044, 0x902b669d, 0x94ea7b2a, 0xe0b41de7, 0xe4750050,
        0xe9362689, 0xedf73b3e, 0xf3b06b3b, 0xf771768c, 0xfa325055, 0xfef34de2,
        0xc6bcf05f, 0xc27dede8, 0xcf3ecb31, 0xcbffd686, 0xd5b88683, 0xd1799b34,
        0xdc3abded, 0xd8fba05a, 0x690ce0ee, 0x6dcdfd59, 0x608edb80, 0x644fc637,
        0x7a089632, 0x7ec98b85, 0x738aad5c, 0x774bb0eb, 0x4f040d56, 0x4bc510e1,
        0x46863638, 0x42472b8f, 0x5c007b8a, 0x58c1663d, 0x558240e4, 0x51435d53,
        0x251d3b9e, 0x21dc2629, 0x2c9f00f0, 0x285e1d47, 0x36194d42, 0x32d850f5,
        0x3f9b762c, 0x3b5a6b9b, 0x0315d626, 0x07d4cb91, 0x0a97ed48, 0x0e56f0ff,
        0x1011a0fa, 0x14d0bd4d, 0x19939b94, 0x1d528623, 0xf12f560e, 0xf5ee4bb9,
        0xf8ad6d60, 0xfc6c70d7, 0xe22b20d2, 0xe6ea3d65, 0xeba91bbc, 0xef68060b,
        0xd727bbb6, 0xd3e6a601, 0xdea580d8, 0xda649d6f, 0xc423cd6a, 0xc0e2d0dd,
        0xcda1f604, 0xc960ebb3, 0xbd3e8d7e, 0xb9ff90c9, 0xb4bcb610, 0xb07daba7,
        0xae3afba2, 0xaafbe615, 0xa7b8c0cc, 0xa379dd7b, 0x9b3660c6, 0x9ff77d71,
        0x92b45ba8, 0x9675461f, 0x8832161a, 0x8cf30bad, 0x81b02d74, 0x857130c3,
        0x5d8a9099, 0x594b8d2e, 0x5408abf7, 0x50c9b640, 0x4e8ee645, 0x4a4ffbf2,
        0x470cdd2b, 0x43cdc09c, 0x7b827d21, 0x7f436096, 0x7200464f, 0x76c15bf8,
        0x68860bfd, 0x6c47164a, 0x61043093, 0x65c52d24, 0x119b4be9, 0x155a565e,
        0x18197087, 0x1cd86d30, 0x029f3d35, 0x065e2082, 0x0b1d065b, 0x0fdc1bec,
        0x3793a651, 0x3352bbe6, 0x3e119d3f, 0x3ad08088, 0x2497d08d, 0x2056cd3a,
        0x2d15ebe3, 0x29d4f654, 0xc5a92679, 0xc1683bce, 0xcc2b1d17, 0xc8ea00a0,
        0xd6ad50a5, 0xd26c4d12, 0xdf2f6bcb, 0xdbee767c, 0xe3a1cbc1, 0xe760d676,
        0xea23f0af, 0xeee2ed18, 0xf0a5bd1d, 0xf464a0aa, 0xf9278673, 0xfde69bc4,
        0x89b8fd09, 0x8d79e0be, 0x803ac667, 0x84fbdbd0, 0x9abc8bd5, 0x9e7d9662,
        0x933eb0bb, 0x97ffad0c, 0xafb010b1, 0xab710d06, 0xa6322bdf, 0xa2f33668,
        0xbcb4666d, 0xb8757bda, 0xb5365d03, 0xb1f740b4
    ]
    CRC32 = 0xffffffff
    data_test = []
    iterator = 0
    while iterator < len( data ):
        data_test.append( int( data[iterator] + data[iterator + 1], 16 ) )
        # data_test.append(int(data[iterator], 16))
        iterator += 2
    for i in data_test:
        CRC32 = ((CRC32 << 8) ^ CRC32_mpeg2_table[((CRC32 >> 24) ^ int( hex( i ), 16 )) & 0xff]) & 0xffffffff
    return CRC32

# WRITE COMMANDS
def push_pac_main_method(pac):
    global ser
    byte_pac = form_list_byte( pac )
    for i in byte_pac:
        ser.write( i )

'''
END PACKAGE
'''

'''
LOGGER
'''
def new_parth_logger(number):
	global path_in_data
	if number == 0:
		f = open(path_in_data + 'logger_user.lg', 'w')
	elif number == 1:
		f = open(path_in_data + 'logger.lg', 'w')
	f.close()
	
def write_log(text, number):
	global path_in_data
	if number == 0:
		f = open(path_in_data + 'logger_user.lg', 'a')
	elif number == 1:
		f = open(path_in_data + 'logger.lg', 'a')
	f.write(text + '\n')
	f.close()
'''
END LOGGER
'''


# READ TEMPERATURE
def give_me_temperature_chip(textbox, number_chip):
    global ser
    command = 2
    parameters = 0  # ? OR 2
    bin_list = []  # number chip:bin code
    write_package( number_chip, command, parameters, 0, 0, 0, 0, 0, 0, 0, textbox )
    str_bit_in_chip = ""
    for i in range(25):
        time.sleep(0.5)
        bit_in_chip = ser.readlines()
        print(str(bit_in_chip))
        if len(bit_in_chip) > 0:
            str_bit_in_chip = str(bit_in_chip)[2:len(str(bit_in_chip))-4]
            break
    inv_str_bin_code = ""
    for i in range(len(str_bit_in_chip)):
        if i <= 4:
            inv_str_bin_code += str_bit_in_chip[i]
        else:
            if "0" in str_bit_in_chip[i]:
                inv_str_bin_code += "1"
            elif "1" in str_bit_in_chip[i]:
                inv_str_bin_code += "0"
            else:
                print ("ERROR")
                break
    bin_list.append(str(inv_str_bin_code))
    if len(bit_in_chip) == 0:
        textbox.insert(END, 'Chip ' + str(number_chip) + ' : ' + 'no temperature' + '\n')
    else:
        textbox.insert(END, 'Chip ' + str(number_chip) + ' : ' + str(inv_str_bin_code) + '\n')
    return bin_list[0]


# FORM TEMPERATURE IN CHIPS, NEED DELAY 3000 mS
def form_temperature_in_all_chips(textbox):
    write_package( 255, 4, 0, 0, 0, 0, 0, 0, 0, 0, textbox )


# FORM LIST BYTES IN PAC
def form_list_byte(pac):
    byte_pac = []
    for i in range( 0, len( pac ), 2 ):
        byte_pac.append( chr( int( pac[i] + pac[i + 1], 16 ) ) )
    return byte_pac

'''
FORM WINDOWS
'''

def start_menu(ev):
    global height_param
    global width_param
    global parameter
    global ser

    start_menu_windows = Tk()
    start_menu_windows.title("start_menu")
    start_menu_windows.iconbitmap('C:/main_programs_micros/LogoDCS(16x16).ico')
    #start_menu_windows.update()

    panel_start_frame = Frame(start_menu_windows, height=height_param * 1.3, width=width_param, bg='#3498db')
    panel_start_frame.pack(side='top', fill='x')

    text_frame = Frame(start_menu_windows, height=height_param - height_param / 2, width=width_param)
    text_frame.pack(side='bottom', fill='both', expand=1)

    textbox = Text(text_frame, font='Arial 10', wrap='word')
    scrollbar = Scrollbar(text_frame)

    scrollbar['command'] = textbox.yview
    textbox['yscrollcommand'] = scrollbar.set

    textbox.pack(side='left', fill='both', expand=1)
    scrollbar.pack(side='right', fill='y')

    # BUTTON
    if parameter == 0:
        color = "red"
    else:
        color = "green"
    button_voltage = Button(panel_start_frame, text='Упарвление питанием', bg=color, command=lambda: app_voltage(textbox, button_voltage))
    button_give_temperature = Button(panel_start_frame, text='Записать REZ и адрес', command=lambda: write_rez_and_address(textbox))
    button_read_address = Button(panel_start_frame, text='Начать измерения', command=lambda: read_temperature_and_write_data_file(textbox))
    button_write_address = Button(panel_start_frame, text='Записать коэффичиенты')
    button_write_rez = Button(panel_start_frame, text='Записать память ОТР')
    button_write_memory_otp = Button(panel_start_frame, text='Автоматический режим')

    button_voltage.place(x=width_param / 2 - 55, y=10, height=30, width=150)
    button_give_temperature.place(x=width_param / 2 - 55, y=50, height=30, width=150)
    button_read_address.place(x=width_param / 2 - 55, y=90, height=30, width=150)
    button_write_address.place(x=width_param / 2 - 55, y=130, height=30, width=150)
    button_write_rez.place(x=width_param / 2 - 55, y=170, height=30, width=150)
    button_write_memory_otp.place(x=width_param / 2 - 55, y=210, height=30, width=150)

    start_menu_windows.mainloop()

def commands_menu(ev):
    global height_param
    global width_param
    global parameter

    commands_windows = Tk()
    commands_windows.title("commands_menu")
    commands_windows.iconbitmap('C:/main_programs_micros/LogoDCS(16x16).ico')
    commands_windows.update()

    panel_commands_frame = Frame(commands_windows, height=height_param * 1.6, width=width_param, bg='#3498db')
    #e74c3c
    panel_commands_frame.pack(side='top', fill='x')

    text_frame = Frame(commands_windows, height=height_param - height_param / 2, width=width_param)
    text_frame.pack(side='bottom', fill='both', expand=1)

    textbox = Text(text_frame, font='Arial 10', wrap='word')
    scrollbar = Scrollbar(text_frame)

    scrollbar['command'] = textbox.yview
    textbox['yscrollcommand'] = scrollbar.set

    textbox.pack(side='left', fill='both', expand=1)
    scrollbar.pack(side='right', fill='y')
    # LABLE
    lable_work_in_files = Label(panel_commands_frame, text='Работа с файлами', font='arial 13', bg='#3498db')
    lable_write_in_chips = Label(panel_commands_frame, text='Основные команды', font='arial 13', bg='#3498db')
    lable_read_data_in_chip = Label(panel_commands_frame, text='Запись данных', font='arial 13', bg='#3498db')


    lable_work_in_files.place(x=width_param/2 - 150, y=30, height=30, width=150, anchor="n")
    lable_write_in_chips.place(x=width_param/2 + 30 , y=30, height=30, width=150, anchor="n")
    lable_read_data_in_chip.place(x=width_param/2 + 210, y=30, height=30, width=150, anchor="n")
    # BUTTON
    if parameter == 0:
        color = "red"
    else:
        color = "green"
    button_voltage = Button(panel_commands_frame, text='Управление питанием', bg=color, command=lambda: app_voltage(textbox, button_voltage))
    button_give_temperature = Button(panel_commands_frame, text='Считать темп. код', bg= '#e39696', command=lambda: read_temperature(textbox))
    button_read_address = Button(panel_commands_frame, text='Считать адрес', bg= '#e39696', command=lambda: read_address(textbox))
    button_write_address = Button(panel_commands_frame, text='Записать адрес', bg = '#58aab0', command=lambda: write_address(textbox))
    button_write_rez = Button(panel_commands_frame, text='Записать REZ', bg = '#58aab0', command=lambda: write_rez(textbox))
    button_write_memory_otp = Button(panel_commands_frame, text='Записать память OTP', bg = '#58aab0', command=lambda: write_OTP_block(textbox))
    button_read_memory_otp = Button(panel_commands_frame, text='Считать память OTP', bg= '#e39696', command=lambda: read_OTP_block(textbox))
    button_write_enable2 = Button(panel_commands_frame, text='Записать enable2', bg = '#58aab0', command=lambda: write_en_2(textbox))
    button_write_coefficients_b_and_b = Button(panel_commands_frame, text='Записать коэффициенты', bg = '#58aab0', command=lambda: write_coefficient_k_and_b(textbox))
    #button_test_work_chip = Button(panel_commands_frame, text='Проверка микросхем', command=lambda: verification_chips(textbox))
    button_test_work_chip = Button( panel_commands_frame, text='Считать температуру', bg= '#e39696', command=lambda: check_real_temperature( textbox ))
    button_new_path = Button(panel_commands_frame, text='Работа с новой партией', bg= '#8ae68d', command=lambda: work_new_parth())
    button_form_archive = Button(panel_commands_frame, text='Сохранить в архив', bg= '#8ae68d', command=lambda: main_save_archive())
    button_write_address_in_file = Button(panel_commands_frame, text='Считать адреса в файл', bg= '#8ae68d', command=lambda: form_address_file(textbox))
    button_check_address = Button(panel_commands_frame, text='Проверить адреса', bg= '#8ae68d', command=lambda: check_address(textbox))
    button_main_work = Button(panel_commands_frame, text='Начать измерения', bg= '#e3c119',command=lambda: read_temperature_and_write_data_file(textbox))
    button_full_test = Button(panel_commands_frame, text='Tap me', bg= '#58aab0',command=lambda: finaly_test_all_chip(textbox))

    button_voltage.place(x=width_param / 2 - 45, y=80, height=30, width=150)
    button_give_temperature.place(x=width_param / 2 - 45, y=120, height=30, width=150)
    button_test_work_chip.place(x=width_param / 2 - 45, y=160, height=30, width=150)
    button_read_address.place(x=width_param / 2 - 45, y=200, height=30, width=150)
    button_read_memory_otp.place(x=width_param / 2 - 45, y=240, height=30, width=150)
    button_main_work.place(x=width_param / 2 - 45, y=300, height=30, width=150)
    button_write_address.place(x=width_param / 2 + 135, y=80, height=30, width=150)
    button_write_rez.place(x=width_param / 2 + 135, y=120, height=30, width=150)
    button_write_memory_otp.place(x=width_param / 2 + 135, y=200, height=30, width=150)
    button_write_enable2.place(x=width_param / 2 + 135, y=240, height=30, width=150) #111
    button_write_coefficients_b_and_b.place(x=width_param / 2 + 135, y=160, height=30, width=150)
    button_new_path.place(x=width_param/2 - 225, y=80, height=30, width=150)
    button_form_archive.place(x=width_param/2 - 225, y=160, height=30, width=150)
    button_write_address_in_file.place(x=width_param/2 - 225, y=120, height=30, width=150)
    button_check_address.place(x=width_param/2 - 225, y=220, height=30, width=150)
	button_write_enable2.place(x=width_param / 2 + 135, y=280, height=30, width=150)

    commands_windows.mainloop()

def form_option(ev):
    global height_param
    global width_param
    global var

    options_windows = Tk()
    options_windows.title("configuration_menu")
    options_windows.iconbitmap('../LogoDCS(16x16).ico')
    panel_options_frame = Frame(options_windows, height=height_param + 30, width=width_param + 300, bg='#3498db')
    panel_options_frame.pack( side='top', fill='x' )

    # LABLE
    lable_com_port_microchip = Label(panel_options_frame, text='№ COM порта микроконтроллера', font='arial 8')
    lable_number_start_chip = Label(panel_options_frame, text='№ первой микросхемы', font='arial 8')
    lable_number_finish_chip = Label(panel_options_frame, text='№ последней микросхемы', font='arial 8')
    lable_com_port_mit = Label(panel_options_frame, text='№ COM порта MIT', font='arial 8' )
    lable_number_start_datchik = Label(panel_options_frame, text='№ первого датчика', font='arial 8')
    lable_number_finish_datchik = Label(panel_options_frame, text='№ последнего датчика', font='arial 8')
    lable_messenger = Label(panel_options_frame, text='Настройка адреса микросхемы', font='arial 8')
    lable_choose = Label(panel_options_frame, text='Выбор источника', font='arial 8')
    lable_part = Label(panel_options_frame, text='Номер партии', font='arial 8')
    lable_temperature_termostrim = Label(panel_options_frame, text='Температура:', font='arial 8')
    lable_source = Label(panel_options_frame, text=' 1 - YOKOGAWA' + '\n' + '2 - REGOL', font='arial 8')

    lable_com_port_microchip.place(x=100, y=30, height=30, width=180, anchor="n")
    lable_number_start_chip.place(x=100, y=70, height=30, width=180, anchor="n")
    lable_number_finish_chip.place(x=100, y=110, height=30, width=180, anchor="n")
    lable_com_port_mit.place(x=100, y=150, height=30, width=180, anchor="n")
    lable_number_start_datchik.place(x=100, y=190, height=30, width=180, anchor="n")
    lable_number_finish_datchik.place(x=100, y=230, height=30, width=180, anchor="n")
    lable_messenger.place(x=300 + 90, y=30, height=30, width=180, anchor="n")
    lable_choose.place( x=540 + 90, y=30, height=30, width=180, anchor="n" )
    lable_part.place( x=300 + 45, y=70, height=30, width=90, anchor="n" )
    lable_temperature_termostrim.place( x=300 + 45, y=200, height=30, width=90, anchor="n" )
    lable_source.place(x=540 + 45, y=70, height=30, width=90, anchor="n")

    # TEXTBOX
    textbox_com_port_microchip = Text(panel_options_frame, font='Arial 12', wrap='word')
    textbox_number_start_chip = Text(panel_options_frame, font='Arial 12', wrap='word')
    textbox_number_finish_chip = Text(panel_options_frame, font='Arial 12', wrap='word')
    textbox_com_port_mit = Text(panel_options_frame, font='Arial 12', wrap='word')
    textbox_number_start_sensor = Text(panel_options_frame, font='Arial 12', wrap='word')
    textbox_number_finish_sensor = Text(panel_options_frame, font='Arial 12', wrap='word')
    textbox_part = Text(panel_options_frame, font='Arial 12', wrap='word')
    textbox_source = Text(panel_options_frame, font='Arial 12', wrap='word')
    textbox_temperature_termostrim = Text(panel_options_frame, font='Arial 12', wrap='word')

    textbox_temperature_termostrim.place(x=405, y=200, height=30, width=230)
    textbox_com_port_microchip.place(x=200, y=30, height=30, width=35)
    textbox_number_start_chip.place(x=200, y=70, height=30, width=35)
    textbox_number_finish_chip.place(x=200, y=110, height=30, width=35)
    textbox_com_port_mit.place(x=200, y=150, height=30, width=35)
    textbox_number_start_sensor.place(x=200, y=190, height=30, width=35)
    textbox_number_finish_sensor.place(x=200, y=230, height=30, width=35)
    textbox_part.place(x=400, y=70, height=30, width=45)
    textbox_source.place(x=640, y=70, height=30, width=45)

    # LIST BOX
    listbox_address = Listbox(panel_options_frame, height=5, width=15, selectmode=SINGLE)
    list_address = ["BMK_GEN (0x28)", "BMK_DIODE (0x29)", "CUSTOM_GEN (0x06)", "CUSTOM_DIODE (0x07)",
                    "TEST_SAMPLE (0xAD)"]
    for i in list_address:
        listbox_address.insert(END, i)
    listbox_address.place(x=300 + 90, y=110, height=80, width=180, anchor="n")

    # LOAD FILE
    load_file = load_file_options()

    textbox_com_port_microchip.insert(END, str(load_file[0]))
    textbox_number_start_chip.insert(END, str(load_file[1]))
    textbox_number_finish_chip.insert(END, str(load_file[2]))
    textbox_com_port_mit.insert(END, str(load_file[3]))
    textbox_number_start_sensor.insert(END, str(load_file[4]))
    textbox_number_finish_sensor.insert(END, str(load_file[5]))
    textbox_part.insert(END, str(load_file[6]))
    textbox_source.insert(END, str(load_file[8]))
    textbox_temperature_termostrim.insert(END, str(load_file[9]))


    # BUTTON
    button_save = Button(panel_options_frame, text='Сохранить', command=lambda: save_file_options(options_windows, str(listbox_address.curselection())[1:len(str(listbox_address.curselection())) - 2],
        textbox_part.get('1.0', END),
        textbox_com_port_microchip.get('1.0', END),
        textbox_number_start_chip.get('1.0', END),
        textbox_number_finish_chip.get('1.0', END),
        textbox_com_port_mit.get('1.0', END),
        textbox_number_start_sensor.get('1.0', END),
        textbox_number_finish_sensor.get('1.0', END),
        textbox_source.get('1.0', END),
        textbox_temperature_termostrim.get('1.0', END)))
    button_out = Button(panel_options_frame, text='Выход', command=options_windows.destroy)

    button_save.place(x=width_param + 10 + 60, y=height_param - 30 + 30, height=30, width=100, anchor="w")
    button_out.place(x=width_param + 130 + 60, y=height_param - 30 + 30, height=30, width=100, anchor="w")

    options_windows.mainloop()

# GLOBAL VARIABLE
parameter = 0  # ON/OFF SOURCE MICROCHIP
path = "../configuration/save_config.txt"  # FILE SAVE CONFIG
path_in_address_all_memory_otp_in_one_chip = '../address/all_address_otp_in_one_chip_'
path_in_address_all_memory_otp_in_one_chip_write = '../address/all_address_otp_in_one_chip_write_'
path_in_data = '../data/'
path_all_address = '../listing_file/'
path_map_mit_ports = '../configuration/map_MIT_and_chip.txt'
time_sleep_MIT = 40  # SECOND STEP MIT
max_current = 0.4  # CURRENT
var = 0  # PARAMETER SOURCE
ser = 0  # SERIAL PORT

if __name__ == "__main__":
    # MAIN PROGRAMS
    start_windows = Tk()
    start_windows.title("main_menu")
    start_windows.iconbitmap( '../LogoDCS(16x16).ico' )

    height_param = 250
    width_param = 500

    panelFrame = Frame(start_windows, height=height_param, width=width_param, bg='#3498db')
    panelFrame.pack(side='top', fill='both')

    options = Button(panelFrame, text='Настройка')

    options.bind("<Button-1>", form_option)

    # width=40,

    options.place(x=width_param / 2 - 85, y=height_param / 2 - 50, height=30, width=170)

    try:
        flag_open_option = 0
        ser = form_ser_com_port_chip()
    except:
        tkMessageBox.showwarning("Ошибка", "Не найдено устройство по введенному COM порту," + "\n" +
                                 "проверте в настройках введнный COM порт и перезагрузите программу.")
        ser = 0
    if ser != 0:
        commands = Button(panelFrame, text='Список команд')
        #main_programs = Button(panelFrame, text='Старт')

        #main_programs.place(x=width_param / 2 - 85, y=height_param / 2 - 60, height=30, width=170)
        commands.place(x=width_param / 2 - 85, y=height_param / 2 - 5, height=30, width=170)

        commands.bind("<Button-1>", commands_menu)
        #main_programs.bind("<Button-1>", start_menu)

    start_windows.mainloop()
