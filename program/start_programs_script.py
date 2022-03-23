import sys
import time
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMessageBox

import program.logger as logger
import program.servis_method as servis_method
import program.save_options as save_options
import program.other.other_functions as other_functions
import program.other.other_devices as other_devices
import program.other.mit as mit
import program.basic_commands_onewire as basic_commands_onewire


# class ConfigurationWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super(ConfigurationWindow, self).__init__()
#         uic.loadUi('./ui/Setting.ui', self)
#         self.show()


class Commands_Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Commands_Window, self).__init__()
        uic.loadUi('./ui/commands_OneWire_New.ui', self)
        self.show()

        # 1 column
        self.vddButton.clicked.connect(self.workVdd)
        # self.newPartButton.clicked.connect(self.)
        self.addArchiveButton.clicked.connect(self.saveArchive)

        # 2 column
        self.readTempButton.clicked.connect(self.readTemp)
        self.readAddressButton.clicked.connect(self.readID)
        self.readOTPButton.clicked.connect(self.readMem)

        # 3 column
        self.startWorkButton.clicked.connect(self.presetting)
        self.writeKAndBButton.clicked.connect(self.writeMem)
        self.writeENButton.clicked.connect(self.writeEN)
        # self.write3VButton.clicked.connect(self.write3V) #Проверить!

        # main
        self.startButton.clicked.connect(self.startRead)

    # Реализация данного метода есть во всех классах типов микросхем. В случае изменения включения питания переделать.
    def workVdd(self):
        print("\nПроизводится управление питанием, ожидайте.")
        if not servis_method.all_vdd(save_options.getInstance()):
            print("Не удалось выполнить настройку питания. Проверьте источник напряжения.")
        else:
            if getattr(save_options.getInstance(), "voltage_state"):
                self.vddButton.setStyleSheet('QPushButton {background-color: #22ff13;}')
                print("\nПитание включено.")
            else:
                self.vddButton.setStyleSheet('QPushButton {background-color: #ff5a0e;}')
                print("\nПитание выключено.")

    # Чтение температураного кода. Формат вывода - (KOD : TEMP)
    def readTemp(self):
        list_temp = []
        if not other_functions.power_check(save_options.getInstance()):
            self.print_message_error("Питание микроконтролера отключено. \nПожалуйста включите питание")
            return
        try:
            logger.write_log("Чтение температурного кода.", 0)
            list_mk = getattr(save_options.getInstance(), 'list_mk')
            for iterator_mk in list_mk:
                basic_commands_onewire.form_temp_cod_not_active(iterator_mk.number_slot)
                logger.write_log(f"Формирование температурного кода в микросхеме {iterator_mk.number_slot}", 0)
            # TODO тут проблема, каждая мк имеет свое время преобразования т.кода
            time.sleep(0.5)
            for iterator_mk in list_mk:
                temp_cod = iterator_mk.type_chip.readTemp()
                list_temp.append(temp_cod)
            print(list_temp)
        except:
            logger.write_log("Произошла ошибка в чтении температурного кода.", 0)

    # Чтеине памяти микросхемы. Формат вывода - (ADDRESS : DATA, .....) В виде листа.
    def readMem(self):
        if not other_functions.power_check(save_options.getInstance()):
            self.print_message_error("Питание микроконтролера отключено. \nПожалуйста включите питание")
            return
        try:
            logger.write_log("Чтение памяти микросхем", 0)
            list_mk = getattr(save_options.getInstance(), 'list_mk')
            for iterator_mk in list_mk:
                iterator_mk.type_chip.readMem(iterator_mk.number_slot)
        except:
            logger.write_log("Произошла ошибка в чтении памяти микросхем", 0)

    # Чтение адреса микросхемы. Не все мк имеют адрес.
    def readID(self):
        if not other_functions.power_check(save_options.getInstance()):
            self.print_message_error("Питание микроконтролера отключено. \nПожалуйста включите питание")
            return
        try:
            logger.write_log("Чтение адреса микросхем", 0)
            list_mk = getattr(save_options.getInstance(), 'list_mk')
            for iterator_mk in list_mk:
                iterator_mk.type_chip.readID(iterator_mk.number_slot)
            print("Конец записи функции чтения адреса.")
        except:
            logger.write_log("Произошла ошибка в чтении адреса микросхем", 0)

    # Запись бита перключения работы мк. В некоторых микросхемах записываются дополительные функцианальные биты.
    def writeEN(self):
        try:
            if not other_functions.power_check(save_options.getInstance()):
                self.print_message_error("Питание микроконтролера отключено. \nПожалуйста включите питание")
                return
            if not self.action_check():
                return
            logger.write_log("Запись EN", 0)
            list_mk = getattr(save_options.getInstance(), 'list_mk')
            for iterator_mk in list_mk:
                if other_functions.smart_mode_check(save_options.getInstance()):
                    if not iterator_mk.writeMem:
                        self.print_message_error(f"Микросхема под номером {iterator_mk.number_slot} не может "
                                                 f"выполнить данную функцию, \nтак как не выолнены предидущие "
                                                 f"итерации")
                        return
            for iterator_mk in list_mk:
                iterator_mk.type_chip.writeEN(iterator_mk.number_slot)
                iterator_mk.writeEN = True
                iterator_mk.dump()
            logger.write_log("Конец функции записи EN", 0)
        except:
            self.print_message_error(f"Запись EN не выполенно")
            logger.write_log("Запись EN не выполенно", 0)

    # Запись памяти мк. В некоторых мк записывается больше информации.
    # TODO надо додумать для паралельного программирования. Возможно, стоит добавить многопоточку, для расчета
    def writeMem(self):
        if not other_functions.power_check(save_options.getInstance()):
            self.print_message_error("Питание микроконтролера отключено. \nПожалуйста включите питание")
            return
        if not self.action_check():
            return
        logger.write_log("Запись памяти", 0)
        list_mk = getattr(save_options.getInstance(), 'list_mk')
        for iterator_mk in list_mk:
            if other_functions.smart_mode_check(save_options.getInstance()):
                if not iterator_mk.startRead:
                    self.print_message_error(f"Микросхема под номером {iterator_mk.number_slot} не может "
                                             f"выполнить данную функцию, \nтак как не выолнены предидущие "
                                             f"итерации")
                    return

        for iterator_mk in list_mk:
            iterator_mk.type_chip.writeMem(iterator_mk)
            iterator_mk.writeMem = True
            iterator_mk.dump()
        logger.write_log("Конец записи данных в микросхемы.", 0)

    # Запуск измерения микросхем для последующей настройки. Происходит формирование файлов вида - (TEMP DATA).
    # Для некоторых микросхем может быть изменено.
    def startRead(self):
        if not other_functions.power_check(save_options.getInstance()):
            self.print_message_error("Питание микроконтролера отключено. \nПожалуйста включите питание")
            return
        logger.write_log("Старт измерений", 0)
        list_mk = getattr(save_options.getInstance(), 'list_mk')
        for iterator_mk in list_mk:
            if other_functions.smart_mode_check(save_options.getInstance()):
                if not iterator_mk.presetting:
                    self.print_message_error(f"Микросхема под номером {iterator_mk.number_slot} не может "
                                             f"выполнить данную функцию, \nтак как не выолнены предидущие "
                                             f"итерации")
                    return
        list_temp_spec = getattr(save_options.getInstance(), 'list_temperature')
        logger.write_log(f"Список температур {list_temp_spec}", 0)
        for temp_spec in list_temp_spec:
            other_devices.work_spec(temp_spec)
            mit.sleep_in_time(save_options.getInstance(), temp_spec)
            for i in range(2):
                print(f'Осталось {20 - i * 10} минут, температура {temp_spec}')
                time.sleep(600)
            # TODO тут надо как то сделать оп другому. так очень долго
            for iterator_mk in list_mk:
                iterator_mk.type_chip.read_temp_and_write_in_file(iterator_mk.number_slot)
                iterator_mk.dump()
            logger.write_log("", 0)
        logger.write_log("Конец измерений", 0)
        for iterator_mk in list_mk:
            iterator_mk.startRead = True
            iterator_mk.dump()

    # Перевести микросхему на 3 вольта. Данная функция может быить применена и для других действий. Смотрите описание.
    # TODO данная функция отключена
    def write3V(self):
        # if not other_functions.power_check(save_options.getInstance()):
        #     self.print_message_error("Питание микроконтролера отключено. \nПожалуйста включите питание")
        #     return
        # self.chip_13.write3V()
        self.print_message_error("Данная функция не работает, обратитесь в отдел разработки ПО.")

    # Добавление всех данных по настройке микросхем в архив. Данный метод реализован в каждом классе.
    # При необходимости можно переделать
    def saveArchive(self):
        other_functions.main_save_archive("13")

    # Предварительная настройка микросхем. Для каждого типа микросхем выполняется набор своих действий.
    # Смотрите описание для каждой микросхемы.
    def presetting(self):
        try:
            if not other_functions.power_check(save_options.getInstance()):
                self.print_message_error("Питание микроконтролера отключено. \nПожалуйста включите питание")
                return
            if not self.action_check():
                return
            logger.write_log("Предварительная настройка", 0)
            list_mk = getattr(save_options.getInstance(), 'list_mk')
            for iterator_mk in list_mk:
                print(f'микросхема {iterator_mk.number_slot}')
                iterator_mk.type_chip.presetting(iterator_mk.number_slot)
                iterator_mk.presetting = True
                iterator_mk.dump()
        except:
            logger.write_log("Предварительная настройка не выполена", 0)
            self.print_message_error("Предварительная настройка не выполена")

    # Работа с новой партией. Пока что не реализована совсем.
    # def work_new_part(self):
    #     return

    def action_check(self):
        message = 'Подтвердите действие'
        reply = QtWidgets.QMessageBox.question(self, 'Уведомление', message,
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            return True
        else:
            return False

    def print_message_error(self, text):
        QMessageBox.about(self, "Внимение", text)


# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         uic.loadUi('./ui/Main.ui', self)
#         self.setWindowTitle('MainWindow')
#         type_mk = getattr(saveOption, "type_mk")
#
#         self.comands.clicked.connect(self.show_CommandsWindow_OneWire_New)
#         # self.options.clicked.connect(self.show_ConfigurationWindow)
#
#     # def show_ConfigurationWindow(self):
#     #     self.w1 = ConfigurationWindow()
#     #     self.w1.show()
#
#     # новый Аналог
#     def show_CommandsWindow_OneWire_Analog(self):
#         self.w1 = Commands_Window_OneWire_New_Analog()
#         self.w1.show()


voltage_state = False
logger.write_log("\nЗапуск программы\n---------------", 0)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # w = MainWindow()
    w = Commands_Window()
    w.show()
    # w.show_CommandsWindow()
    sys.exit(app.exec_())
