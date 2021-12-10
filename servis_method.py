import serial
import sys
import time

import basic_commands_onewire


def write_commands(ser, byte_0, byte_1, byte_2, byte_3):
    crc = form_crc(byte_0, byte_1, byte_2, byte_3)
    print("Commands " + str(byte_0) + "_" + str(byte_1) + "_" + str(byte_2) + "_" + str(byte_3) + "_" + str(crc))
    ser.write(bytes([byte_0]))
    ser.write(bytes([byte_1]))
    ser.write(bytes([byte_2]))
    ser.write(bytes([byte_3]))
    ser.write(bytes([crc]))
    print("Waiting for the master's response")
    while True:
        if ser.waitForReadyRead(4):
            if (int.from_bytes(ser.read(), "big")) == 51:
                print("Master confirmed")
                break
            elif (int.from_bytes(ser.read(), "big")) == 54:
                write_commands(ser, byte_0, byte_1, byte_2, byte_3)
            else:
                print("Master's answer " + str(int.from_bytes(ser.read(), "big")))
        else:
            ser.write(bytes([0]))
    print("Waiting for a slave's response")
    while True:
        if ser.waitForReadyRead(4):
            if (int.from_bytes(ser.read(), "big")) == 68:
                print("Slave's confirmed")
                break
        print("Slave's's answer " + str(int.from_bytes(ser.read(), "big")))


def get_ser_com():
    ser = serial.Serial('COM3', 115200, timeout=4)
    time.sleep(2)
    return ser


