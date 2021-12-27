import matplotlib.pyplot as plt
from scipy import interpolate

# Analog

def coefficients(number_mk, chip):

    file = open('./data/' + str(number_mk) + '.txt', 'r')
    xlistNew = []
    ylist = []
    for line in file:
        line.replace("\n", "")
        data = line.split(' ')
        if len(data) > 0:
            xlistNew.append(float(data[0]))
            ylist.append(int(data[1]))
    file.close()
    ylistNew = []
    all_minus = ylist[0] - 200 # ERROR
    for i in ylist:
        ylistNew.append(round((i - all_minus) / 1))
    print(xlistNew)
    print(ylistNew)
    calculationOfCoefficients(xlistNew, ylistNew, all_minus, chip)



def form_interval(xlist, x_list_interval_data, y_list_interval_data, i, k):
    x_list_interval_data1 = []
    y_list_interval_data1 = []
    interval_data1 = []
    interval_delete = 0
    start = xlist[i]
    stop = xlist[k]
    test_flag = False
    for f in range(len(x_list_interval_data)):
        interval_delete += 1
        if test_flag == True:
            x_list_interval_data1.append(round(x_list_interval_data[f], 2))
            y_swich = float(y_list_interval_data[f])
            y_list_interval_data1.append(y_swich)  # !!!!!!!!!!
            if round(x_list_interval_data[f], 2) >= stop:
                break
        if round(x_list_interval_data[f], 2) >= round(start, 2):
            test_flag = True
    interval_data1.append(x_list_interval_data1)
    interval_data1.append(y_list_interval_data1)
    interval_data1.append(interval_delete)
    return interval_data1


def minimum(xlist, ylist):
    interval_data = interpol(xlist, ylist)
    x_list_interval_data = interval_data[0]
    y_list_interval_data = interval_data[1]

    max_step_number = 8

    xlist_test = []
    ylist_test = []

    xlist_test.append(round(x_list_interval_data[0], 1))
    for i in range(1, max_step_number):
        new_temperature = round(xlist_test[i - 1] + (185 / max_step_number), 1)
        xlist_test.append(new_temperature)
    xlist_test.append(round(x_list_interval_data[-1], 1))
    for i in xlist_test:
        test = float(y_list_interval_data[x_list_interval_data.index(i)])
        ylist_test.append(test)

    # plt.axis([minElement(xlist)-10, maxElement(xlist)+10, minElement(ylist)-200, maxElement(ylist)+200])
    # plt.plot(xlist_test, ylist_test, color = 'blue')
    # plt.show()

    for i in range(max_step_number):

        print(xlist_test)
        print(ylist_test)
        print("step = " + str(i + 1) + " in " + str(max_step_number))
        interval = form_interval(xlist_test, x_list_interval_data, y_list_interval_data, i, i + 1)

        # del x_list_interval_data[0:interval[2]]
        # del y_list_interval_data[0:interval[2]]

        x_list_interval = interval[0]
        y_list_interval = interval[1]

        y_real = 0
        x_real = 0
        sum_last = 0
        for j in range(len(x_list_interval) - 1):
            k_real = float((ylist_test[i] - ylist_test[i + 1]) / (xlist_test[i] - xlist_test[i + 1]))
            b_real = ylist_test[i + 1] - k_real * xlist_test[i + 1]
            difference = []
            x_list_test = []
            for k in range(len(y_list_interval) - 1):
                x_list_test.append(k)
                kv_sum = abs(x_list_interval[k] * k_real + b_real) - abs(y_list_interval[k])  # Hmmmm  math is not real
                difference.append(pow(kv_sum, 2))
            sum = 0
            for k in difference:
                sum = sum + abs(k)
            if j != 0:
                if (sum / (len(y_list_interval))) < (sum_last / (len(y_list_interval))):
                    y_real = ylist_test[i + 1]
                    x_real = round(xlist_test[i + 1], 1)
                    sum_last = sum
            else:
                sum_last = sum

            ylist_test[i + 1] = y_list_interval[j]
            xlist_test[i + 1] = x_list_interval[j]

        print("--> " + str(sum / (len(y_list_interval) - 1)) + " <--")
        ylist_test[i + 1] = y_real
        xlist_test[i + 1] = x_real

    new_list_y_KOD = []

    new_list_x_test = []
    for i in ylist_test:
        new_list_x_test.append(serch_temp_in_data_list_interpolation(x_list_interval_data, y_list_interval_data,
                                                                     round(float(i) / 16) * 16))
        new_list_y_KOD.append(round(float(i) / 16) * 16)

    print("New X = " + str(xlist_test))
    print("New Y = " + str(new_list_y_KOD))
    print("OLD Y = " + str(ylist_test))
    return xlist_test, new_list_y_KOD


