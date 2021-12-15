import time
import pylab
import numpy
import scipy
# from matplotlib import mlab
import matplotlib.pyplot as plt
from scipy import interpolate


# from scipy.interpolate import interp1d

def coefficients():
    # xlist = [-60, -3.8, 33.7, 71.1, 125]
    xlist = [-62.01, -26.7, -0.63, 31.88, 72.02, 124.21]
    ylist = [25513, 22521, 20440, 18288, 16001, 13635]
    xlistNew = xlist
    ylistNew = []
    all_min = int(ylist[-1] - 200)
    for i in ylist:
        ylistNew.append(round((i - all_min) / 4))

    calculationOfCoefficients(xlistNew, ylistNew, all_min)


def form_interval(xlist, x_list_interval_data, y_list_interval_data, i, k):
    x_list_interval_data1 = []
    y_list_interval_data1 = []
    interval_data1 = []
    interval_delete = 0
    start = xlist[i]
    stop = xlist[k]
    # print ("start = " + str(start) + " stop = " + str(stop))
    test_flag = False
    for f in range(len(x_list_interval_data)):
        interval_delete += 1
        if test_flag == True:
            x_list_interval_data1.append(round(x_list_interval_data[f], 2))
            y_swich = float(y_list_interval_data[f])
            y_list_interval_data1.append(round(y_swich, 3))  # !!!!!!!!!!
            if round(x_list_interval_data[f], 2) == stop:
                break
        if round(x_list_interval_data[f], 2) >= round(start, 2):
            # print(x_list_interval_data[f])
            test_flag = True
    print(str(interval_delete))
    interval_data1.append(x_list_interval_data1)
    interval_data1.append(y_list_interval_data1)
    interval_data1.append(interval_delete)
    return interval_data1


def minimum(xlist, ylist):
    xlist_test = xlist
    ylist_test = ylist

    interval_data = interpol(xlist, ylist)
    x_list_interval_data = interval_data[0]
    y_list_interval_data = interval_data[1]

    max_step_number = 8

    xlist_test = []
    ylist_test = []

    xlist_test.append(round(x_list_interval_data[0] + 0.01, 2))
    for i in range(1, max_step_number):
        new_temperature = round(xlist_test[i - 1] + (185 / (max_step_number)), 2)
        xlist_test.append(new_temperature)
    xlist_test.append(round(x_list_interval_data[-1] - 0.01, 2))
    for i in xlist_test:
        test = float(y_list_interval_data[x_list_interval_data.index(i)])
        ylist_test.append(round(test, 3))

    # print(y_list_interval_data)
    # plt.axis([minElement(xlist)-10, maxElement(xlist)+10, minElement(ylist)-200, maxElement(ylist)+200])
    # plt.plot(new_list_x, new_list_y, color = 'blue')
    # plt.show()

    for i in range(max_step_number):

        print(xlist_test)
        print(ylist_test)
        print("step = " + str(i + 1) + " in " + str(max_step_number))
        interval = form_interval(xlist_test, x_list_interval_data, y_list_interval_data, i, i + 1)
        del x_list_interval_data[0:interval[2]]
        del y_list_interval_data[0:interval[2]]
        x_list_interval = interval[0]
        y_list_interval = interval[1]
        # print (y_list_interval)
        y_real = 0
        x_real = 0
        for j in range(len(x_list_interval) - 1):
            k_real = float((ylist_test[i] - ylist_test[i + 1]) / (xlist_test[i] - xlist_test[i + 1]))
            b_real = int(ylist_test[i + 1] - k_real * xlist_test[i + 1])
            difference = []
            x_list_test = []
            for k in range(len(y_list_interval) - 1):
                x_list_test.append(k)
                kv_sum = abs(x_list_interval[k] * k_real + b_real) - abs(y_list_interval[k])
                difference.append(pow(kv_sum, 2))
            sum = 0
            for k in difference:
                sum = sum + abs(k)
            if j != 0:
                if (sum / (len(y_list_interval) - 1)) < (sum_last / (len(y_list_interval) - 1)):
                    y_real = int(ylist_test[i + 1])
                    x_real = round(xlist_test[i + 1], 1)
                    sum_last = sum
            else:
                sum_last = sum

            ylist_test[i + 1] = y_list_interval[j]
            xlist_test[i + 1] = x_list_interval[j]
        print("--> " + str(sum / (len(y_list_interval) - 1)) + " <--")
        ylist_test[i + 1] = y_real
        xlist_test[i + 1] = x_real

    new_list_x_temperature = []
    new_list_y_KOD = []

    for i in ylist_test:
        new_list_y_KOD.append(round(float(i) / 16) * 16)

    new_list = []
    new_list.append(xlist_test)
    new_list.append(new_list_y_KOD)
    print("New X = " + str(xlist_test))
    print("New Y = " + str(new_list_y_KOD))
    # print ("New Y = " + str(ylist_test))

    return new_list


