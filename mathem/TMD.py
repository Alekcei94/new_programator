from scipy import interpolate
import numpy as np
import random as rand
import math
# import mathem.utility as test
import mathem.utility as utility


class TMD:
    """Main tm class"""

    def __init__(self, tm_type, xy_path, left_temp=-60, right_temp=125, num_interpolate_points=20000, kind='cubic',
                 num_points_total=9,
                 maximum_gap=10,
                 min_code=200, annealing_start_temp=50, annealing_step=0.001, annealing_multiplier=10, k_bits=5,
                 b_bits_shift=4,
                 m_bits=12, m_bits_shift=4, left_mutation=-10, right_mutation=10,
                 force_minimum=None):
        self.tm_type = tm_type
        self.left_temp = left_temp
        self.right_temp = right_temp
        self.num_interpolate_points = num_interpolate_points
        self.kind = kind
        self.num_points_total = num_points_total
        self.maximum_gap = maximum_gap
        #
        self.min_code = min_code
        self.force_minimum = force_minimum
        #
        self.annealing_start_temp = annealing_start_temp
        self.annealing_step = annealing_step
        self.annealing_multiplier = annealing_multiplier
        self.left_mutation = left_mutation
        self.right_mutation = right_mutation

        if tm_type == '10':
            self.k_ideal = -16
            self.b_ideal = 2047
            self.common_divisor = 4
        elif tm_type == "analog":
            self.k_ideal = 18.43
            self.b_ideal = 1371.67
            self.common_divisor = 1

        self.k_bits = k_bits
        self.b_bits_shift = b_bits_shift
        self.m_bits = m_bits
        self.m_bits_shift = m_bits_shift

        self.temp_interpolate = np.linspace(self.left_temp, self.right_temp, num=self.num_interpolate_points,
                                            endpoint=True)
        self.temp_interpolate_extended = np.linspace(self.left_temp - 2, self.right_temp + 2,
                                                     num=self.num_interpolate_points,
                                                     endpoint=True)
        self.pair_result_saved = dict()

        with open(xy_path) as f:
            lines = f.readlines()
            x = [float(el.split(' ')[0]) for el in lines]
            y = [float(el.split(' ')[1].strip()) for el in lines]
        self.interpol, self.minimum, self.code_interpolate_fitted, self.code_interpolate_fitted_extended = self.prepare_interpolation(
            x, y)
        self.interpolation_dictionary = self.prepare_interpolation_dictionary(self.code_interpolate_fitted_extended)
        self.possible_points = self.prepare_possible_points(self.code_interpolate_fitted_extended)
        self.ideal_code = self.prepare_ideal_code(self.interpolation_dictionary)

    def prepare_interpolation(self, temp, code):
        """Create fitted interpolation list for extended temp.
        Fill interpolation dictionary with codes as keys and temps as values."""
        interpol = interpolate.interp1d(temp, code, kind=self.kind, fill_value='extrapolate')

        if self.tm_type == '10':
            minimum = int(interpol(125) - self.min_code)
        elif self.tm_type == 'analog':
            minimum = int(interpol(-60) - self.min_code)
        if self.force_minimum is not None:
            minimum = self.force_minimum
        code_interpolate_fitted = [round((interpol(t) - minimum) / self.common_divisor) for t in
                                   self.temp_interpolate]
        code_interpolate_fitted_extended = [round((interpol(t) - minimum) / self.common_divisor) for t in
                                            self.temp_interpolate_extended]
        print(code_interpolate_fitted)
        return interpol, minimum, code_interpolate_fitted, code_interpolate_fitted_extended

    def prepare_interpolation_dictionary(self, code_interpolate_fitted):
        interpolation_dictionary = dict()
        for temp, value in zip(self.temp_interpolate_extended, code_interpolate_fitted):
            interpolation_dictionary[value] = temp
        print(interpolation_dictionary)
        return interpolation_dictionary

    def prepare_possible_points(self, code_interpolate_fitted):
        """Fill possible points for M: from first code rounded to 4 bits to last code rounded to 4 bits."""
        possible_points = []
        # possible points are 0, 16, 32, 48, 64, 80, 96 ..., maximum possible value is max(code_interpolate_fitted)
        edge_one = round(code_interpolate_fitted[-1] / (2 ** self.m_bits_shift)) * (2 ** self.m_bits_shift)
        edge_two = round((code_interpolate_fitted[0]) / (2 ** self.m_bits_shift)) * (2 ** self.m_bits_shift)
        [possible_points.append(code) for code in
         np.arange(min(edge_one, edge_two) + 16, max(edge_one, edge_two), step=(2 ** self.m_bits_shift))]
        # print(possible_points)
        return possible_points

    def prepare_ideal_code(self, interpolation_dictionary):
        """Calculate ideal code for all codes.
        Example: mk_code: 50 => temp: 125 => ideal_code[50]: -16*125 + 2047"""
        ideal_code = dict()
        for value in interpolation_dictionary.keys():
            temp = interpolation_dictionary[value]
            ideal_code[value] = round(self.k_ideal * temp + self.b_ideal, 2)
        return ideal_code

    def start_transform(self):
        return self.simulated_annealing()

    def simulated_annealing(self):
        dict_points = self.get_random_points()
        annealing_temp = self.annealing_start_temp
        annealing_sum = 0
        while annealing_sum == 0:
            dict_points = self.get_random_points()
            try:
                annealing_sum = self.outcome(dict_points)
            except utility.BadMutationException:
                print('Failing starting point.')
        while annealing_temp > 0:
            changes = self.mutate_points(dict_points)
            try:
                attempt_sum = self.outcome(dict_points)
                delta_sum = attempt_sum - annealing_sum
                if delta_sum < 0:
                    annealing_sum = attempt_sum
                else:
                    probability = math.exp(-delta_sum / annealing_temp)
                    if probability < rand.uniform(0, 1):
                        self.undo_changes(dict_points, changes)
                    else:
                        annealing_sum = attempt_sum
            except utility.BadMutationException:
                self.undo_changes(dict_points, changes)
                # print(Exception)
            annealing_temp -= self.annealing_step
            if round(annealing_temp * 10000) % 10000 == 0:
                print(annealing_temp)
                print(dict_points)
                print(annealing_sum)

        self.outcome(dict_points, printable=True, shorted=False)
        print(dict_points)
        return dict_points

    def get_random_points(self):
        """Requires prepared possible_points to work."""
        dict_points = dict()
        dict_points[self.possible_points[0]] = 0
        dict_points[self.possible_points[-1]] = 0
        while len(dict_points) < self.num_points_total:
            dict_points[self.possible_points[rand.randrange(1, len(self.possible_points) - 1)]] = rand.randrange(-20,
                                                                                                                 20)
        return dict_points

    def mutate_points(self, points):
        """Choose one random point from dictionary (except edges) and exchange it with new random point and random
        value. """
        possible_key = rand.choice(self.possible_points)
        if possible_key not in points:
            keys = list(points)
            keys.sort()
            key_delete = rand.choice(keys[1:-1])
            value_delete = points[key_delete]
            points.pop(key_delete)
            possible_value = 0
            if self.left_mutation != 0 and self.right_mutation != 0:
                possible_value = rand.randrange(self.left_mutation, self.right_mutation)
            points[possible_key] = possible_value
            return key_delete, value_delete, possible_key, possible_value
        else:
            possible_value = 0
            if self.left_mutation != 0 and self.right_mutation != 0:
                possible_value = rand.randrange(self.left_mutation, self.right_mutation)
            value_delete = points[possible_key]
            points[possible_key] = possible_value
            return possible_key, value_delete, possible_key, possible_value

    def undo_changes(self, points, changes):
        """Undo changes that was initiated by mutate_points method."""
        key_delete, value_delete, possible_key, possible_value = changes
        points.pop(possible_key)
        points[key_delete] = value_delete

    def outcome(self, points, printable=False, shorted=True):
        """Optimization function: sum standard deviations for all codes
         using ranges of points that was set inside points variable.
         We are using additive value to decrease gaps near points.
         Printable variable is for logs.
         Shorted variable gives speed boost to function but cuts logging messages (recommended True)"""
        points_list = list(points.keys())
        points_list.sort()
        pairs = [(points_list[i], points_list[i + 1]) for i in range(len(points_list) - 1)]
        integral = 0
        last = None
        max_code = max(self.code_interpolate_fitted[0], self.code_interpolate_fitted[-1])
        min_code = min(self.code_interpolate_fitted[0], self.code_interpolate_fitted[-1])
        for idx, pair in enumerate(pairs):
            x1, x2 = pair[0], pair[1]
            k, b = self.get_k_b_for_line(self.interpolation_dictionary[x1], x1 + points[x1],
                                         self.interpolation_dictionary[x2], x2 + points[x2])
            z = math.copysign(1, b)
            self.log(f'k1:{k} b1: {b} z: {z} <==> ki: {self.k_ideal} bi: {self.b_ideal} ', printable)
            k_int, b_int = self.form_k_refactored(k), self.form_b_refactored(b)
            self.log(f'k_deviation: {(k_int / ((2 ** self.k_bits) * k + 0.0001) - 1) * 100}%', printable)
            self.log(f'k_int:{k_int} b_int: {b_int} z: {z}', printable)
            self.log(f'b_deviation_absolute: {b_int - abs(b) / (2 ** self.b_bits_shift)}', printable)
            # speed up by using previous results
            res = self.pair_result_saved.get((k_int, b_int, pair))
            if res is not None and shorted:
                integral += res
                if last is None:
                    last = (int((x2 - 1) * k_int) >> self.k_bits) + z * (b_int << self.b_bits_shift)
                    continue
                gap = (int(x1 * k_int) >> self.k_bits) + z * (b_int << self.b_bits_shift) - last
                if gap > self.maximum_gap:
                    integral += gap ** 2
                last = (int((x2 - 1) * k_int) >> self.k_bits) + z * (b_int << self.b_bits_shift)
                continue
            #
            A = []
            B = []
            test = []
            x1 = max(min(x1, max_code), min_code)
            x2 = max(min(x2, max_code), min_code)
            if x1 == x2: raise utility.BadMutationException()
            for code in range(x1, x2):
                A.append(self.ideal_code.get(code))
                # mk_code = int(code * k) + b
                mk_code = (int(code * k_int) >> self.k_bits) + z * (b_int << self.b_bits_shift)
                B.append(round(mk_code, 2))
                test.append((code, self.interpolation_dictionary[code], self.ideal_code.get(code), round(mk_code, 2)))
            standard_deviation = math.sqrt(math.sqrt(np.sum(np.power((np.array(A) - np.array(B)), 6)) / len(A)))
            integral += standard_deviation * (x2 - x1)
            self.pair_result_saved[k_int, b_int, pair] = standard_deviation
            # we should calculate gap
            if last is not None:
                gap = (int(x1 * k_int) >> self.k_bits) + z * (b_int << self.b_bits_shift) - last
                if gap > self.maximum_gap:
                    integral += gap ** 2
            last = (int((x2 - 1) * k_int) >> self.k_bits) + z * (b_int << self.b_bits_shift)
            self.log(test, printable)
            self.log(f'maximum_absolute_point_deviation: {max(abs(np.array(A) - np.array(B)))}', printable)
            self.log(f'standard_deviation: {standard_deviation}', printable)

        integral = integral * self.annealing_multiplier
        self.log(integral / self.annealing_multiplier, printable)
        return integral

    def get_k_b_for_line(self, x0, y0, x1, y1):
        """
        | ideal: y = k * x + b
        | real: y = g * x + c;
        ideal = real * f + shift
        k * x + b = (g * x + c) * f + shift      =>
        | f = k / g
        | shift = b - c * f
        """
        if x0 == x1:
            raise utility.BadMutationException(f'same code near points: x0:{x0} y0:{y0} x1:{x1} y1:{y1}')
        g = (y1 - y0) / (x1 - x0)
        c = y0 - g * x0
        f = self.k_ideal / g
        shift = self.b_ideal - ((self.k_ideal / g) * c)
        k = round(f, 4)
        return k, shift

    def form_k_refactored(self, k):
        if k >= 8:
            raise utility.BadMutationException(f'k = {k}')
        decimal_part = int(k)
        fractional_part = round((k % 1) * (2 ** self.k_bits))
        int_k = (decimal_part << self.k_bits) | fractional_part
        return int_k

    def form_b_refactored(self, b):
        if int(abs(b) // (2 ** self.b_bits_shift)) > 255:
            return 255
        return int(abs(b) // (2 ** self.b_bits_shift))

    def log(self, element, printable):
        print(element) if printable else None

    def get_m_k_b_z_for_points(self, interpolation_dictionary, points):
        points_list = list(points.keys())
        points_list.sort()
        pairs = [(points_list[i], points_list[i + 1]) for i in range(len(points_list) - 1)]
        m_set = set()
        k_arr = []
        b_arr = []
        z_arr = []
        for pair in pairs:
            x1, x2 = pair[0], pair[1]
            k, b = self.get_k_b_for_line(interpolation_dictionary[x1], x1 + points[x1],
                                         interpolation_dictionary[x2], x2 + points[x2])
            if math.copysign(1, b) >= 0:
                z = 0
            else:
                z = 1
            k_int, b_int = self.form_k_refactored(k), self.form_b_refactored(b)
            m_set.add(x1)
            m_set.add(x2)
            k_arr.append(k_int)
            b_arr.append(b_int)
            z_arr.append(z)

        m_arr = sorted(list(m_set))[1:-1]
        return m_arr, k_arr, b_arr, z_arr

    def execute_point_optimization(self):
        points = self.start_transform()
        return self.get_m_k_b_z_for_points(self.interpolation_dictionary, points)
