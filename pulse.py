import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum


class Method(Enum):
    TRIVIAL = 0
    PASCAL = 1


def sm_filter(source, smooth_size, method):
    if smooth_size < 3:
        raise IOError("Smoothing size must be greater than 2.")
    if smooth_size % 2 == 0:
        raise IOError("Smoothing size must be an odd number.")
    result = []
    result_size = len(source) - smooth_size + 1
    shift = int((smooth_size - 1) / 2)
    if method == Method.TRIVIAL:
        denominator = (shift + 1) ** 2
    elif method == Method.PASCAL:
        denominator = 2 ** (smooth_size - 1)
        numerators = get_pascal_coefficients(smooth_size - 1)
        print(numerators)
    else:
        raise IOError("Unknown method.")
    formula = 'result[0] = '
    for i in range(result_size - 1):
        value = 0
        for j in range(smooth_size):
            if method == Method.TRIVIAL:
                numerator = j + 1 if j <= shift else smooth_size - j
            elif method == Method.PASCAL:
                numerator = numerators[j]
            else:
                raise IOError("Unknown method.")
            value = value + (numerator / denominator) * source[i + j]
            if len(result) == 0:
                formula = formula + f'{numerator}/{denominator} * Y[{i + j}] + '
        result.append(value)
    truncated_source = source[shift: result_size + shift - 1]
    return truncated_source, result, formula[0:len(formula) - 3]


def get_pascal_coefficients(row_number):
    def get_pascal_triangle(rows):
        def combination(n, r):
            return int((math.factorial(n)) / ((math.factorial(r)) * math.factorial(n - r)))

        result = []
        for count in range(rows):
            row = []
            for element in range(count + 1):
                row.append(combination(count, element))
            result.append(row)
        return result

    return get_pascal_triangle(row_number + 1)[row_number]


def union(input_extremums, lower_cutoff, precision):
    do_while = True
    result = []
    for e in input_extremums:
        if e > lower_cutoff: result.append(e)
    while do_while:
        extremums = result
        result = []
        # print(extremums)
        for i in range(len(extremums) - 1):
            # print(" i == ", i, " len(extremums)-1 = ", len(extremums) - 1)
            if abs(extremums[i + 1] - extremums[i]) < precision:
                result.append(max(extremums[i + 1], extremums[i]))
                # print(" append max (%d-th, %d-th) between (%d and %d)" % (i, i + 1, extremums[i], extremums[i + 1]))
                for j in range(i + 2, len(extremums)):
                    result.append(extremums[j])
                    # print(" tail append %d-th element = %d" % (j, extremums[j]))
                break
            else:
                result.append(extremums[i])
                # print(" append %d-th element = %d" % (i, extremums[i]))
                if i + 1 == len(extremums) - 1:
                    result.append(extremums[i + 1])
                    # print(" append %d-th tail element = %d" % (i + 1, extremums[i + 1]))
                    do_while = False
                    break
    return result


def smooth(sample, method, lower_cutoff, precision, step_limit, extremums_count_limit):
    for step in range(1, step_limit + 1):
        source, result, formula_example = sm_filter(sample, step*2+1, method)
        print('Formula example : ', formula_example)
        print('Source integral = %d, result integral = %d, divergence %d%%' %
              (sum(source), sum(result), (100 - 100 / sum(source) * sum(result))))
        df = pd.Series(result)
        grp = df.groupby((np.sign(df.diff().fillna(0)).diff().fillna(0).ne(0)).cumsum())
        extremums = grp.apply(lambda x: x.max())
        print("Extremums = ", extremums.values)
        extremums = union(extremums.values, lower_cutoff, precision)
        print("United extremums = ", extremums)
        if (len(extremums) <= extremums_count_limit): break
    return source, result


spectrum = pd.read_csv('spectrum4.csv', names=['Y'])
source_sample = spectrum['Y'][1:800].values
Y, W = smooth(source_sample, Method.TRIVIAL, int(max(source_sample)/16), int(max(source_sample)/512), 30, 3)
X = range(Y.size)
plt.plot(X, Y, X, W)
plt.show()
