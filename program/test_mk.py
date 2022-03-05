import numpy as np


def sum_list(iterator, y):
    new_x = list(y)
    new_x.pop(iterator)
    return sum(new_x)/len(new_x)


x = [63489, 61440, 63488, 63489, 63490, 63490, 63489, 63489, 63490, 63489, 63489, 63489, 63489, 63489, 63490, 63488,
     62977, 63489, 63489, 63489, 63489, 63489, 63490, 63490, 63489, 63489, 63489, 63473, 63489, 63490, 63233, 63489]

last_average = sum(x)/len(x)
index = None
while True:
    flag = True
    print("---------")
    for i in x:
        average = sum_list(x.index(i), x)
        if abs(average - last_average) > 7:
            index = x.index(i)
            last_average = average
            # TODO добавить сюда логирование
            flag = False
            break
    if flag:
        break
    x.pop(index)

