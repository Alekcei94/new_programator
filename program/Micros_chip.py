import os.path
import ast

import save_options
import logger
import Сhip_Сlasses.Analog_Chip as Analog_Chip
import Сhip_Сlasses.I2C_Chip as I2C_Chip
import Сhip_Сlasses.OneWire_Chip as OneWire_Chip
import Сhip_Сlasses.SPI_Chip as SPI_Chip


class Chip:
    number_slot = None
    type_chip = None
    data = {}

    presetting = False
    startRead = False
    writeMem = False
    write3V = False
    writeEN = False

    def __init__(self, number):
        if not self.check_file(number):
            self.number_slot = number
            self.type_chip = self.choice_of_object_of_work(number)
        else:
            self.load(number)

    def adding_dimension_data_to_spec(self, temp, cod):
        self.data[temp] = cod

    def load(self, number):
        file_data = open("../microchip_life/" + str(number) + ".txt")
        for line in file_data:
            if "data" in line:
                self.data = ast.literal_eval(line.split(" ")[1])
            elif "number_slot" in line:
                self.number_slot = int(line.split(" ")[1])
            elif "type_chip" in line:
                if int(line.split(" ")[1]) == 13:
                    self.type_chip = Analog_Chip.Analog_Chip()
                elif int(line.split(" ")[1]) == 12:
                    self.type_chip = I2C_Chip.I2C_Chip()
                elif int(line.split(" ")[1]) == 11:
                    self.type_chip = SPI_Chip.SPI_Chip()
                elif int(line.split(" ")[1]) == 10:
                    self.type_chip = OneWire_Chip.OneWire_Chip()
            elif "presetting" in line:
                self.presetting = True
            elif "startRead" in line:
                self.startRead = True
            elif "writeMem" in line:
                self.writeMem = True
            elif "write3V" in line:
                self.write3V = True
            elif "writeEN" in line:
                self.writeEN = True
        file_data.close()

    def dump(self):
        file_data = open("../microchip_life/" + str(self.number_slot) + ".txt", 'w')
        file_data.write(f"number_slot {self.number_slot}\n")
        file_data.write(f"type_chip {self.type_chip.type}\n")
        file_data.write(f"data {self.data}\n")
        if self.presetting: file_data.write("presetting\n")
        if self.startRead: file_data.write("startRead\n")
        if self.writeMem: file_data.write("writeMem\n")
        if self.write3V: file_data.write("write3V\n")
        if self.writeEN: file_data.write("writeEN\n")
        file_data.close()

    def check_file(self, number):
        if os.path.exists("../microchip_life/" + str(number) + ".txt"):
            return True
        return False

    def choice_of_object_of_work(self, iterator_mk):
        list_type = getattr(save_options.getInstance(), 'list_type_mk')
        type_mk = (iterator_mk - 1) // 8
        if list_type[type_mk] == 13:
            return Analog_Chip.Analog_Chip()
        elif list_type[type_mk] == 12:
            return I2C_Chip.I2C_Chip()
        elif list_type[type_mk] == 11:
            return SPI_Chip.SPI_Chip()
        elif list_type[type_mk] == 10:
            return OneWire_Chip.OneWire_Chip()
        print(f"Для микросхемы {iterator_mk} не удалось определить тип. Необходимо перезапустить метод. "
              f"При повторении проблема обратиться в отдлел разработки.")
        logger.write_log("У микросхемы " + str(iterator_mk) + " не удалось определить тип. "
                                                              "Перезапустить метод. При повторении проблема обратиться "
                                                              "в отдлел разработки", 0)
        return None
