import other.mit as mit
import other.other_devices as other_devices
import servis_method

# Метод ожидания выхода SPEC в нужную температуру.
# TODO тут ли метод?
def sleep_in_time(saveOption, temp):
    while True:
        flag = True
        temp_mit = mit.main_function_MIT(saveOption)
        print(f'Температура на датчиках МИТ {temp_mit}, температура на SPEC {temp}')
        for i in temp_mit:
            if not (temp - 2) <= i <= (temp + 2):
                flag = False
                other_devices.work_spec(temp)
                break
        if flag:
            break

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
        print("Питание микроконтролера отклюено. Включить питание?")
        if action_check():
            servis_method.all_vdd(save_object)
            return True
        else:
            print("Не удалось включить питание микроконтролера")
            return False
    return True

# нахождение среднеарфмитиечкого значения листа, за исключением элемента на месте iterator.
def sum_list(iterator, y):
    new_x = list(y)
    new_x.pop(iterator)
    return sum(new_x) / len(new_x)
