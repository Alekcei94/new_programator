class Chip:
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

    def __init__(self, number, type, interface, address, k_list, b_list, m_list, om1, om2, delete, z1, z2):
        self.number = number
        self.type = type
        self.interface = interface
        self.address = address
        self.k_list = k_list
        self.b_list = b_list
        self.m_list = m_list
        self.om1 = om1
        self.om2 = om2
        self.delete = delete
        self.z1 = z1
        self.z2 = z2