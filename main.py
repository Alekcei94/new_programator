import servis_method
import save_options


# def queue_test_teams(number_mk):
#     claster, number = servis_method.serch_claster_and_number(number_mk)
#     servis_method.write_commands(ser, claster, number, 170, 0)  # AA
#     servis_method.write_commands(ser, claster, number, 166, 56)  # not command
#     servis_method.write_commands(ser, claster, number, 166, 7)
#     servis_method.write_commands(ser, claster, number, 166, 48)
#     servis_method.write_commands(ser, claster, number, 166, 0)
#     servis_method.write_commands(ser, claster, number, 166, 1)
#     servis_method.write_commands(ser, claster, number, 166, 94)
#     servis_method.write_commands(ser, claster, number, 166, 6)
#     servis_method.write_commands(ser, claster, number, 166, 140)
#     servis_method.write_commands(ser, claster, number, 166, 219)
#     pr(number_mk)


def read_otp_address(number_mk, number_OTP_mem):
    address_otp_list = [[0, 248], [8, 248], [16, 248], [24, 248], [32, 248], [40, 248], [48, 248], [56, 248], [64, 248],
                        [72, 248], [80, 248], [88, 248], [96, 248], [104, 248], [112, 248], [120, 248], [128, 248],
                        [136, 248], [144, 248], [152, 248], [160, 248], [168, 248], [176, 248], [184, 248], [192, 248],
                        [200, 248], [208, 248], [216, 248], [224, 248], [232, 248], [240, 248], [248, 248], [0, 249],
                        [8, 249], [16, 249], [24, 249], [32, 249], [40, 249], [48, 249], [56, 249], [64, 249],
                        [72, 249], [80, 249], [88, 249], [96, 249], [104, 249], [112, 249], [120, 249], [128, 249],
                        [136, 249], [144, 249], [152, 249], [160, 249], [168, 249], [176, 249], [184, 249], [192, 249],
                        [200, 249], [208, 249], [216, 249], [224, 249], [232, 249], [240, 249], [248, 249], [0, 250],
                        [8, 250], [16, 250], [24, 250], [32, 250], [40, 250], [48, 250], [56, 250], [64, 250],
                        [72, 250], [80, 250], [88, 250], [96, 250], [104, 250], [112, 250], [120, 250], [128, 250],
                        [136, 250], [144, 250], [152, 250], [160, 250], [168, 250], [176, 250], [184, 250], [192, 250],
                        [200, 250], [208, 250], [216, 250], [224, 250], [232, 250], [240, 250], [248, 250], [0, 251],
                        [8, 251], [16, 251], [24, 251], [32, 251], [40, 251], [48, 251], [56, 251], [64, 251],
                        [72, 251], [80, 251], [88, 251], [96, 251], [104, 251], [112, 251], [120, 251], [128, 251],
                        [136, 251], [144, 251], [152, 251], [160, 251], [168, 251], [176, 251], [184, 251], [192, 251],
                        [200, 251], [208, 251], [216, 251], [224, 251], [232, 251], [240, 251], [248, 251], [0, 252],
                        [8, 252], [16, 252], [24, 252], [32, 252], [40, 252], [48, 252], [56, 252], [64, 252],
                        [72, 252], [80, 252], [88, 252], [96, 252], [104, 252], [112, 252], [120, 252], [128, 252],
                        [136, 252], [144, 252], [152, 252], [160, 252], [168, 252], [176, 252], [184, 252], [192, 252],
                        [200, 252], [208, 252], [216, 252], [224, 252], [232, 252], [240, 252], [248, 252], [0, 253],
                        [8, 253], [16, 253], [24, 253], [32, 253], [40, 253], [48, 253], [56, 253], [64, 253],
                        [72, 253], [80, 253], [88, 253], [96, 253], [104, 253], [112, 253], [120, 253], [128, 253],
                        [136, 253], [144, 253], [152, 253], [160, 253], [168, 253], [176, 253], [184, 253], [192, 253],
                        [200, 253], [208, 253], [216, 253], [224, 253], [232, 253], [240, 253], [248, 253], [0, 254],
                        [8, 254], [16, 254], [24, 254], [32, 254], [40, 254], [48, 254], [56, 254], [64, 254],
                        [72, 254], [80, 254], [88, 254], [96, 254], [104, 254], [112, 254], [120, 254], [128, 254],
                        [136, 254], [144, 254], [152, 254], [160, 254], [168, 254], [176, 254], [184, 254], [192, 254],
                        [200, 254], [208, 254], [216, 254], [224, 254], [232, 254], [240, 254], [248, 254], [0, 255],
                        [8, 255], [16, 255], [24, 255], [32, 255], [40, 255], [48, 255], [56, 255], [64, 255],
                        [72, 255], [80, 255], [88, 255], [96, 255], [104, 255], [112, 255], [120, 255], [128, 255],
                        [136, 255], [144, 255], [152, 255], [160, 255], [168, 255], [176, 255], [184, 255], [192, 255],
                        [200, 255], [208, 255], [216, 255], [224, 255], [232, 255], [240, 255], [248, 255]]

    global ser
    claster, number = servis_method.serch_claster_and_number(number_mk)
    servis_method.write_commands(ser, claster, number, 170, 0)  # AA
    servis_method.write_commands(ser, claster, number, 166, 228)  # A6 e4
    servis_method.write_commands(ser, claster, number, 166, address_otp_list[number_OTP_mem][0])  # A6 data_0
    servis_method.write_commands(ser, claster, number, 166, address_otp_list[number_OTP_mem][1])  # A6 data_1
    address_otp_cod = read_data_in_mk(claster, number, 2, False)
    return address_otp_cod


