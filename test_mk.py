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

def interpol(xlist_test, ylist_test):
    tck = interpolate.splrep(xlist_test, ylist_test)
    temperaturerite = xlist_test[0]
    stop_step = xlist_test[len(xlist_test) - 1]
    step = 0.1
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

real_y = [266.175, 284.6025, 303.03, 321.4575, 339.885, 358.3125, 376.74, 395.1675, 413.595, 432.0225, 450.45, 468.8775, 487.305, 505.7325, 524.16, 542.5875, 561.015, 579.4425, 597.87, 616.2975, 634.725, 653.1525, 671.58, 690.0075, 708.435, 726.8625, 745.29, 763.7175, 782.145, 800.5725, 819, 837.4275, 855.855, 874.2825, 892.71, 911.1375, 929.565, 947.9925, 966.42, 984.8475, 1003.275, 1021.7025, 1040.13, 1058.5575, 1076.985, 1095.4125, 1113.84, 1132.2675, 1150.695, 1169.1225, 1187.55, 1205.9775, 1224.405, 1242.8325, 1261.26, 1279.6875, 1298.115, 1316.5425, 1334.97, 1353.3975, 1371.825, 1390.2525, 1408.68, 1427.1075, 1445.535, 1463.9625, 1482.39, 1500.8175, 1519.245, 1537.6725, 1556.1, 1574.5275, 1592.955, 1611.3825, 1629.81, 1648.2375, 1666.665, 1685.0925, 1703.52, 1721.9475, 1740.375, 1758.8025, 1777.23, 1795.6575, 1814.085, 1832.5125, 1850.94, 1869.3675, 1887.795, 1906.2225, 1924.65, 1943.0775, 1961.505, 1979.9325, 1998.36, 2016.7875, 2035.215, 2053.6425, 2072.07, 2090.4975, 2108.925, 2127.3525, 2145.78, 2164.2075, 2182.635, 2201.0625, 2219.49, 2237.9175, 2256.345, 2274.7725, 2293.2, 2311.6275, 2330.055, 2348.4825, 2366.91, 2385.3375, 2403.765, 2422.1925, 2440.62, 2459.0475, 2477.475, 2495.9025, 2514.33, 2532.7575, 2551.185, 2569.6125, 2588.04, 2606.4675, 2624.895, 2643.3225, 2661.75, 2680.1775, 2698.605, 2717.0325, 2735.46, 2753.8875, 2772.315, 2790.7425, 2809.17, 2827.5975, 2846.025, 2864.4525, 2882.88, 2901.3075, 2919.735, 2938.1625, 2956.59, 2975.0175, 2993.445, 3011.8725, 3030.3, 3048.7275, 3067.155, 3085.5825, 3104.01, 3122.4375, 3140.865, 3159.2925, 3177.72, 3196.1475, 3214.575, 3233.0025, 3251.43, 3269.8575, 3288.285, 3306.7125, 3325.14, 3343.5675, 3361.995, 3380.4225, 3398.85, 3417.2775, 3435.705, 3454.1325, 3472.56, 3490.9875, 3509.415, 3527.8425, 3546.27, 3564.6975, 3583.125, 3601.5525, 3619.98, 3638.4075, 3656.835, 3675.2625]
real_x = [i for i in range(-60, 126, 1)]

xlist = [-62.8, -39.6, -20, -0.5, 18.9, 39.3, 59.3, 78.4, 97.4, 125.7]
ylist1 = [62521,
62839,
63056,
63242,
63417,
63574,
63707,
63811,
63899,
64010]
min = ylist1[0]-200
ylist = [i - min for i in ylist1]

interval_data = interpol(xlist, ylist)
t = interval_data[0]
y = interval_data[1]

step = 0.1
tem = -47.2
razn0 = []
test_x = []
test_y = []
real_temp = []
tem = -60
while tem <= 125:
     test_x.append(tem)
     real_temp.append(tem)
     x = int(y[t.index(tem)])

     z = -1
     m = [28,43,56,70,81,90,97]
     k1 = [40,53,61,64,76,94,120,136]
     b1 = [2,14,24,30,56,102,176,224]
     # if x > (m[0] << 4):
     #     #print(0)
     #     razn0.append("R0")
     #     k = k1[0] #- 1
     #     b = b1[0] #+ 10#+ 4
     # elif x > (m[1] << 4):
     #     razn0.append("R1")
     #     #print(1)
     #     k = k1[1] #+ 1
     #     b = b1[1] #+ 3
     # elif x > (m[2] << 4):
     #     razn0.append("R2")
     #     #print(2)
     #     k = k1[2] #+ 1
     #     b = b1[2] #- 1 #+ 2
     # elif x > (m[3] << 4):
     #     razn0.append("R3")
     #     #print(3)
     #     k = k1[3] #+ 1
     #     b = b1[3] #+ 1 #+ 3
     # elif x > (m[4] << 4):
     #     razn0.append("R4")
     #     #print(4)
     #     k = k1[4]  # Угол не верный
     #     b = b1[4]  #+ 1#+ 2
     # elif x > (m[5] << 4):
     #     razn0.append("R5")
     #     #print(5)
     #     k = k1[5]
     #     b = b1[5] #- 1
     # elif x > (m[6] << 4):
     #     razn0.append("R6")
     #     #print(6)
     #     k = k1[6] #+ 1
     #     b = b1[6] #+ 1
     # elif x <= (m[6] << 4):
     #     razn0.append("R7")
     #     #print(7)
     #     k = k1[7]
     #     b = b1[7]
     #     #z = -1
     if x < (m[0] << 4):
         #print(0)
         razn0.append("R0")
         k = k1[0]
         b = b1[0]
     elif x < (m[1] << 4):
         razn0.append("R1")
         #print(1)
         k = k1[1]
         b = b1[1]
     elif x < (m[2] << 4):
         razn0.append("R2")
         #print(2)
         k = k1[2]
         b = b1[2]
     elif x < (m[3] << 4):
         razn0.append("R3")
         #print(3)
         k = k1[3]
         b = b1[3]
     elif x < (m[4] << 4):
         razn0.append("R4")
         #print(4)
         k = k1[4]
         b = b1[4]
     elif x < (m[5] << 4):
         razn0.append("R5")
         #print(5)
         k = k1[5]
         b = b1[5]
     elif x < (m[6] << 4):
         razn0.append("R6")
         #print(6)
         k = k1[6]
         b = b1[6]
     elif x >= (m[6] << 4):
         razn0.append("R7")
         #print(7)
         k = k1[7]
         b = b1[7]
         #z = -1
     kod = x * k
     new_kod = (kod >> 5) + z * (b << 4)
     #print("temp: " + str(tem) + " kod: " + str(new_kod))
     # temp = 1
     # if new_kod >= 2048:
     #     temp = -1 * (new_kod - 2048) * 0.0625
     # else:
     #     temp = (2047 - new_kod) * 0.0625
     test_y.append(new_kod)
     #print("Ideal temp = " + str(tem) + " Real temp = " + str(temp))
     tem = round((tem + 1), 1)
#for i in range(len(test_y)):
    #print(test_y[i] - real_y[i])
plt.axis([minElement(test_x) - 5, maxElement(test_x) + 5, minElement(test_y) - 5, maxElement(test_y) + 5])
plt.plot(test_x, test_y, color='blue')
#plt.plot(test_x, real_temp, color='red')
plt.plot(real_x, real_y, color='red')
plt.show()