import program.logger as logger


class SPI_Chip:
    type = 11

    # def workVdd(self):
    #     print("Данная функция пока недоступна")

    def readTemp(self, iterator_mk):
        logger.write_log("Чтение температурного кода в микросхеме " + str(iterator_mk) + " микросхема: "
                         + str(iterator_mk) + "; Данная функция пока недоступна ", 0)
        return "Микросхема: " + str(iterator_mk) + "; Данная функция пока недоступна "

    def readMem(self, iterator_mk):
        logger.write_log("Чтение памяти в микросхеме: " + str(iterator_mk) + "; Данная функция пока не доступна", 0)
        print(f"Чтение памяти в микросхеме: {iterator_mk}; Данная функция пока не доступна")

    def readID(self, iterator_mk):
        logger.write_log("Чтение адреса в микросхеме: " + str(iterator_mk) + "; Данная функция пока не доступна", 0)
        # print(f"Чтение адреса в микросхеме {iterator_mk} Данная функция пока не доступна")
        return "Чтение адреса в микросхеме: " + str(iterator_mk) + "; Данная функция пока не доступна"

    def writeEN(self, iterator_mk):
        logger.write_log("Запись EN в микросхеме: " + str(iterator_mk) + "; Данная функция пока не доступна", 0)
        print(f"Запись EN в микросхеме: {iterator_mk}; Данная функция пока не доступна")

    def writeMem(self, iterator_mk):
        logger.write_log("Запись памяти в микросхеме: " + str(iterator_mk) + "; Данная функция пока не доступна", 0)
        print(f"Запись памяти в микросхеме: {iterator_mk}; Данная функция пока не доступна")

    def startRead(self, iterator_mk):
        logger.write_log("Данная функция пока не доступна", 0)
        print(f"Данная функция пока не доступна")

    def write3V(self, iterator_mk):
        logger.write_log("Перевод микросхемы: " + str(iterator_mk) + " на напряжение питания 3V", 0)
        print(f"Перевод микросхемы: {iterator_mk} на напряжение питания 3V")

    def presetting(self, iterator_mk):
        logger.write_log("Предварительная настройка микросхемы: " + str(iterator_mk), 0)
        print(f"Предварительная настройка микросхемы: {iterator_mk}")

    def read_temp_and_write_in_file(self, iterator_mk):
        print("Не работает")