import servis_method
import micros_old.program_logic as program_logic
import save_options
import time


#
# def queue_test_teams(number_mk):
#     claster, number = servis_method.search_claster_and_number(number_mk)
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


# формирование температурного кода
def form_temp_cod_not_active(number_mk):
    global ser
    claster, number = servis_method.search_claster_and_number(number_mk)
    servis_method.write_commands(ser, claster, number, 162, 0)  # A2 следующие команды выполняются стеком
    servis_method.write_commands(ser, claster, number, 170, 0)  # AA reset
    servis_method.write_commands(ser, claster, number, 166, 204)  # A6 CC
    servis_method.write_commands(ser, claster, number, 166, 68)  # A6 44
    servis_method.write_commands(ser, claster, number, 42, 0)  # 2A конец записи стека, выполнение


# чтение температурного кода
def read_temp_active(number_mk):
    global ser
    claster, number = servis_method.search_claster_and_number(number_mk)
    servis_method.write_commands(ser, claster, number, 162, 0)  # A2 следующие команды выполняются стеком
    servis_method.write_commands(ser, claster, number, 170, 0)  # AA reset
    servis_method.write_commands(ser, claster, number, 166, 204)  # A6 CC
    servis_method.write_commands(ser, claster, number, 166, 190)  # A6 BE
    servis_method.write_commands(ser, claster, number, 164, 2)  # A4 сообщить slave сколько байт считать надо будет
    servis_method.write_commands(ser, claster, number, 42, 0)  # 2A конец записи стека, выполнение
    temp_cod = servis_method.read_data_in_mk(claster, number, 2, False)


# чтеине ИД адреса микросхемы
def read_address(number_mk):
    global ser
    claster, number = servis_method.search_claster_and_number(number_mk)
    servis_method.write_commands(ser, claster, number, 162, 0)  # A2 следующие команды выполняются стеком
    servis_method.write_commands(ser, claster, number, 170, 0)  # AA reset
    servis_method.write_commands(ser, claster, number, 166, 51)  # A6 33
    servis_method.write_commands(ser, claster, number, 164, 8)  # A4 сообщить slave сколько байт считать надо будет
    servis_method.write_commands(ser, claster, number, 42, 0)  # 2A конец записи стека, выполнение
    address_mk = servis_method.read_data_in_mk(claster, number, 8, True)


# чтение адреса отп одной ячейки
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
    claster, number = servis_method.search_claster_and_number(number_mk)
    servis_method.write_commands(ser, claster, number, 170, 0)  # AA
    servis_method.write_commands(ser, claster, number, 166, 228)  # A6 e4
    servis_method.write_commands(ser, claster, number, 166, address_otp_list[number_OTP_mem][0])  # A6 data_0
    servis_method.write_commands(ser, claster, number, 166, address_otp_list[number_OTP_mem][1])  # A6 data_1
    address_otp_cod = servis_method.read_data_in_mk(claster, number, 2, True)
    return address_otp_cod


# Записать REZ
def write_REZ(number_mk):
    global ser
    claster, number = servis_method.search_claster_and_number(number_mk)
    servis_method.write_commands(ser, claster, number, 170, 0)  # AA
    # команда страта записи REZ
    servis_method.write_commands(ser, claster, number, 166, 120)  # A6 78
    servis_method.write_commands(ser, claster, number, 166,
                                 program_logic.write_REZ('''вставить сюда бинарный код'''))  # A6 бит записи REZ


# Записаь ИД микросхемы (основного адреса)
def write_ID(number_mk):
    global ser
    claster, number = servis_method.search_claster_and_number(number_mk)
    servis_method.write_commands(ser, claster, number, 170, 0)  # AA
    # команда страта записи ИД
    servis_method.write_commands(ser, claster, number, 166, 56)  # A6 38 проверить поссылку
    id = program_logic.set_address(number_mk)
    servis_method.write_commands(ser, claster, number, 166, id[0])  # A6 data_0
    servis_method.write_commands(ser, claster, number, 166, id[1])  # A6 data_1
    servis_method.write_commands(ser, claster, number, 166, id[2])  # A6 data_2
    servis_method.write_commands(ser, claster, number, 166, id[3])  # A6 data_3
    servis_method.write_commands(ser, claster, number, 166, id[4])  # A6 data_4
    servis_method.write_commands(ser, claster, number, 166, id[5])  # A6 data_5
    servis_method.write_commands(ser, claster, number, 166, id[6])  # A6 data_6
    servis_method.write_commands(ser, claster, number, 166, id[7])  # A6 data_7


# Запись памяти ОТП
def write_OTP(number_mk):
    global ser
    claster, number = servis_method.search_claster_and_number(number_mk)
    servis_method.write_commands(ser, claster, number, 170, 0)  # AA
    servis_method.write_commands(ser, claster, number, 166, 0)  # A6 не настроенна команда


# Запись коэффициентов К и В
def write_mem_K_and_B(number_mk):
    global ser
    claster, number = servis_method.search_claster_and_number(number_mk)
    servis_method.write_commands(ser, claster, number, 170, 0)  # AA
    # Запись К и В
    servis_method.write_commands(ser, claster, number, 166, 56)  # A6 38 проверить поссылку


# записать EN2 (переводит работу микросхему на память ОТП)
def write_EN2(number_mk):
    global ser
    claster, number = servis_method.search_claster_and_number(number_mk)
    servis_method.write_commands(ser, claster, number, 170, 0)  # AA
    servis_method.write_commands(ser, claster, number, 166, 0)  # A6 не настроенна команда


# Запись памяти в новый микрос OneWire интерфейсом
# Важно number_mem берется из карты памяти по формуле номер строки - 1.
def write_mem_new_micros_OneWire(number_mk, number_mem, data):
    global ser
    claster, number = servis_method.search_claster_and_number(number_mk)
    servis_method.write_commands(ser, claster, number, 162, 0)  # A2 следующие команды выполняются стеком
    servis_method.write_commands(ser, claster, number, 170, 0)  # AA reset
    servis_method.write_commands(ser, claster, number, 166, 24)  # A6 24(0x18) Команда записи памяти
    servis_method.write_commands(ser, claster, number, 166, number_mem)  # A6 addr
    servis_method.write_commands(ser, claster, number, 166, data)  # A6 data
    servis_method.write_commands(ser, claster, number, 90, 4)  # 5A задержка в 80мкС
    servis_method.pr(ser, claster, number)
    servis_method.write_commands(ser, claster, number, 42, 0)  # 2A конец записи стека, выполнение


def get_ser():
    global ser
    return ser


# Данное место необходимо переделать
# ser = servis_method.get_ser_com()
ser = 12
