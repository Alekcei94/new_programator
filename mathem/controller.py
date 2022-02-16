import TMD
import utility

if __name__ == '__main__':
    TM = TMD.TMD(tm_type='10', xy_path='tm_10_points.txt', annealing_step=0.001, maximum_gap=100,
                 num_points_total=9, kind='cubic',
                 annealing_multiplier=20, left_mutation=-20, right_mutation=20, min_code=100)

    # m, k, b, z = \
    #     [288, 528, 672, 992, 1200, 1328, 1440], [40, 49, 58, 64, 80, 101, 125, 148], [9, 4, 5, 13, 44, 93, 155, 220], [
    #         1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]
    #
    # ddd, std, abd = utility.plot_graph(TM, (m, k, b, z), plot=False)
    # print(m, k, b, z)
    # next = dict()
    # for key, value in ddd.items():
    #     next[value[0]] = key, value[1], value[2], value[3]
    #
    # results = []
    # OM = TM.minimum
    # for code in [2045]:
    #     for i in range(0, -10, -1):
    #         if next.get(code - i) is not None:
    #             results.append(next.get(code - i))
    #             break
    # print(results)
    # print(results[0][0] + TM.minimum)
    # exit(0)
    # test = int(TM.interpol(-58.3) - TM.minimum)
    # # print(test+ TM.minimum)
    # print(f'test: {test + TM.minimum}')
    # mk_code = (int(test * results[0][1]) >> 5) + results[0][3] * (results[0][2] << 4)
    # print(f'mk_code: {mk_code}')
    # print(f'minimum: {TM.minimum}')
    # exit(0)
    # [print(res) for res in results]
    results = [62530, 62633, 62698, 62762, 62824, 62882, 62936, 62985, 63032, 63080, 63125, 63170, 63212, 63257, 63301,
               63341, 63386, 63425, 63455, 63495, 63532, 63588, 63608, 63634, 63665, 63694, 63722, 63750, 63776, 63800,
               63824, 63846, 63867, 63888, 63908, 63927, 63969]
    m, k, b, z = TM.execute_point_optimization()
    print(m, k, b, z)
    exit(0)
    # print(TM.minimum)

    # m, k, b, z = \
    # [288, 528, 672, 992, 1200, 1328, 1440], [40, 49, 58, 64, 80, 101, 125, 148], [9, 4, 5, 13, 44, 93, 155, 220], [
    #     1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]
    ddd, std, abd = utility.plot_graph(TM, (m, k, b, z), plot=False)
    print(std, abd)
    another = [print(int(ddd[res - TM.minimum][0])) for res in results]
    print(m, k, b, z)
    print(TM.minimum)
    ddd, std, abd = utility.plot_graph(TM, (m, k, b, z), plot=True)

    # utility.plot_interpolation(TM.interpolation_dictionary)
    # utility.check_real_line(TM, (m, k, b, z))
