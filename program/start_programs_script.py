import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication

import logger
import servis_method
import save_options
import Сhip_Сlasses.Analog_Chip as Analog_Chip
import other.other_functions as other_functions


# class ConfigurationWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super(ConfigurationWindow, self).__init__()
#         uic.loadUi('./ui/Setting.ui', self)
#         self.show()


class Commands_Window(QtWidgets.QMainWindow):
    analog_chip = Analog_Chip.Analog_Chip()


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
        print('\n' + "Производиться управлене питанием, ожидайте.")
        if not servis_method.all_vdd(save_options.SaveOption()):
            print('\n' + "Не удалось выполнить настройку питания. Проверте источник напряжения.")
        else:
            if getattr(save_options.SaveOption(), "voltage_state"):
                self.vddButton.setStyleSheet('QPushButton {background-color: #22ff13;}')
                print('\n' + "Питание включено.")
            else:
                self.vddButton.setStyleSheet('QPushButton {background-color: #ff5a0e;}')
                print('\n' + "Питание выключено.")

    # Чтение температураного кода. Формат вывода - (KOD : TEMP)
    def readTemp(self):
        self.analog_chip.readTemp()

    # Чтеине памяти микросхемы. Формат вывода - (ADDRESS : DATA, .....) В виде листа.
    def readMem(self):
        self.analog_chip.readMem()

    # Чтение адреса микросхемы. Не все мк имеют адрес.
    def readID(self):
        self.analog_chip.readID()

    # Запись бита перключения работы мк. В некоторых микросхемах записываются дополительные функцианальные биты.
    def writeEN(self):
        self.analog_chip.writeEN()

    # Запись памяти мк. В некоторых мк записывается больше информации.
    def writeMem(self):
        self.analog_chip.writeMem()

    # Запуск измерения микросхем для последующей настройки. Происходит формирование файлов вида - (TEMP DATA).
    # Для некоторых микросхем может быть изменено.
    def startRead(self):
        self.analog_chip.startRead()

    # Перевести микросхему на 3 вольта. Данная функция может быить применена и для других действий. Смотрите описание.
    # TODO данная функция отключена
    def write3V(self):
        self.analog_chip.write3V()

    # Добавление всех данных по настройке микросхем в архив. Данный метод реализован в каждом классе.
    # При необходимости можно переделать
    def saveArchive(self):
        other_functions.main_save_archive("13")

    # Предварительная настройка микросхем. Для каждого типа микросхем выполняется набор своих действий.
    # Смотрите описание для каждой микросхемы.
    def presetting(self):
        self.analog_chip.presetting()

    # Работа с новой партией. Пока что не реализована совсем.
    # def work_new_part(self):
    #     return

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
logger.write_log('\n' + "Запуск программы" + '\n' + "---------------", 0)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # w = MainWindow()
    w = Commands_Window()
    w.show()
    # w.show_CommandsWindow()
    sys.exit(app.exec_())
