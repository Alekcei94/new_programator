import time
import servis_method

def read_otp_address(number_mk):
    address_otp_list = [[0, 248],
    [8, 248],
    [16, 248],
    [24, 248],
    [32, 248],
    [40, 248],
    [48, 248],
    [56, 248],
    [64, 248],
    [72, 248],
    [80, 248],
    [88, 248],
    [96, 248],
    [104, 248],
    [112, 248],
    [120, 248],
    [128, 248],
    [136, 248],
    [144, 248],
    [152, 248],
    [160, 248],
    [168, 248],
    [176, 248],
    [184, 248],
    [192, 248],
    [200, 248],
    [208, 248],
    [216, 248],
    [224, 248],
    [232, 248],
    [240, 248],
    [248, 248],
    [0, 249],
    [8, 249],
    [16, 249],
    [24, 249],
    [32, 249],
    [40, 249],
    [48, 249],
    [56, 249],
    [64, 249],
    [72, 249],
    [80, 249],
    [88, 249],
    [96, 249],
    [104, 249],
    [112, 249],
    [120, 249],
    [128, 249],
    [136, 249],
    [144, 249],
    [152, 249],
    [160, 249],
    [168, 249],
    [176, 249],
    [184, 249],
    [192, 249],
    [200, 249],
    [208, 249],
    [216, 249],
    [224, 249],
    [232, 249],
    [240, 249],
    [248, 249],
    [0, 250],
    [8, 250],
    [16, 250],
    [24, 250],
    [32, 250],
    [40, 250],
    [48, 250],
    [56, 250],
    [64, 250],
    [72, 250],
    [80, 250],
    [88, 250],
    [96, 250],
    [104, 250],
    [112, 250],
    [120, 250],
    [128, 250],
    [136, 250],
    [144, 250],
    [152, 250],
    [160, 250],
    [168, 250],
    [176, 250],
    [184, 250],
    [192, 250],
    [200, 250],
    [208, 250],
    [216, 250],
    [224, 250],
    [232, 250],
    [240, 250],
    [248, 250],
    [0, 251],
    [8, 251],
    [16, 251],
    [24, 251],
    [32, 251],
    [40, 251],
    [48, 251],
    [56, 251],
    [64, 251],
    [72, 251],
    [80, 251],
    [88, 251],
    [96, 251],
    [104, 251],
    [112, 251],
    [120, 251],
    [128, 251],
    [136, 251],
    [144, 251],
    [152, 251],
    [160, 251],
    [168, 251],
    [176, 251],
    [184, 251],
    [192, 251],
    [200, 251],
    [208, 251],
    [216, 251],
    [224, 251],
    [232, 251],
    [240, 251],
    [248, 251],
    [0, 252],
    [8, 252],
    [16, 252],
    [24, 252],
    [32, 252],
    [40, 252],
    [48, 252],
    [56, 252],
    [64, 252],
    [72, 252],
    [80, 252],
    [88, 252],
    [96, 252],
    [104, 252],
    [112, 252],
    [120, 252],
    [128, 252],
    [136, 252],
    [144, 252],
    [152, 252],
    [160, 252],
    [168, 252],
    [176, 252],
    [184, 252],
    [192, 252],
    [200, 252],
    [208, 252],
    [216, 252],
    [224, 252],
    [232, 252],
    [240, 252],
    [248, 252],
    [0, 253],
    [8, 253],
    [16, 253],
    [24, 253],
    [32, 253],
    [40, 253],
    [48, 253],
    [56, 253],
    [64, 253],
    [72, 253],
    [80, 253],
    [88, 253],
    [96, 253],
    [104, 253],
    [112, 253],
    [120, 253],
    [128, 253],
    [136, 253],
    [144, 253],
    [152, 253],
    [160, 253],
    [168, 253],
    [176, 253],
    [184, 253],
    [192, 253],
    [200, 253],
    [208, 253],
    [216, 253],
    [224, 253],
    [232, 253],
    [240, 253],
    [248, 253],
    [0, 254],
    [8, 254],
    [16, 254],
    [24, 254],
    [32, 254],
    [40, 254],
    [48, 254],
    [56, 254],
    [64, 254],
    [72, 254],
    [80, 254],
    [88, 254],
    [96, 254],
    [104, 254],
    [112, 254],
    [120, 254],
    [128, 254],
    [136, 254],
    [144, 254],
    [152, 254],
    [160, 254],
    [168, 254],
    [176, 254],
    [184, 254],
    [192, 254],
    [200, 254],
    [208, 254],
    [216, 254],
    [224, 254],
    [232, 254],
    [240, 254],
    [248, 254],
    [0, 255],
    [8, 255],
    [16, 255],
    [24, 255],
    [32, 255],
    [40, 255],
    [48, 255],
    [56, 255],
    [64, 255],
    [72, 255],
    [80, 255],
    [88, 255],
    [96, 255],
    [104, 255],
    [112, 255],
    [120, 255],
    [128, 255],
    [136, 255],
    [144, 255],
    [152, 255],
    [160, 255],
    [168, 255],
    [176, 255],
    [184, 255],
    [192, 255],
    [200, 255],
    [208, 255],
    [216, 255],
    [224, 255],
    [232, 255],
    [240, 255],
    [248, 255]]

    for one_line in address_otp_list:
        global ser
        claster, number = servis_method.serch_claster_and_number(number_mk)
        servis_method.write_commands(ser, claster, number, 170, 0)  # AA
        servis_method.write_commands(ser, claster, number, 228, 0)  # e4
        servis_method.write_commands(ser, claster, number, one_line[0], 0)  #
        servis_method.write_commands(ser, claster, number, one_line[1], 0)  #
        address_otp_cod = read_data_in_mk(claster, number, 2)

