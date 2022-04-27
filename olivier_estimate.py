import pandas as pd
import numpy as np
from Extension.record import Record
import matplotlib.pyplot as plt
import os
import psutil
import time
import multiprocessing

def olivier_estimate_for_single_value(enviornment, delta_i, n, delay, var, gamma, beta, phi):
    pid = os.getpid()

    mistake_duration = 0
    next_expected_arrival_time = enviornment[0]
    record = Record(n)
    wrong_count = 0
    for arrival_time in enviornment:
        record.append(arrival_time)
        current_length = record.get_length()
        current_sum = record.get_sum()

        if arrival_time > next_expected_arrival_time:
            mistake_duration += arrival_time - next_expected_arrival_time
            wrong_count += 1

        # calculating the value of alpha
        error = arrival_time - next_expected_arrival_time - delay
        delay = delay + gamma * error
        var = var + gamma * (np.abs(error) - var)
        alpha = beta * delay + phi * var

        # calculating the next expected arrival time
        next_expected_arrival_time = alpha + current_sum / current_length + ((current_length + 1) / 2) * delta_i

    detection_time = next_expected_arrival_time - enviornment[-1]
    pa = (len(enviornment) - wrong_count) / len(enviornment)
    cpu_time = psutil.Process(pid).cpu_times().system
    memory = psutil.Process(pid).memory_info().rss / 1024 / 1024

    return mistake_duration, detection_time, pa, cpu_time, memory


def olivier_estimate_for_parameter_array(enviornment, delta_i, n, delay, var, gamma, beta, phi):
    if type(delay) == np.ndarray:
        length = len(delay)
    elif type(var) == np.ndarray:
        length = len(var)
    elif type(gamma) == np.ndarray:
        length = len(gamma)
    elif type(beta) == np.ndarray:
        length = len(beta)
    else:
        length = len(phi)

    mistake_duration = np.zeros(length, dtype=np.float64)
    expected_arrival_time = np.array([enviornment[0] for i in range(length)], dtype=np.float64)
    record = Record(n)
    for arrival_time in enviornment:
        record.append(arrival_time)
        current_length = record.get_length()
        current_sum = record.get_sum()

        duration = -expected_arrival_time + arrival_time
        duration = np.maximum(duration, 0)
        mistake_duration += duration

        # calculating the value of alpha
        error = arrival_time - expected_arrival_time - delay
        delay = delay + gamma * error
        var = var + gamma * (np.abs(error) - var)
        alpha = beta * delay + phi * var

        # calculating the next expected arrival time
        expected_arrival_time = alpha + current_sum / current_length + (
                (current_length + 1) / 2) * delta_i

    return mistake_duration

def olivier_estimate_for_n_array(enviornment, delta_i, n_array, delay, var, gamma, beta, phi):
    length = len(n_array)
    mistake_duration = np.zeros(length, dtype=float)
    expected_arrival_time = np.array([enviornment[0] for i in range(length)])
    record_list = [Record(i) for i in n_array]
    current_length = np.zeros(length)
    current_sum = np.zeros(length, dtype=float)
    for arrival_time in enviornment:
        for inx, record in enumerate(record_list):
            record.append(arrival_time)
            current_length[inx] = record.get_length()
            current_sum[inx] = record.get_sum()

        duration = -expected_arrival_time + arrival_time
        duration = np.maximum(duration, 0)
        mistake_duration += duration

        error = arrival_time - expected_arrival_time - delay
        delay = delay + gamma * error
        var = var + gamma * (np.abs(error) - var)
        alpha = beta * delay + phi * var

        expected_arrival_time = alpha + current_sum / current_length + (
                (current_length + 1) / 2) * delta_i

    return mistake_duration


def olivier_estimate(enviornment, delta_i, n, delay, var, gamma, beta=1, phi=4):
    parameter_dic = {'n': n, 'delay': delay, 'var': var, 'gamma': gamma, 'beta': beta, 'phi': phi}
    int_list = []
    array_list = []
    float_list = []
    for name, parameter in parameter_dic.items():
        if type(parameter) == int:
            int_list.append(name)
        elif type(parameter) == np.ndarray:
            array_list.append(name)
        elif type(parameter) == float:
            float_list.append(name)
        else:
            raise TypeError('The data structure only support int, float and np.ndarray')

    if len(array_list) == 0:
        # means there are no array-type parameters
        return olivier_estimate_for_single_value(enviornment, delta_i, n, delay, var, gamma, beta, phi)
    if len(array_list) == 1:
        # means there is one array-type parameter
        if array_list[0] == 'n':
            # means the array-type parameter is n
            return olivier_estimate_for_n_array(enviornment, delta_i, n, delay, var, gamma, beta, phi)
        else:
            # means the array-type parameter is not n
            return olivier_estimate_for_parameter_array(enviornment, delta_i, n, delay, var, gamma, beta, phi)
    else:
        raise TypeError('There are more than one array in the parameters')

if __name__ == '__main__':
    df = pd.read_csv(r'.\data\Node0\trace.csv')
    df = df[df.site == 8]
    arrival_time_array = np.array(df.timestamp_receive)

    delta_i = 100000000.0
    n = 1000
    # alpha_list = np.array([i for i in range(10001)], dtype=float)
    # alpha_list = 10000
    # gamma = np.array([i / 10 for i in range(10)], dtype=np.float64)
    # gamma = np.array([i for i in range(4000)])
    # gamma = gamma / 10000
    gamma = 0.01
    delay = 0
    var = 0
    beta = 1
    phi = 4

    mistake_duration, detection_time, pa, cpu_time, memory = olivier_estimate_for_single_value(arrival_time_array, delta_i, n, delay,
                                                                                var, gamma, beta, phi)

    print(f"{mistake_duration / 1000000:.2f} ms")
    print(f"{detection_time / 1000000:.2f} ms")
    print(f"{pa:.2%}")
    print(f"{cpu_time:.2f} s")
    print(f"{memory:.2f} MB")
    #
    # plt.plot(n, mistake_duration)
    # plt.show()
