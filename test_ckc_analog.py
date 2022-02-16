import matplotlib.pyplot as plt
from scipy import interpolate


def minElement(list):
    min = 10000
    for element in list:
        if int(element) < min:
            min = int(element)
    return min


def maxElement(list):
    max = -10000
    for element in list:
        if int(element) > max:
            max = int(element)
    return max


def clc_k_b(x0, y0, x1, y1):
    kIdeal = 18.43
    bIdeal = 1371.67

    k_real = float((y0 - y1) / (x0 - x1))
    b_real = y0 - k_real * x0

    b_ideal = -1 * ((kIdeal / k_real) * b_real) + bIdeal
    b_round = round(float(b_ideal) / 32) * 32

    # print(" old b = " + str(b_ideal) + " __ " + str(b_round))

    b = b_round
    new_k_test = kIdeal / k_real
    k = round(new_k_test, 4)

    return k, b


def form_k(ele):
    x = float(ele)
    binCodeEleK = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    intX = int(x)
    i = 10
    while i < 13:
        y = str(intX % 2)
        binCodeEleK[i] = int(y)
        i = i + 1
        intX = int(intX / 2)
    intY = float(ele) - int(ele)
    i = 9
    while i >= 0:
        z = intY * 2
        binCodeEleK[i] = int(z)
        intY = float(z) - int(z)
        i = i - 1
    string_test = ""
    for i in range(8):
        string_test += str(binCodeEleK[len(binCodeEleK) - 1 - i])

    return int(string_test, 2)


def form_b(ele):
    x = ele
    binCodeEleB = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    i = 0
    if ele < 0:
        binCodeEleB[12] = 1
        x = x * (-1)
    else:
        binCodeEleB[12] = 0
    while x > 0:
        y = str(x % 2)
        if i < 12:
            binCodeEleB[i] = int(y)
            i = i + 1
        else:
            break
        x = int(x / 2)
    string_test = ""
    for i in range(9):
        string_test += str(binCodeEleB[len(binCodeEleB) - 1 - i])
    return int(string_test[1:], 2)


def form_m(ele):
    binCodeEleM = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    x = int(ele)
    i = 0
    while i < 12:
        y = str(x % 2)
        binCodeEleM[i] = int(y)
        i = i + 1
        x = int(x / 2)
    string_test = ""
    for i in range(8):
        string_test += str(binCodeEleM[len(binCodeEleM) - 1 - i])
    return int(string_test, 2)


def interpol(xlist_test, ylist_test):
    interpol = interpolate.interp1d(xlist_test, ylist_test, kind='cubic', fill_value='extrapolate')
    # temperaturerite = xlist_test[0]
    # stop_step = xlist_test[len(xlist_test) - 1]
    temperaturerite = -61.0
    stop_step = 126.0
    step = 0.01
    interval_y = []
    interval_x = []

    while round(temperaturerite, 2) <= stop_step:
        interval_x.append(round(temperaturerite, 2))
        interval_y.append(interpol(temperaturerite))
        temperaturerite = temperaturerite + step
    return interval_x, interval_y


def minimum(x_list_interval_data, y_list_interval_data):
    max_step_number = 8
    xlist_test = []
    ylist_test = []
    xlist_test.append(round(x_list_interval_data[0], 1))
    for i in range(1, max_step_number):
        new_temperature = float(round(xlist_test[i - 1] + (185 / max_step_number), 1))
        xlist_test.append(new_temperature)
    xlist_test.append(round(x_list_interval_data[-1], 1))
    for i in xlist_test:
        test = float(y_list_interval_data[x_list_interval_data.index(i)])
        ylist_test.append(round(test, 3))
    print(xlist_test)
    print(ylist_test)
    return xlist_test, ylist_test


