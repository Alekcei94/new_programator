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
    list_type_mk = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 1 - OneWire; 2 - SPI: 3 - I2C
    com_port_mit = 1
    first_mit = 1
    last_mit = 4
    path = "../configuration/save_config.txt"  # FILE SAVE CONFIG
    ser = 0

    def __init__(self):
        file_setting = open('./options/setting.txt', 'r')
        self.ser = basic_commands_onewire.get_ser()
        for line in file_setting:
            line = line.replace("\n", "")
            if ":" in line:
                data_line = line.split(":")
                voltage_and_type = data_line[1].split("|")
                self.list_voltage[int(data_line[0]) - 1] = int(voltage_and_type[0])
                self.list_type_mk[int(data_line[0]) - 1] = int(voltage_and_type[1])
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
        file_setting.close()

    # @staticmethod
    # def main_save_archive():
    #     if check_click("Сохранить все данные в архив и удалить файлы в текущих папках?"):
    #         now = datetime.datetime.now()
    #         form_path = str(now.day) + "_" + str(now.month) + "_" + str(now.year)
    #         try:
    #             os.mkdir("../archive/" + form_path)
    #         except:
    #             print("Создать директорию не удалось")
    #         path_data_archive = "../archive/" + form_path + "/data/"
    #         path_address_archive = "../archive/" + form_path + "/address/"
    #         path_finally_test_archive = "../archive/" + form_path + "/finally_test/"
    #         try:
    #             os.mkdir(path_data_archive)
    #             os.mkdir(path_address_archive)
    #             os.mkdir(path_finally_test_archive)
    #         except:
    #             print("Создать директорию не удалось")
    #
    #         list_file_data = os.listdir("../data/")
    #         for i in list_file_data:
    #             shutil.copyfile("../data/" + i, path_data_archive + i)
    #             os.remove("../data/" + i)
    #         list_file_address = os.listdir("../address/")
    #         for i in list_file_address:
    #             shutil.copyfile("../address/" + i, path_address_archive + i)
    #             os.remove("../address/" + i)
    #         list_file_finally_test = os.listdir("../finally_test/")
    #         for i in list_file_finally_test:
    #             shutil.copyfile("../finally_test/" + i, path_finally_test_archive + i)
    #             os.remove("../finally_test/" + i)
    #
    # # CHECK LINE AND SAVE IN FILE
    # @staticmethod
    # def check_save_line(text):
    #     if '\n' in text:
    #         text = text.split('\n')[0]
    #     if len(text) == 0:
    #         return "0"
    #     return text
    #
    # @staticmethod
    # def load_file_options():
    #     global path
    #     data_file = []
    #     if os.path.exists(path):
    #         file_config = open(path, 'r')
    #         for line in file_config:
    #             data_file.append(line)
    #         file_config.close()
    #     if len(data_file) != 10:
    #         for i in range(10):
    #             data_file.append(0)
    #     return data_file
    #
    # # SAVE CONFIGURATION
    # @staticmethod
    # def save_file_options(options_windows, number_serii, number_part, number_com_por_microchip, number_start_chip,
    #                       number_finish_chip,
    #                       number_com_port_mit, number_start_sensor, number_finish_sensor, variable_source,
    #                       temperature_termostrim):
    #     global path
    #     file_save = open(path, 'w')
    #     if number_serii == '':
    #         number_serii = 0
    #     file_save.write(SaveOption.check_save_line(number_com_por_microchip) + '\n' + SaveOption.check_save_line(
    #         number_start_chip) + '\n'
    #                     + SaveOption.check_save_line(number_finish_chip) + '\n' + SaveOption.check_save_line(
    #         number_com_port_mit) + '\n'
    #                     + SaveOption.check_save_line(number_start_sensor) + '\n' + SaveOption.check_save_line(
    #         number_finish_sensor) + '\n'
    #                     + SaveOption.check_save_line(number_part) + '\n' + SaveOption.check_save_line(
    #         str(int(number_serii) + 1)) + '\n'
    #                     + SaveOption.check_save_line(variable_source) + '\n' + SaveOption.check_save_line(
    #         temperature_termostrim))
    #     options_windows.destroy()
    #     file_save.close()
    #
    # @staticmethod
    # def get_com_port_MIT():
    #     global path
    #     if os.path.exists(path):
    #         file_config = open(path, 'r')
    #         iterator = 0
    #         for data in file_config:
    #             if iterator == 3:
    #                 com_port_data = int(data)
    #             iterator += 1
    #         file_config.close()
    #         return com_port_data
    #     else:
    #         return 0