def serch_temp_in_data_list_interpolation(x_list_interval_data, y_list_interval_data, data_y):
    try:
        for i in range(len(y_list_interval_data)):
            if y_list_interval_data[i] > data_y:
                return x_list_interval_data[i - 1]
    except:
        exit("Not work")


def interpol(xlist_test, ylist_test):
    tck = interpolate.splrep(xlist_test, ylist_test)
    temperaturerite = xlist_test[0]
    stop_step = xlist_test[len(xlist_test) - 1]
    step = 0.01
    interval_y = []
    interval_x = []
    interval = []

    while round(temperaturerite, 2) <= stop_step:
        interval_x.append(round(temperaturerite, 2))
        interval_y.append(interpolate.splev(temperaturerite, tck))
        temperaturerite = temperaturerite + step
    interval.append(interval_x)
    interval.append(interval_y)
    return interval


def calculationOfCoefficients(xlist, ylist, all_minus, chip):
    coefB = []
    coefK = []
    kIdeal = 18.43
    bIdeal = 1371.67
    i = 0
    print("\n" + "-------------------------" + "\n" + "RESULT:")

    x_new_list, y_new_list = minimum(xlist, ylist)

    interval_data = interpol(xlist, ylist)
    x_list_interval_data = interval_data[0]
    y_list_interval_data = interval_data[1]

    test_k = []
    test_b = []
    while i < len(x_new_list) - 1:
        k_real = float((y_new_list[i] - y_new_list[i + 1]) / (x_new_list[i] - x_new_list[i + 1]))
        b_real = y_new_list[i] - k_real * x_new_list[i]

        print("b_real in interval " + str(x_new_list[i]) + " : " + str(x_new_list[i + 1]) + " = " + str(b_real))
        print("k_real in interval " + str(x_new_list[i]) + " : " + str(x_new_list[i + 1]) + " = " + str(k_real))

        b_ideal = -1 * ((kIdeal / k_real) * b_real) + bIdeal

        test_k.append(k_real)
        test_b.append(b_real)

        b_round = round(float(b_ideal) / 32) * 32
        print(" old b = " + str(b_ideal) + " __ " + str(b_round))
        coefB.append(b_round)
        new_k_1_test = (kIdeal * x_new_list[i] + bIdeal - b_round) / (k_real * x_new_list[i] + b_real)
        new_k_2_test = (kIdeal * x_new_list[i + 1] + bIdeal - b_round) / (k_real * x_new_list[i + 1] + b_real)
        new_k_test = (new_k_1_test + new_k_2_test) / 2
        coefK.append(round(new_k_test, 4))
        i = i + 1

    # coefB.append(b_ideal)

    sttt_temperature = -60
    step_test = 1
    test_x = []
    test_y = []
    test_temperature_list = []
    # print("ERROR START")
    # for iter_temp in range(len(y_list_interval_data)):
    #     cod_ideal = x_list_interval_data[iter_temp] * (-16) + 2047
    #     if y_list_interval_data[iter_temp] > y_new_list[1]:
    #         cod_mk = y_list_interval_data[iter_temp] * coefK[0] + coefB[0]
    #     elif y_list_interval_data[iter_temp] < y_new_list[1] and y_list_interval_data[iter_temp] > y_new_list[2]:
    #         cod_mk = y_list_interval_data[iter_temp] * coefK[1] + coefB[1]
    #     elif y_list_interval_data[iter_temp] < y_new_list[2] and y_list_interval_data[iter_temp] > y_new_list[3]:
    #         cod_mk = y_list_interval_data[iter_temp] * coefK[2] + coefB[2]
    #     elif y_list_interval_data[iter_temp] < y_new_list[3] and y_list_interval_data[iter_temp] > y_new_list[4]:
    #         cod_mk = y_list_interval_data[iter_temp] * coefK[3] + coefB[3]
    #     elif y_list_interval_data[iter_temp] < y_new_list[4] and y_list_interval_data[iter_temp] > y_new_list[5]:
    #         cod_mk = y_list_interval_data[iter_temp] * coefK[4] + coefB[4]
    #     elif y_list_interval_data[iter_temp] < y_new_list[6] and y_list_interval_data[iter_temp] > y_new_list[7]:
    #         cod_mk = y_list_interval_data[iter_temp] * coefK[5] + coefB[5]
    #     elif y_list_interval_data[iter_temp] < y_new_list[7] and y_list_interval_data[iter_temp] > y_new_list[8]:
    #         cod_mk = y_list_interval_data[iter_temp] * coefK[6] + coefB[6]
    #     elif y_list_interval_data[iter_temp] < y_new_list[8]:
    #         cod_mk = y_list_interval_data[iter_temp] * coefK[7] + coefB[7]
    #     print(str(x_list_interval_data[iter_temp]) + " --> " + str(cod_ideal - cod_mk) )
    # for iter_temp in range(len(y_list_interval_data)):
    #     if x_list_interval_data[iter_temp] > 125:
    #         break
    #     test_x.append(x_list_interval_data[iter_temp])
    #     if x_list_interval_data[iter_temp] > x_new_list[-1]:
    #         me_KOD = y_list_interval_data[iter_temp] * coefK[-1] + coefB[-1]
    #         print(str(x_list_interval_data[iter_temp]) + " --> " + str(x_list_interval_data[iter_temp] + " __ "  + str(me_KOD * 0.0625)))
    #         test_y.append(me_KOD)
    #     else:
    #         for i in range(1, len(x_new_list)):
    #             if x_list_interval_data[iter_temp] <= x_new_list[i]:
    #                 me_KOD = y_list_interval_data[iter_temp] * coefK[i-1] + coefB[i-1]
    #                 print(str(x_list_interval_data[iter_temp]) + " --> " + str(
    #                     x_list_interval_data[iter_temp]) + " __ "  + str(me_KOD * 0.0625))
    #                 test_y.append(me_KOD)
    #                 break

    # print("ERROR FINISH")

    # plt.axis([minElement(test_x) - 10, maxElement(test_x) + 10, minElement(test_y) - 200, maxElement(test_y) + 200])
    # plt.plot(test_x, test_y, color='blue')
    # plt.plot([-60, 120], [266, 3583], color='red')
    # plt.show()

    for j in range(len(y_new_list)):
        print("M = " + str(y_new_list[j]))
    for j in range(len(coefK)):
        print("K = " + str(coefK[j]))
    for j in range(len(coefB)):
        print("B = " + str(coefB[j]))
    print("\n" + "BINARY BLOCK")
    #
    # block sending data
    #
    binCodeCorfB = []
    binCodeCorfK = []
    binCodeCorfM = []
    list_m_new = []
    for i in range(1, len(y_new_list) - 1):
        binCodeEleM = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        x = int(y_new_list[i])
        i = 0
        while i < 12:
            y = str(x % 2)
            binCodeEleM[i] = int(y)
            i = i + 1
            x = int(x / 2)
        coefmm = ""
        for i in binCodeEleM:
            coefmm = coefmm + str(i)
            binCodeCorfM.append(i)
        string_test = ""
        for i in range(8):
            string_test += str(binCodeEleM[len(binCodeEleM) - 1 - i])
        list_m_new.append(string_test)

    list_m_int = []
    for line in list_m_new:
        list_m_int.append(int(line, 2))
    setattr(chip, "m_list", list_m_int)

    print("//M")
    print(list_m_new[0] + " //M0")
    print(list_m_new[1] + " //M1")
    print(list_m_new[2] + " //M2")
    print(list_m_new[3] + " //M3")
    print(list_m_new[4] + " //M4")
    print(list_m_new[5] + " //M5")
    print(list_m_new[6] + " //M6")
    # print(list_m_new[7] + " //M7")
    # print(list_m_new[8] + " //M8")

    list_b_new = []
    for ele in coefB:
        x = ele
        # binCodeEleB = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        binCodeEleB = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        i = 0
        if ele < 0:
            # binCodeEleB[13] = 1
            binCodeEleB[12] = 1
            x = x * (-1)
        else:
            # binCodeEleB[13] = 0
            binCodeEleB[12] = 0
        n = ""
        while x > 0:
            y = str(x % 2)
            if i < 12:
                binCodeEleB[i] = int(y)
                i = i + 1
            else:
                break
            x = int(x / 2)
        coefbb = ""
        for z in binCodeEleB:
            binCodeCorfB.append(z)
            coefbb = coefbb + str(z)
        string_test = ""
        for i in range(9):
            string_test += str(binCodeEleB[len(binCodeEleB) - 1 - i])
        # print("b = " + coefbb)
        list_b_new.append(string_test)
        # print("b_test_8_bit = 0b'" + string_test)

    list_b_int = []
    for line in list_b_new:
        list_b_int.append(int(line[1:], 2))
    setattr(chip, "b_list", list_b_int)

    print("//B")
    # print(list_b_new[1][1:] + " //B1")
    print(list_b_new[0] + " //B0")
    print(list_b_new[1] + " //B1")
    print(list_b_new[2] + " //B2")
    print(list_b_new[3] + " //B3")
    print(list_b_new[4] + " //B4")
    print(list_b_new[5] + " //B5")
    print(list_b_new[6] + " //B6")
    print(list_b_new[7] + " //B7")
    # print(list_b_new[8] + " //B8")
    # print(list_b_new[9] + " //B9")
    list_k_new = []
    for ele in coefK:
        x = float(ele)
        binCodeEleK = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # binCodeEleK = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        intX = int(x)
        i = 10
        # i = 5
        while i < 13:
            # while i < 8:
            y = str(intX % 2)
            binCodeEleK[i] = int(y)
            i = i + 1
            intX = int(intX / 2)
        intY = float(ele) - int(ele)
        i = 9
        # i = 4
        while i >= 0:
            z = intY * 2
            binCodeEleK[i] = int(z)
            intY = float(z) - int(z)
            i = i - 1
        coefkk = ""
        for ele in binCodeEleK:
            coefkk = coefkk + str(ele)
            binCodeCorfK.append(ele)
        string_test = ""
        for i in range(8):
            string_test += str(binCodeEleK[len(binCodeEleK) - 1 - i])
        # print("k = " + coefkk)
        list_k_new.append(string_test)

    list_k_int = []
    for line in list_k_new:
        list_k_int.append(int(line, 2))
    setattr(chip, "k_list", list_k_int)

    print("//K")
    print(list_k_new[0] + " //K0")
    print(list_k_new[1] + " //K1")
    print(list_k_new[2] + " //K2")
    print(list_k_new[3] + " //K3")
    print(list_k_new[4] + " //K4")
    print(list_k_new[5] + " //K5")
    print(list_k_new[6] + " //K6")
    print(list_k_new[7] + " //K7")
    # print(list_k_new[8] + " //K8")
    # print(list_k_new[9] + " //K9")

    step = 0
    stepK = 0
    stepB = 0
    stepM = 0
    pacet = []
    while step < 6:
        text = ""
        for i in range(stepK, stepK + 13):
            pacet.append(binCodeCorfK[i])
        stepK = stepK + 13
        for i in range(stepB, stepB + 14):
            pacet.append(binCodeCorfB[i])
        stepB = stepB + 14
        for i in range(stepM, stepM + 12):
            pacet.append(binCodeCorfM[i])
        stepM = stepM + 12
        step = step + 1
    for i in range(stepK, stepK + 13):
        pacet.append(binCodeCorfK[i])
        stepK = stepK + 13
    for i in range(stepB, stepB + 14):
        pacet.append(binCodeCorfB[i])
        stepB = stepB + 14
    text = ""
    iterat = 0
    win_test = []
    for i in range(258):
        if iterat < 8:
            text = text + str(pacet[i])
            iterat += 1
        else:
            not_Invers = list(text)
            nul = 7
            invers = ""
            for j in range(8):
                invers = invers + not_Invers[nul]
                nul -= 1
            win_test.append(chr(int(invers, 2)))
            test = hex(int(invers, 2))
            text = ""
            text = text + str(pacet[i])
            iterat = 1
    text = ""

    # OM
    binCodeEleOM = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # binCodeEleM = [0, 0, 0, 0, 0, 0, 0, 0]
    x = int(all_minus)
    i = 0
    while i < 16:
        # while i < 8:
        y = str(x % 2)
        binCodeEleOM[i] = str(int(y))
        i = i + 1
        x = int(x / 2)


    print("//OM1")
    OM1 = binCodeEleOM[:8]
    setattr(chip, "om1", int(str(''.join(OM1))[::-1], 2))
    print(str(''.join(OM1))[::-1] + " //OM1")

    print("//OM2")
    OM2 = binCodeEleOM[8:]
    setattr(chip, "om2", int(str(''.join(OM2))[::-1], 2))
    print(str(''.join(OM2))[::-1] + " //OM2")

    print("//Z1")
    Z1 = ""
    for i in range(8):
        Z1 += str(list(list_b_new[7 - i])[0])
    setattr(chip, "z", int(Z1, 2))
    print(Z1 + "//Z1")
    Z2 = ""

    # Z2 += str(list(list_b_new[9])[0])
    # Z2 += str(list(list_b_new[8])[0])
    # for i in range(6):
    #     Z2 += "0"
    # setattr(chip, "z2", int(Z2, 2))
    # print("8'b" + Z2 + ";")
    print("-------------------------" + "\n")
    pass


def searchForCoordinats(y_list, x_list, y):
    x = -10000
    f = True
    i = 0
    while f:
        if (y < y_list[i]) and (y >= y_list[i + 1]):
            y1 = y_list[i]
            y2 = y_list[i + 1]
            x1 = x_list[y_list.index(y1)]
            x2 = x_list[y_list.index(y2)]
            x = (((y - y1) * (x2 - x1)) / (y2 - y1)) + x1
            break
        i = i + 1
    return x


def binaryKey(list, size):
    number = 0
    iterator = size
    for element in list:
        number = number + int(element) * (2 ** iterator)
        iterator = iterator - 1
    print(number)
    return number


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

