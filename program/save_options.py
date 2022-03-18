import basic_commands_onewire
import Micros_chip

instance = None


def getInstance():
    global instance
    if instance is None:
        instance = SaveOption()
        instance.form_list_mk_obj()
    return instance


class SaveOption:
    # Сосотояние наличиние питания на мк Ложь - нету, Истина - есть.
    voltage_state = False

    # Режим умного работы программы. 1 - включен, 0 - выключен.
    # Данный режим не позволяет случайно выбрать не то действие.Необходимо строго выполнять последовательность действий.
    smart_operating_mode = 0

    # Лист устарновленных VDD во всех кластерах. 5 - 5 Вольт, 3 - 3.3 вольта.
    list_voltage = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # 1 - OneWire; 2 - SPI: 3 - I2C
    list_interface_mk = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # тип микросхемы. 1 - старый OneWire; 2 - старый SPI; 3 - новый OneWire_10; 4 - новый SPI; 5
    # - новый I2C; 6 - новый OneWire_ANALOG
    list_type_mk = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Лист температур для измерения в SPEC
    list_temperature = []

    # Номера используемого COM порта MIT8
    com_port_mit = 1

    # Лист используемых микросхем
    list_IC = []

    # Список датчиков MIT8
    list_of_sensors_MIT8 = []

    # Путь до файла настроек
    path = "../configuration/save_config.txt"
    ser = 0

    list_mk = []

    def __init__(self):
        self.update()


    def form_list_mk_obj(self):
        for iterator in self.list_IC:
            self.list_mk.append(Micros_chip.Chip(iterator))

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
            elif "IC_list" in line:
                self.list_IC = self.forming_a_list_from_a_string(line.split("|"))
            elif "comMIT" in line:
                self.com_port_mit = int(line.split("|")[1].replace(" ", ""))
            elif "list_of_sensors_MIT8" in line:
                self.list_of_sensors_MIT8 = self.forming_a_list_from_a_string(line.split("|"))
            elif "list_temperature" in line:
                self.list_temperature = []
                for temp in line.split("|")[1].replace(" ", "").split(","):
                    self.list_temperature.append(int(temp))
            elif "smart_operating_mode" in line:
                self.smart_operating_mode = int(line.split("|")[1])
                if self.smart_operating_mode != 0 and self.smart_operating_mode != 1:
                    print(f"Неверно настроен параметр: smart_operating_mode = {self.smart_operating_mode}")
                    exit(0)
        file_setting.close()

    # Преобразует строки типа "IC_list 1, 3-8" в лист типа int вида [1,3,4,5,6,7,8]
    def forming_a_list_from_a_string(self, line):
        list_mk = []
        temp_list_str = line[1]
        temp_list_str.replace(" ", "")
        for number_mk in temp_list_str.split(","):
            if "-" in number_mk:
                for number in range(int(number_mk.split("-")[0]), int(number_mk.split("-")[1]) + 1):
                    list_mk.append(number)
            else:
                list_mk.append(number_mk)
        list_mk = [int(i) for i in list_mk]
        return list_mk