def clc(number_mk, chip):
    file = open('./data/' + str(number_mk) + '.txt', 'r')
    xlist = []
    ylist = []
    dict_temp = {}
    for line in file:
        line.replace("\n", "")
        data = line.split(' ')
        if len(data) > 0:
            xlist.append((data[0]))
            ylist.append(int(data[1]))
    file.close()
    average = []
    for i in range(len(xlist)):
        if '_' in str(xlist[i]):
            continue
        if dict_temp.get(xlist[i]) is None:
            dict_temp[xlist[i]] = [ylist[i]]
        else:
            dict_temp.get(xlist[i]).append(ylist[i])
    new_dict = {}
    xlist = []
    ylist = []
    # xlist.append(-61)
    # ylist.append(62658)
    for key in dict_temp.keys():
        print(key)
        list_temp = dict_temp[key]
        xlist.append(float(key))
        ylist.append(int(sum(list_temp) / len(list_temp)))
        average.append(int(sum(list_temp)/len(list_temp)))
        # new_dict[key] = min(list_temp), int(sum(list_temp)/len(list_temp)), max(list_temp)
        new_dict[key] = int(sum(list_temp)/len(list_temp))
    # print(new_dict)
    # xlist.append(126)
    # ylist.append(64079)
    print(average)
    ylistNew = []
    new_x_list, new_y_list = interpol(xlist, ylist)
    # print(new_y_list[new_x_list.index(125)])
    all_minus = new_y_list[new_x_list.index(-60)] - 100
    # all_minus = 62417
    for i in new_y_list:
        ylistNew.append(round(i - all_minus))
    # print(f'temp -36.6  {ylistNew[new_x_list.index(-36.6)] + all_minus}')
    # print(f'temp -37.6  {ylistNew[new_x_list.index(-37.6)] + all_minus}')
    form_x_list, form_y_list = minimum(new_x_list, ylistNew)

    k_list = []
    b_list = []
    for iterator in range(len(form_x_list) - 1):
        k, b = clc_k_b(form_x_list[iterator], form_y_list[iterator], form_x_list[iterator + 1],
                       form_y_list[iterator + 1])
        k_list.append(k)
        b_list.append(b)

    # print(k_list)
    print(f' b_list {b_list}')

    int_k_list = []
    int_b_list = []
    int_m_list = []
    for iterator in k_list:
        int_k_list.append(form_k(iterator))
    for iterator in b_list:
        int_b_list.append(form_b(iterator))
    # form_y_list = [288, 528, 672, 992, 1200, 1328, 1440]
    # for iterator in range(1, len(form_y_list) - 1):
    #     int_m_list.append(form_m(form_y_list[iterator]))
    for iterator in form_y_list:
        int_m_list.append(form_m(iterator))
    # for iterator in form_y_list:
    #     int_m_list.append(int(iterator/16))
    # print(int_k_list)
    # print(int_b_list)
    # print(int_m_list)
    # int_k_list =  [40, 49, 58, 64, 80, 101, 125, 148]
    # int_b_list = [9, 4, 5, 13, 44, 93, 155, 220]

    step = 0.1

    test_x = []
    test_y = []

    tem = -60
    real_y = []
    list_error = [0,0,0,0,0,0,0,0]
    size_list = [0,0,0,0,0,0,0,0]
    while tem <= 125:
        x = int(ylistNew[new_x_list.index(tem)])
        z = 1
        for iterator_list in range(len(int_m_list) - 1):
            if x >= (int_m_list[iterator_list] << 4) and x < (int_m_list[iterator_list + 1] << 4):
                k = int_k_list[iterator_list]
                b = int_b_list[iterator_list]
                if b_list[iterator_list] < 0:
                    z = -1
                kod = x * k
                new_kod = (kod >> 5) + z * (b << 4)
                real_kod = 18.43 * tem + 1371.67
                list_error[iterator_list] =  list_error[iterator_list] + (new_kod - real_kod)
                size_list[iterator_list] = size_list[iterator_list] + 1
                break
        # if new_kod - real_kod > 8:
        #         int_b_list[4] = int_b_list[4] + z * (-1)
        #         b_list[4] = b_list[4] + z * (-1) * 16
        #         continue
        #     elif new_kod - real_kod < -8:
        #         int_b_list[4] = int_b_list[4] + z
        #         b_list[4] = b_list[4] + z * 16
        #         continue
        test_y.append(new_kod)
        real_y.append(real_kod)
        test_x.append(tem)
        tem = round((tem + step), 2)
    list_error = [list_error[i]/size_list[i] for i in range(len(list_error))]
    print(f'list_error {list_error}')

    Z1 = ""
    for i in range(len(b_list)):
        if b_list[7 - i] >= 0:
            Z1 += "0"
        else:
            Z1 += "1"

    binCodeEleOM = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    x = int(all_minus) # -64 10micros
    i = 0
    while i < 16:
        y = str(x % 2)
        binCodeEleOM[i] = str(int(y))
        i = i + 1
        x = int(x / 2)

    OM1 = binCodeEleOM[:8]
    OM2 = binCodeEleOM[8:]

    print("Z " + str(int(Z1, 2)))
    print("B " + str(int_b_list))
    print("K " + str(int_k_list))
    print("M " + str(int_m_list))
    print("OM1 " + str(int(str(''.join(OM1))[::-1], 2)))
    print("OM2 " + str(int(str(''.join(OM2))[::-1], 2)))
    print(all_minus)

    # setattr(chip, "m_list", int_m_list)
    # setattr(chip, "b_list", int_b_list)
    # setattr(chip, "k_list", int_k_list)
    # setattr(chip, "om1", int(str(''.join(OM1))[::-1], 2))
    # setattr(chip, "om2", int(str(''.join(OM2))[::-1], 2))
    # setattr(chip, "z", int(Z1, 2))


    plt.axis([minElement(test_x) - 5, maxElement(test_x) + 5, minElement(test_y) - 5, maxElement(test_y) + 5])
    plt.plot(test_x, test_y, color='blue')
    # plt.plot(test_x, real_temp, color='red')
    plt.plot(test_x, real_y, color='red')
    plt.show()
    return int_k_list, int_b_list, int_m_list, int(Z1, 2)