def form_temp_cod_not_activ(number_mk):
    global ser
    claster, number = servis_method.serch_claster_and_number(number_mk)
    servis_method.write_commands(ser, claster, number, 170, 0)  # AA
    servis_method.write_commands(ser, claster, number, 166, 204)  # A6 CC
    servis_method.write_commands(ser, claster, number, 166, 68)  # A6 44


def read_temp_activ(number_mk):
    global ser
    claster, number = servis_method.serch_claster_and_number(number_mk)
    servis_method.write_commands(ser, claster, number, 170, 0)  # AA
    servis_method.write_commands(ser, claster, number, 166, 204)  # A6 CC
    servis_method.write_commands(ser, claster, number, 166, 190)  # A6 BE
    temp_cod = read_data_in_mk(claster, number, 2, True)


def read_address(number_mk):
    global ser
    claster, number = servis_method.serch_claster_and_number(number_mk)
    servis_method.write_commands(ser, claster, number, 170, 0)  # AA
    servis_method.write_commands(ser, claster, number, 166, 51)  # A6 33
    address_mk = read_data_in_mk(claster, number, 8)


def pr(number_mk):
    global ser
    claster, number = servis_method.serch_claster_and_number(number_mk)
    servis_method.write_commands(ser, claster, number, 168, 0)  # A8
    sleep_slave(number, 250)
    servis_method.write_commands(ser, claster, number, 165, 5)  # A5 #time.sleep(3)
    servis_method.write_commands(ser, claster, number, 169, 0)  # A9


def read_data_in_mk(claster, number, number_of_bytes, read_flag):
    global ser
    servis_method.write_commands(ser, claster, number, 164, number_of_bytes)  # A4
    start_stack_execution()
    buf = []
    address = []
    temperature = 0
    flag_ok = True
    while flag_ok:
        for i in range(number_of_bytes):
            data = ser.read()
            print(data)
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


# Если приходит Ложь, включить питание, иначе включить
def all_vdd(switcher, first_mk, last_mk):
    global ser
    claster_first, number_first = servis_method.serch_claster_and_number(first_mk)
    claster_last, number_last = servis_method.serch_claster_and_number(last_mk)
    print(claster_first)
    print(claster_last)
    if not switcher:
        commands = 161
        switcher = True
    else:
        commands = 160
        switcher = False
    for iterator in range(claster_first, claster_last + 1):
        servis_method.write_commands(ser, iterator, 10, commands, 0)
    return switcher


def get_number_mk():
    print("write number chip")
    return int(input())


def start_stack_execution():
    servis_method.write_commands(ser, 255, 255, 167, 0)  # A7


def sleep_slave_all(first_mk, last_mk, timer):
    claster_first, number_first = servis_method.serch_claster_and_number(first_mk)
    claster_last, number_last = servis_method.serch_claster_and_number(last_mk)
    time = int(timer / 50)
    for iterator in range(claster_first, claster_last + 1):
        servis_method.write_commands(ser, iterator, 10, 165, time)


def sleep_slave(number_mk, timer):
    claster, number = servis_method.serch_claster_and_number(number_mk)
    time = int(timer / 50)
    servis_method.write_commands(ser, claster, 10, 165, time)


# ??
# ser = servis_method.get_ser_com()
ser = 12
