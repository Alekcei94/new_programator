from scipy import interpolate
from scipy import integrate
import numpy as np
import matplotlib.pyplot as plt
import random as rand
import math
# import main
# import main_analog_tm as analog_tm

class BadMutationException(Exception):
    """Raised when coefficients are forming k=0"""
    pass

def get_all_codes_assosiation_revert(M, k, b, z):
    ran = np.arange(0, 4000, 1)
    # print(ran)
    d = dict()
    for code in ran:
        ch = False
        for i in range(len(M)):
            if code > M[i]:
                d[code] = k[i], b[i], z[i]
                ch = True
        if not ch:
            d[code] = k[7], b[7], z[7]
    # print(d)
    answers = dict()
    for code in d.keys():
        k_int, b_int, z_int = d[code]
        mk_code = (int(code * k_int) >> main.k_bits) + z_int * (b_int << main.b_bits_shift)
        answers[mk_code] = code
    # print(answers)
    return answers


def get_all_codes_association(tm, M, k, b, z):
    ran = np.arange(0, 4000, 1)
    d = dict()
    for code in ran:
        ch = False
        for i in range(len(M)):
            if code < M[i]:
                d[code] = k[i], b[i], z[i]
                ch = True
                break
        if not ch:
            d[code] = k[len(M)], b[len(M)], z[len(M)]
    answers = dict()
    for code in d.keys():
        k_int, b_int, z_int = d[code]
        mk_code = (int(code * k_int) >> tm.k_bits) + z_int * (b_int << tm.b_bits_shift)
        # mk_code = int(code * k_int) + z_int * b_int
        answers[code] = mk_code, k_int, b_int, z_int
    return answers

def plot_graph_for_codes_in_dictionary(dicti):
    print(dicti)


def start(minimum):
    # check all real points
    with open('./1_kb1.txt') as f:
        with open('./1_kb2.txt') as f2:
            M = [int(el)*16 for el in f.readline().strip().split(' ')]
            k = [int(el) for el in f.readline().strip().split(' ')]
            b = [int(el) for el in f.readline().strip().split(' ')]
            z = [int(el) for el in f.readline().strip().split(' ')]
            M2 = [int(el) * 16 for el in f2.readline().strip().split(' ')]
            k2 = [int(el) for el in f2.readline().strip().split(' ')]
            b2 = [int(el) for el in f2.readline().strip().split(' ')]
            z2 = [int(el) for el in f2.readline().strip().split(' ')]
            # (code = 1 to 4000): mk_code -> code
            revert_dict = get_all_codes_assosiation_revert(M, k, b, z)
            # (code = 1 to 4000): code -> mk_code, k, b, z
            lexa_old_dict = get_all_codes_association(M, k, b, z)
            lexa_new_dict = get_all_codes_association(M2, k2, b2, z2)
            with open('./1_t.txt') as f2:
                lines = f2.readlines()
                temp = [float(el.split(' ')[0]) for el in lines]
                codes = [2048 - int(el.split(' ')[1].strip()) for el in lines]
                # print(codes)
                old_codes = [revert_dict.get(code) if revert_dict.get(code) is not None else revert_dict.get(code+1) for code in codes]
                temp_old_codes = [elem for elem in zip(temp, old_codes)]
                # print(temp_old_codes)
                return lexa_old_dict, lexa_new_dict, temp_old_codes


    # outcome(interpolation_dictionary, pts, True)


def plot_graph(tm, coeffs, plot=True):
    ddd = get_all_codes_association(tm, coeffs[0], coeffs[1], coeffs[2], coeffs[3])
    t_line = []
    ideal_line = []
    real_line = []
    with open('log.txt', 'w') as f:
        for t in tm.temp_interpolate:
            inti = round((tm.interpol(t) - tm.minimum) / tm.common_divisor)
            if ddd[inti] is None:
                break
            t_line.append(t)
            ideal_line.append(t * tm.k_ideal + tm.b_ideal)
            real_line.append(ddd[inti][0])
            # print(t, t * tm.k_ideal + tm.b_ideal, ddd[inti], file=f)
    standard_deviation = math.sqrt(np.sum(np.power((np.array(real_line) - np.array(ideal_line)), 2)) / len(t_line))
    # print(f'st. deviation: {standard_deviation}')
    absolute_deviation = max(abs(np.array(real_line) - np.array(ideal_line)))
    # print(f'abs. deviation: {absolute_deviation}')

    plt.plot(t_line, real_line)
    plt.plot(t_line, ideal_line)
    if plot:
        plt.show()
    plt.clf()
    return ddd, standard_deviation, absolute_deviation


def plot_interpolation(interpolation_dictionary):
    x = []
    y = []
    for key, value in interpolation_dictionary.items():
        x.append(key)
        y.append(value)
    plt.plot(x, y)
    plt.show()


def check_real_line(tm, coeffs):
    # check all real points
    lexa_old_dict, lexa_new_dict, base_temp_code = start(tm.minimum)
    ddd = get_all_codes_association(coeffs[0], coeffs[1], coeffs[2], coeffs[3])

    with open('log.txt', 'w') as f:
        for t in tm.temp_interpolate:
            inti = round((tm.interpol(t) - tm.minimum) / 4)
            print(t, t * tm.k_ideal + tm.b_ideal, lexa_old_dict[inti], lexa_new_dict[inti], ddd[inti], file=f)

    true_code = [t * tm.k_ideal + tm.b_ideal for t in tm.temp_interpolate]
    lexa_old_code = [lexa_old_dict[round((tm.interpol(t) - tm.minimum) / 4)][0] for t in
                     tm.temp_interpolate]
    lexa_new_code = [lexa_new_dict[round((tm.interpol(t) - tm.minimum) / 4)][0] for t in tm.temp_interpolate]
    dima_code = [ddd[round((tm.interpol(t) - tm.minimum) / 4)][0] for t in tm.temp_interpolate]
    print(
        f'lexa_old: st. deviation: {math.sqrt(np.sum(np.square(np.array(true_code) - np.array(lexa_old_code))) / len(lexa_old_code))}')
    print(
        f'lexa_new: st. deviation: {math.sqrt(np.sum(np.square(np.array(true_code) - np.array(lexa_new_code))) / len(lexa_new_code))}')
    print(
        f'dima: st. deviation: {math.sqrt(np.sum(np.square(np.array(true_code) - np.array(dima_code))) / len(dima_code))}')
    print(
        f'lexa_old: max absolute deviation: {math.sqrt(np.max(np.square(np.array(true_code) - np.array(lexa_old_code))))}')
    print(
        f'lexa_new: max absolute deviation: {math.sqrt(np.max(np.square(np.array(true_code) - np.array(lexa_new_code))))}')
    print(
        f'dima: max absolute deviation: {math.sqrt(np.max(np.square(np.array(true_code) - np.array(dima_code))))}')
    # print(possible_points)
    # print(M)