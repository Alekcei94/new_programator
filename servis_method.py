import serial
import sys
import time

def write_commands(ser, byte_0, byte_1, byte_2, byte_3):
    pac = 0
    pac += int(byte_0)
    pac += int(byte_1)
    pac += int(byte_2)
    ser.write(bytes([byte_0]))
    ser.flush()
    ser.write(bytes([byte_1]))
    ser.flush()
    ser.write(bytes([byte_2]))
    ser.flush();
    ser.write(bytes([byte_3]))
    ser.flush();
    print(bytes([byte_0]))
    print(bytes([byte_1]))
    print(bytes([byte_2]))
    print(bytes([byte_3]))
    # ser.close()
    '''
    crc32 = hex(getCRC32_Mpeeg2(pac))[2:]
    if len(crc32) < 16:
        sum_null = 16 - len(crc32)
        for i in range(sum_null):
            crc32 = '0' + crc32
    pac += hex(crc32)[]

    byte_pac = form_list_byte(pac)
    for i in byte_pac:
        ser.write(bytes([i]))
    '''

def form_list_byte(pac):
    byte_pac = []
    for i in range(0, len(pac), 2):
        byte_pac.append(chr(int(pac[i] + pac[i + 1], 16)))
    return byte_pac

def get_ser_com():
    ser = serial.Serial('COM3', 115200, timeout=1)
    time.sleep(2)
    # ser.close()
    # ser.open()
    # ser.isOpen()
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

def serch_claster_and_number(number_mk):
    if number_mk % 8 == 0:
        claster = (number_mk // 8) - 1
        number = 8
    else:
        claster = number_mk // 8
        number = (number_mk - (claster) * 8)
        claster = claster + 16
    return claster, number