def get_com_port():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def search_claster_and_number(number_mk):
    if number_mk % 8 == 0:
        claster = (number_mk // 8) - 1 + 16
        number = 8
    else:
        claster = number_mk // 8
        number = (number_mk - claster * 8)
        claster = claster + 16
    return claster, number


def form_crc(data_0, data_1, data_2, data_3):
    list_Test = [data_0, data_1, data_2, data_3]
    crc8Table = [
        0x00, 0x5E, 0xBC, 0xE2, 0x61, 0x3F, 0xDD, 0x83,
        0xC2, 0x9C, 0x7E, 0x20, 0xA3, 0xFD, 0x1F, 0x41,
        0x9D, 0xC3, 0x21, 0x7F, 0xFC, 0xA2, 0x40, 0x1E,
        0x5F, 0x01, 0xE3, 0xBD, 0x3E, 0x60, 0x82, 0xDC,
        0x23, 0x7D, 0x9F, 0xC1, 0x42, 0x1C, 0xFE, 0xA0,
        0xE1, 0xBF, 0x5D, 0x03, 0x80, 0xDE, 0x3C, 0x62,
        0xBE, 0xE0, 0x02, 0x5C, 0xDF, 0x81, 0x63, 0x3D,
        0x7C, 0x22, 0xC0, 0x9E, 0x1D, 0x43, 0xA1, 0xFF,
        0x46, 0x18, 0xFA, 0xA4, 0x27, 0x79, 0x9B, 0xC5,
        0x84, 0xDA, 0x38, 0x66, 0xE5, 0xBB, 0x59, 0x07,
        0xDB, 0x85, 0x67, 0x39, 0xBA, 0xE4, 0x06, 0x58,
        0x19, 0x47, 0xA5, 0xFB, 0x78, 0x26, 0xC4, 0x9A,
        0x65, 0x3B, 0xD9, 0x87, 0x04, 0x5A, 0xB8, 0xE6,
        0xA7, 0xF9, 0x1B, 0x45, 0xC6, 0x98, 0x7A, 0x24,
        0xF8, 0xA6, 0x44, 0x1A, 0x99, 0xC7, 0x25, 0x7B,
        0x3A, 0x64, 0x86, 0xD8, 0x5B, 0x05, 0xE7, 0xB9,
        0x8C, 0xD2, 0x30, 0x6E, 0xED, 0xB3, 0x51, 0x0F,
        0x4E, 0x10, 0xF2, 0xAC, 0x2F, 0x71, 0x93, 0xCD,
        0x11, 0x4F, 0xAD, 0xF3, 0x70, 0x2E, 0xCC, 0x92,
        0xD3, 0x8D, 0x6F, 0x31, 0xB2, 0xEC, 0x0E, 0x50,
        0xAF, 0xF1, 0x13, 0x4D, 0xCE, 0x90, 0x72, 0x2C,
        0x6D, 0x33, 0xD1, 0x8F, 0x0C, 0x52, 0xB0, 0xEE,
        0x32, 0x6C, 0x8E, 0xD0, 0x53, 0x0D, 0xEF, 0xB1,
        0xF0, 0xAE, 0x4C, 0x12, 0x91, 0xCF, 0x2D, 0x73,
        0xCA, 0x94, 0x76, 0x28, 0xAB, 0xF5, 0x17, 0x49,
        0x08, 0x56, 0xB4, 0xEA, 0x69, 0x37, 0xD5, 0x8B,
        0x57, 0x09, 0xEB, 0xB5, 0x36, 0x68, 0x8A, 0xD4,
        0x95, 0xCB, 0x29, 0x77, 0xF4, 0xAA, 0x48, 0x16,
        0xE9, 0xB7, 0x55, 0x0B, 0x88, 0xD6, 0x34, 0x6A,
        0x2B, 0x75, 0x97, 0xC9, 0x4A, 0x14, 0xF6, 0xA8,
        0x74, 0x2A, 0xC8, 0x96, 0x15, 0x4B, 0xA9, 0xF7,
        0xB6, 0xE8, 0x0A, 0x54, 0xD7, 0x89, 0x6B, 0x35]

    crc = 0
    for i in list_Test:
        crc = crc8Table[crc ^ i]
    return crc


# Запуск команды прожига, висит задержка в 250 милли секунд
def pr(ser, claster, number):
    write_commands(ser, claster, number, 208, 0)  # D0 опустить линию DQ
    write_commands(ser, claster, number, 168, 0)  # A8 поднять линию PR
    write_commands(ser, claster, number, 165, 13)  # A5 задержка 260мС
    write_commands(ser, claster, number, 169, 0)  # A9 опустить линию PR
    write_commands(ser, claster, number, 209, 0)  # D1 поднять линию DQ


#  Получение данных из мк, необходимо осмыслить его и переделать
def read_data_in_mk(claster, number, number_of_bytes, read_flag):
    global ser
    write_commands(ser, claster, number, 167, number_of_bytes)  # A7 передача из master на ПК
    # time.sleep(5)
    buf = []
    address = []
    temperature = 0
    flag_ok = True
    while flag_ok:
        for i in range(number_of_bytes):
            data = ser.read()
            if data != b'':
                buf.append(data)
        if len(buf) == 2 and not read_flag:
            t_cod = (int.from_bytes(buf[0], "big") | (int.from_bytes(buf[1], "big") << 8))
            print("T_code: " + str(t_cod))
            flag_ok = False
            temperature = float(t_cod * 0.0625)
            print("Temperature: " + str(temperature))
        elif len(buf) == 2 and read_flag:
            t_cod = (int.from_bytes(buf[0], "big") | ((int.from_bytes(buf[1], "big") & 0x0f) << 8))
            print("T_code_otp: " + str(t_cod))
            flag_ok = False
        else:
            for j in range(len(buf)):
                address.append(int.from_bytes(buf[j], "big"))
            print("Address: " + str(address))
            flag_ok = False
    return temperature


# Управление питанием
# Если приходит Ложь, включить питание, иначе включить
def all_vdd(first_mk, last_mk, save_object):
    ser = basic_commands_onewire.get_ser()
    choose_voltage_level(ser, save_object)
    select_operating_mode(ser, save_object)
    switcher = getattr(save_object, "voltage_state")
    claster_first, number_first = search_claster_and_number(first_mk)
    claster_last, number_last = search_claster_and_number(last_mk)
    if not switcher:
        commands = 161
        switcher = True
    else:
        commands = 160
        switcher = False
    setattr(save_object, "voltage_state", switcher)
    for iterator in range(claster_first, claster_last + 1):
        write_commands(ser, iterator, 10, commands, 0)
    return switcher


# Установить напряжения по всем микросхемам
def choose_voltage_level(ser, save_object):
    list_voltage = getattr(save_object, "list_voltage")
    for iterator in range(len(list_voltage)):
        if int(list_voltage[iterator]) == 3:
            write_commands(ser, iterator, 10, 179, 0)
        elif int(list_voltage[iterator]) == 5:
            write_commands(ser, iterator, 10, 181, 0)


# Выбрать режим работы микросхем
def select_operating_mode(ser, save_object):
    list_voltage = getattr(save_object, "list_voltage")
    for iterator in range(len(list_voltage)):
        if int(list_voltage[iterator]) == 1 or int(list_voltage[iterator]) == 2 or int(list_voltage[iterator]) == 3:
            write_commands(ser, iterator, 10, 192, int(list_voltage[iterator]))


# повесить задержку на несколько кластеров
def sleep_slave_1(first_mk, last_mk, timer):
    claster_first, number_first = search_claster_and_number(first_mk)
    claster_last, number_last = search_claster_and_number(last_mk)
    time = int(timer / 20)
    for iterator in range(claster_first, claster_last + 1):
        write_commands(ser, iterator, 10, 165, time)