def min_kv(xlist, ylist, interval_left, interval_right):
    interval = interpol(xlist, ylist)
    x_list_interval = interval[0]
    y_list_interval = interval[1]

    summa_x = 0
    kv_summ_x = 0
    summa_y = 0
    summ_x_y_proizv = 0
    for i in range(len(x_list_interval)):
        summa_x = summa_x + x_list_interval[i]
        kv_summ_x = kv_summ_x + (x_list_interval[i] * x_list_interval[i])
        summa_y = summa_y + y_list_interval[i]
        summ_x_y_proizv = summ_x_y_proizv + (x_list_interval[i] * y_list_interval[i])
    delta = (kv_summ_x * len(x_list_interval)) - (summa_x * summa_x)
    delta_k = (summ_x_y_proizv * len(x_list_interval)) - (summa_y * summa_x)
    delta_b = (kv_summ_x * summa_y) - (summ_x_y_proizv * summa_x)

    coef_k = delta_k / delta
    coef_b = delta_b / delta

    coef_all = [coef_k, coef_b]

    return coef_all


def interpol(xlist_test, ylist_test):
    tck = interpolate.splrep(xlist_test, ylist_test)
    temperaturerite = xlist_test[0]
    stop_step = xlist_test[len(xlist_test) - 1]
    step = 0.01
    interval_y = []
    interval_x = []
    interval = []
    while temperaturerite < stop_step:
        interval_x.append(round(temperaturerite, 2))
        interval_y.append(interpolate.splev(temperaturerite, tck))
        temperaturerite = temperaturerite + step
    interval.append(interval_x)
    interval.append(interval_y)
    return interval


