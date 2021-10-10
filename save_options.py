import os
import shutil
from datetime import datetime


class SaveOption:
    first_mk = 1  # Номер первой микросхемы
    last_mk = 3  # Номер последней микросхемы
    voltage_state = False  # Сосотояние наличиние питания на мк Ложь - нету, Истина - есть.
    type_mk = 1

    @staticmethod
    def main_save_archive():
        if check_click("Сохранить все данные в архив и удалить файлы в текущих папках?"):
            now = datetime.datetime.now()
            form_path = str(now.day) + "_" + str(now.month) + "_" + str(now.year)
            try:
                os.mkdir("../archive/" + form_path)
            except:
                print("Создать директорию не удалось")
            path_data_archive = "../archive/" + form_path + "/data/"
            path_address_archive = "../archive/" + form_path + "/address/"
            path_finally_test_archive = "../archive/" + form_path + "/finally_test/"
            try:
                os.mkdir(path_data_archive)
                os.mkdir(path_address_archive)
                os.mkdir(path_finally_test_archive)
            except:
                print("Создать директорию не удалось")

            list_file_data = os.listdir("../data/")
            for i in list_file_data:
                shutil.copyfile("../data/" + i, path_data_archive + i)
                os.remove("../data/" + i)
            list_file_address = os.listdir("../address/")
            for i in list_file_address:
                shutil.copyfile("../address/" + i, path_address_archive + i)
                os.remove("../address/" + i)
            list_file_finally_test = os.listdir("../finally_test/")
            for i in list_file_finally_test:
                shutil.copyfile("../finally_test/" + i, path_finally_test_archive + i)
                os.remove("../finally_test/" + i)

    # CHECK LINE AND SAVE IN FILE
    @staticmethod
    def check_save_line(text):
        if '\n' in text:
            text = text.split('\n')[0]
        if len(text) == 0:
            return "0"
        return text

    @staticmethod
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
    @staticmethod
    def save_file_options(options_windows, number_serii, number_part, number_com_por_microchip, number_start_chip,
                          number_finish_chip,
                          number_com_port_mit, number_start_sensor, number_finish_sensor, variable_source,
                          temperature_termostrim):
        global path
        file_save = open(path, 'w')
        if number_serii == '':
            number_serii = 0
        file_save.write(SaveOption.check_save_line(number_com_por_microchip) + '\n' + SaveOption.check_save_line(
            number_start_chip) + '\n'
                        + SaveOption.check_save_line(number_finish_chip) + '\n' + SaveOption.check_save_line(
            number_com_port_mit) + '\n'
                        + SaveOption.check_save_line(number_start_sensor) + '\n' + SaveOption.check_save_line(
            number_finish_sensor) + '\n'
                        + SaveOption.check_save_line(number_part) + '\n' + SaveOption.check_save_line(
            str(int(number_serii) + 1)) + '\n'
                        + SaveOption.check_save_line(variable_source) + '\n' + SaveOption.check_save_line(
            temperature_termostrim))
        options_windows.destroy()
        file_save.close()

    @staticmethod
    def get_com_port_MIT():
        global path
        if os.path.exists(path):
            file_config = open(path, 'r')
            iterator = 0
            for data in file_config:
                if iterator == 3:
                    com_port_data = int(data)
                iterator += 1
            file_config.close()
            return com_port_data
        else:
            return 0

path = "../configuration/save_config.txt"  # FILE SAVE CONFIG