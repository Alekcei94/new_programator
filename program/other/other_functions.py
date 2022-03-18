import datetime
import os
import shutil


# Сохранение данных в архив
# version_mk - входные данные версия микросхемы. (10, 11, 12, 13)
def main_save_archive(version_mk):
    now = datetime.datetime.now()
    list_name_dir = ["data", "microchip_life", "logger", "setup_steps"]
    form_path = str(now.day) + "_" + str(now.month) + "_" + str(now.year) + "_" + str(now.hour) + "h"
    try:
        os.mkdir("../archive/" + str(version_mk) + "/" + form_path)
    except:
        print("Создать директорию не удалось " + str(os.getcwd()))
    for name_dir in list_name_dir:
        path_name_dir_archive = "../archive/" + str(version_mk) + "/" + form_path + "/" + name_dir + "/"
        try:
            os.mkdir(path_name_dir_archive)
        except:
            print(f"Создать директорию не удалось {name_dir}")

    for name_dir in list_name_dir:
        list_file_data = os.listdir("../" + name_dir + "/")
        for i in list_file_data:
            shutil.copyfile("../" + name_dir + "/" + i, "../archive/" + str(version_mk) + "/" + form_path + "/" + name_dir + "/" + i)
            os.remove("../" + name_dir + "/" + i)



# Метод подтверждения действий.
def action_check():
    check = input("Подтвердите действие." + "\n")
    if check == "y":
        return True
    print("Отказ выполнения")
    return False


# Метод проверки включенного питания. необходимо передалть. Или не включать из метода питание, или добавить
# изменение цвета кнопки
def power_check(save_object):
    switcher = getattr(save_object, "voltage_state")
    if not switcher:
        print("Питание микроконтролера отклюено. \nПожалуйста включите питание")
        return False
    return True


# Метод проверка включения умного режима работы программы.
def smart_mode_check(save_object):
    switcher = getattr(save_object, "smart_operating_mode")
    if switcher == 1:
        return True
    return False


# нахождение среднеарфмитиечкого значения листа, за исключением элемента на месте iterator.
def sum_list(iterator, y):
    new_x = list(y)
    new_x.pop(iterator)
    return sum(new_x) / len(new_x)


# Проверка в файлах номера микросхемы разрешено ли выполнять функцию с номером.
# 1:Предваритальная настройка
# 2:Измерение
# 3:Память
# 4:3V
# 5:EN и DQ
def read_file_and_check_run_function(number_chip, operation_number):
    path = "../../setup_steps/" + str(number_chip) + ".txt"
    file = open(path)
    if str(operation_number) in file:
        return True
    return False


# Запись в файл сведения о выполнении итерации
# 1:Предваритальная настройка
# 2:Измерение
# 3:Память
# 4:3V
# 5:EN и DQ
def write_file_in_run_function(number_chip, operation_number):
    path = "../../setup_steps/" + str(number_chip) + ".txt"
    file = open(path, 'a')
    file.write(str(operation_number) + '\n')