def calculationOfCoefficients(xlist, ylist, all_minus):
    coefB = []
    coefK = []
    kIdeal = -16
    bIdeal = 2047
    xMinIdeal = -60
    yMinIdeal = -16 * xMinIdeal + 2047
    xMaxIdeal = 125
    yMaxIdeal = -16 * xMaxIdeal + 2047
    i = 0
    print("\n" + "-------------------------" + "\n" + "RESULT:")
    x_new_list = []
    y_new_list = []
    # new_list = minimum(xlist, ylist)
    x_new_list, y_new_list = minimum(xlist, ylist)
    # x_new_list = new_list[0]
    # y_new_list = new_list[1]
    test_k = []
    test_b = []
    while i < len(x_new_list) - 1:
        k_real = 0
        b_real = 0
        k_ideal = 0
        b_ideal = 0
        # k_real = float((y_new_list[i - 1] - y_new_list[i]) / (x_new_list[i - 1] - x_new_list[i]))
        print(x_new_list)
        k_real = float((y_new_list[i] - y_new_list[i + 1]) / float(x_new_list[i] - x_new_list[i + 1]))
        b_real = y_new_list[i] - k_real * x_new_list[i]
        print("b_real in interval " + str(x_new_list[i]) + " : " + str(x_new_list[i + 1]) + " = " + str(b_real))
        print("k_real in interval " + str(x_new_list[i]) + " : " + str(x_new_list[i + 1]) + " = " + str(k_real))
        # k_ideal = round(float(kIdeal / k_real), 4)
        k_ideal = float(kIdeal / k_real)
        # b_ideal = int(-1 * ((kIdeal / k_real) * b_real) + bIdeal)!!
        b_ideal = -1 * ((kIdeal / k_real) * b_real) + bIdeal

        test_k.append(k_real)
        test_b.append(b_real)
        # coefK.append(k_ideal)!!
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
    step_test = 0.1
    test_x = []
    test_y = []
    test_temperature_list = []
    while True:
        if sttt_temperature > 125:
            break
        test_x.append(sttt_temperature)
        if sttt_temperature > x_new_list[-1]:
            sett = sttt_temperature * test_k[-1] + test_b[-1]
            ideal_KOD = kIdeal * sttt_temperature + bIdeal
            me_KOD = sett * coefK[-1] + coefB[-1]
            # print(sttt_temperature)
            # print(ideal_KOD - me_KOD)
            # print(str(sttt_temperature) + " __ " + str(round((ideal_KOD - me_KOD),3)))
            # print("-----")
            test_y.append(me_KOD)
        else:
            for i in range(1, len(x_new_list)):
                if sttt_temperature <= x_new_list[i]:
                    sett = sttt_temperature * test_k[i - 1] + test_b[i - 1]
                    ideal_KOD = kIdeal * sttt_temperature + bIdeal
                    me_KOD = sett * coefK[i - 1] + coefB[i - 1]
                    # print(str(sttt_temperature) + " __ " + str(round((ideal_KOD - me_KOD), 3)))
                    # print("-----")
                    test_y.append(sett * coefK[i - 1] + coefB[i - 1])
                    break
        test_temperature_list.append(sttt_temperature)
        # sttt_temperature = round(sttt_temperature + step_test, 2)!!
        sttt_temperature = sttt_temperature + step_test

    min_delta_temperature = 0
    max_delta_temperature = 0
    for i in range(len(test_temperature_list)):
        deltaa = (test_temperature_list[i] * (kIdeal) + bIdeal) - test_y[i]
        if deltaa > 0:
            max_delta_temperature = max_delta_temperature + deltaa
        if deltaa < 0:
            min_delta_temperature = min_delta_temperature + deltaa

    print("<<--- " + str(min_delta_temperature) + " __ " + str(max_delta_temperature))
    plt.axis([minElement(test_x) - 10, maxElement(test_x) + 10, minElement(test_y) - 200, maxElement(test_y) + 200])
    plt.plot(test_x, test_y, color='blue')
    plt.plot([-60, 125], [2927, 47], color='red')
    plt.show()
    '''
    # NEW BLOCK
    print("START")
    for i in range(len(x_new_list)-1):
        sett = x_new_list[i+1] * test_k[i] + test_b[i]
        me_KOD = sett * coefK[i] + coefB[i]
        ideal_KOD = kIdeal * x_new_list[i+1] + bIdeal
        print(coefB[i])
        coefB[i] = int(coefB[i] - (me_KOD - ideal_KOD)) #1 gradus = 11.5 KOD
        print(coefB[i])
        print("-----")

    print("FINISH")
    sttt_temperature = -60
    test_x = []
    test_y = []
    test_temperature_list = []
    while True:
        if sttt_temperature > 125:
            break
        test_x.append(sttt_temperature)
        if sttt_temperature > x_new_list[-1]:
            sett = sttt_temperature * test_k[-1] + test_b[-1]
            ideal_KOD = kIdeal * sttt_temperature + bIdeal
            me_KOD = sett * coefK[-1] + coefB[-1]
            test_y.append(me_KOD)
        else:
            for i in range(1, len(x_new_list)):
                if sttt_temperature <= x_new_list[i]:
                    sett = sttt_temperature * test_k[i - 1] + test_b[i - 1]
                    ideal_KOD = kIdeal * sttt_temperature + bIdeal
                    me_KOD = sett * coefK[i - 1] + coefB[i - 1]
                    test_y.append(sett * coefK[i - 1] + coefB[i - 1])
                    break
        test_temperature_list.append(sttt_temperature)
        sttt_temperature = round(sttt_temperature + step_test, 2)
    min_delta_temperature = 0
    max_delta_temperature = 0
    for i in range(len(test_temperature_list)):
        deltaa = (test_temperature_list[i] * (kIdeal) + bIdeal) - test_y[i]
        if deltaa > 0:
            max_delta_temperature = max_delta_temperature + deltaa
        if deltaa < 0:
            min_delta_temperature = min_delta_temperature + deltaa
    plt.axis([minElement(test_x) - 10, maxElement(test_x) + 10, minElement(test_y) - 200, maxElement(test_y) + 200])
    plt.plot(test_x, test_y, color='blue')
    plt.plot([-60, 125], [185, 3885], color='red')
    plt.show()
    '''

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
        # binCodeEleM = [0, 0, 0, 0, 0, 0, 0, 0]
        x = int(y_new_list[i])
        i = 0
        while i < 12:
            # while i < 8:
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
        # print("m = " + coefmm)
        list_m_new.append(string_test)
        # print("m_test_8_bit =  0b'" + string_test)
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
                binCodeEleB[i] = int(float(y))
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
    print(str(''.join(OM1))[::-1] + " //OM1")
    print("//OM2")
    OM2 = binCodeEleOM[8:]
    print(str(''.join(OM2))[::-1] + " //OM2")
    print("//Z1")
    Z1 = ""
    for i in range(len(list_b_new)):
        Z1 += str(list(list_b_new[7 - i])[0])
    print("8'b" + Z1 + ";")
    # Z2 = ""
    # for i in range(len(list_b_new)):
    #     Z2 += str(list(list_b_new[7-i])[0])
    print("8'b" + Z1 + ";")
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
            break;
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


def readFile(i):
    try:
        file = open('c:/micros/data/' + i + '.txt', 'r')
        say = []
        col_list = []
        for line in file:
            say = line.split(' ')
            if len(say) > 0:
                col_list.append(say[0])
                col_list.append(say[1])
        file.close()
        print(col_list)
        return col_list
    except:
        pass


def build_graph():
    print("\n" + "-------------------------")
    print("write number file")
    g = raw_input()
    numberPin = int(g)
    col_list = readFile(g)
    xlist = []
    ylist = []
    xlistNew = []
    ylistNew = []
    i = 0
    while i < len(col_list):
        xlist.append(float(col_list[i]))
        i = i + 2
    i = 1
    while i < len(col_list):
        ylist.append(float(col_list[i]))
        i = i + 2
    plt.axis([minElement(xlist) - 10, maxElement(xlist) + 10, minElement(ylist) - 200, maxElement(ylist) + 200])
    plt.plot(xlist, ylist, color='blue')
    plt.plot([-55, 125], [2927, 47], color='red')
    plt.show()
    pass


coefficients()
