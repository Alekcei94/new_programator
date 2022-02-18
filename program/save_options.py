import os
import shutil
from datetime import datetime
import basic_commands_onewire

class SaveOption:
    first_mk = 1  # Номер первой микросхемы
    last_mk = 3  # Номер последней микросхемы
    voltage_state = False  # Сосотояние наличиние питания на мк Ложь - нету, Истина - есть.
    type_mk = 1  # тип микросхемы. 1 - старый OneWire; 2 - старый SPI; 3 - новый OneWire_10; 4 - новый SPI; 5 - новый I2C; 6 - новый OneWire_ANALOG
    list_voltage = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    list_interface_mk = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 1 - OneWire; 2 - SPI: 3 - I2C
    list_type_mk = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # тип микросхемы. 1 - старый OneWire; 2 - старый SPI; 3 - новый OneWire_10; 4 - новый SPI; 5 - новый I2C; 6 - новый OneWire_ANALOG
    list_temperature = []
    com_port_mit = 1
    first_mit = 1
    last_mit = 4
    path = "../configuration/save_config.txt"  # FILE SAVE CONFIG
    ser = 0

    __instance = None

    def __init__(self):
        if not SaveOption.__instance:
            self.update()
        else:
            self.getInstance()
            self.update()

    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = Singleton()
        return cls.__instance


    def update(self):
        file_setting = open('../options/setting.txt', 'r')
        self.ser = basic_commands_onewire.get_ser()
        for line in file_setting:
            line = line.replace("\n", "")
            if "*" in line:
                continue
            if ":" in line:
                data_line = line.split(":")
                voltage_interface_type = data_line[1].split("|")
                self.list_voltage[int(data_line[0]) - 1] = int(voltage_interface_type[0])
                self.list_interface_mk[int(data_line[0]) - 1] = int(voltage_interface_type[1])
                self.list_type_mk[int(data_line[0]) - 1] = int(voltage_interface_type[2])
            elif "firstMk" in line:
                self.first_mk = int(line.split(" ")[1])
            elif "lastMk" in line:
                self.last_mk = int(line.split(" ")[1])
            elif "comMIT" in line:
                self.com_port_mit = int(line.split(" ")[1])
            elif "firstMIT" in line:
                self.first_mit = int(line.split(" ")[1])
            elif "lastMIT" in line:
                self.last_mit = int(line.split(" ")[1])
            elif "type_mk" in line:
                self.type_mk = int(line.split(" ")[1])
            elif "list_temperature" in line:
                self.list_type_mk = [int(i) for i in line.split(" ")[1:]]
        file_setting.close()