def read_temp(number_mk):
    global ser
    claster, number = servis_method.serch_claster_and_number(number_mk)
    servis_method.write_commands(ser, claster, number, 170, 0)  # AA
    servis_method.write_commands(ser, claster, number, 204, 0)  # CC
    servis_method.write_commands(ser, claster, number, 68, 0)  # 44
    servis_method.write_commands(ser, claster, number, 165, 60)  # A5 #time.sleep(3)
    servis_method.write_commands(ser, claster, number, 170, 0)  # AA
    servis_method.write_commands(ser, claster, number, 204, 0)  # CC
    servis_method.write_commands(ser, claster, number, 190, 0)  # BE
    temp_cod = read_data_in_mk(claster, number, 2)

def read_address(number_mk):
    global ser
    claster, number = servis_method.serch_claster_and_number(number_mk)
    servis_method.write_commands(ser, claster, number, 170, 0)
    servis_method.write_commands(ser, claster, number, 51, 0)  # 33
    address_mk = read_data_in_mk(claster, number, 8)

def read_data_in_mk(claster, number, kolvo_byte):
    global ser
    servis_method.write_commands(ser, claster, number, 164, kolvo_byte)  # A4
    buf = []
    t_cod = 0
    temperature = 0
    for i in range(kolvo_byte):
        data = ser.read()
        print(data)
        buf.append(data)
    if len(buf) == 2:
        t_cod = (int.from_bytes(buf[0], "big") | (int.from_bytes(buf[1], "big") << 8))
        print("T_code: " + str(t_cod))
        temperature = float(t_cod * 0.0625)
        print("Temperature: " + str(temperature))
    else:
        print(int.from_bytes(buf, "big"))
    '''lowb = ser.read()
    #lowb = package.hex()
    print(lowb)
    #print(type(lowb))
    highb = ser.read()
    #highb = package.hex()
    print(highb)
    t_cod = (int.from_bytes(lowb, "big") | (int.from_bytes(highb, "big") << 8));
    print("T_code: " + str(t_cod))
    temperature = float(t_cod * 0.0625)
    print("Temperature: " + str(temperature))'''

    '''if len(package) < 12:
        print(package.hex())
        servis_method.write_commands(ser, claster, number, 164)
        package = ser.readlines()
        print(package)'''
    # print("READ COD TEST: " + package)
    return temperature

def vdd(number_mk, switcher):
    global ser
    if switcher == "on":
        commands = 161
    elif switcher == "off":
        commands = 160
    else:
        # Need print exeption
        print("Error command vdd " + switcher)
        return
    claster, number = servis_method.serch_claster_and_number(number_mk)
    # print(claster)
    # print(number)
    # print(commands)
    servis_method.write_commands(ser, claster, number, commands, 0)

def timedelay(number_mk):
    global ser
    commands = 182
    claster, number = servis_method.serch_claster_and_number(number_mk)
    servis_method.write_commands(ser, claster, number, commands, 0)

def get_number_mk():
    print("write number chip")
    return int(input())

# ??
ser = servis_method.get_ser_com()
while True:
    print("1 - read temp cod;")
    print("2 - read address;")
    print("3 - VDD on")
    print("4 - VDD off")
    print("enter commands:")
    commands = str(input())
    if commands == "1":
        number_mk = get_number_mk()
        read_temp(number_mk)
    elif commands == "2":
        number_mk = get_number_mk()
        read_address(number_mk)
    elif commands == "3":
        number_mk = get_number_mk()
        vdd(number_mk, "on")
    elif commands == "4":
        number_mk = get_number_mk()
        vdd(number_mk, "off")
    elif commands == "5":
        for i in range(100):
            print("------> " + str(i))
            for number_mk in range(1, 9):
                # time.sleep(0.5)
                vdd(number_mk, "on")
                # time.sleep(1)
                timedelay(number_mk)

                # time.sleep(0.5)
                # vdd(number_mk, "off")
                # timedelay(1)
        else:
            break
