import os.path

class Chip:
    list_mk = []

    def __init__(self, number, type):
        self.number = number
        if type == 10:
            mk = mk_10(number)
        elif type == 11:
            mk = mk_11(number)
        elif type == 12:
            mk = mk_12(number)
        elif type == 13:
            mk = mk_13(number)

class mk_10:
    number = 0
    type = 0

    def __init__(self, number):
        self.number = number

    def update_file(self):
        if os.path.exists("../microchip_life/" + str(self.number) + ".txt"):
            print()
            # TODO чтение из файла данных и обновление данных в объекте.

class mk_11:
    def __init__(self, number):
        print()

class mk_12:
    def __init__(self, number):
        print()

class mk_13:
    number = 0
    address = []
    k_list = []
    b_list = []
    m_list = []
    om1 = 0
    om2 = 0
    delete = 0
    z1 = 0
    z2 = 0
    type = 0
    interface = 0

    def __init__(self, number):
        self.number = number
