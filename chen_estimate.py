import pandas as pd
import numpy as np
from record import Record
import matplotlib.pyplot as plt


def chen_estimate_for_single_value(enviornment, delta_i, n, alpha):
    mistake_duration = 0
    next_expected_arrival_time = float('inf')
    record = Record(n)
    for arrival_time in enviornment:
        record.append(arrival_time)
        current_length = record.get_length()
        current_sum = record.get_sum()

        if arrival_time > next_expected_arrival_time:
            mistake_duration += arrival_time - next_expected_arrival_time

        if current_length < n:
            next_expected_arrival_time = alpha + current_sum / current_length + ((current_length + 1) / 2) * delta_i
        else:
            next_expected_arrival_time = alpha + current_sum / n + ((n + 1) / 2) * delta_i

    return mistake_duration


def chen_estimate_for_alpha_array(enviornment, delta_i, n, alpha_list):
    mistake_duration = np.zeros(len(alpha_list), dtype=float)
    next_expected_arrival_time = np.array([float('inf') for i in range(len(alpha_list))])
    record = Record(n)
    for arrival_time in enviornment:
        record.append(arrival_time)
        current_length = record.get_length()
        current_sum = record.get_sum()

        duration = -next_expected_arrival_time + arrival_time
        duration = np.maximum(duration, 0)
        mistake_duration += duration

        next_expected_arrival_time = alpha_list + current_sum / current_length + (
                        (current_length + 1) / 2) * delta_i

    return mistake_duration


def chen_estimate_for_n_array(enviornment, delta_i, n_list, alpha):
    mistake_duration = np.zeros(len(n_list), dtype=float)
    next_expected_arrival_time = np.array([float('inf') for i in range(len(n_list))])
    record_list = [Record(i) for i in n_list]
    current_length = np.zeros(len(n_list))
    current_sum = np.zeros(len(n_list), dtype=float)
    for arrival_time in enviornment:
        for inx, record in enumerate(record_list):
            record.append(arrival_time)
            current_length[inx] = record.get_length()
            current_sum[inx] = record.get_sum()

        duration = -next_expected_arrival_time + arrival_time
        duration = np.maximum(duration, 0)
        mistake_duration += duration

        next_expected_arrival_time = alpha + current_sum / current_length + (
                (current_length + 1) / 2) * delta_i

    return mistake_duration

def chen_estimate(enviornment, delta_i, n_list, alpha_list):
    if type(n_list) != np.ndarray and type(n_list) != int:
        raise TypeError('The data type of n can only be numpy array or int')
    if type(alpha_list) != np.ndarray and type(alpha_list) != int:
        raise TypeError('The data type of alpha can only be numpy array or int')

    if type(n_list) == np.ndarray and type(alpha_list) == np.ndarray:
        raise TypeError('The data type of n and alpha cannot be both array')
    elif type(alpha_list) == np.ndarray:
        mistake_duration = chen_estimate_for_alpha_array(enviornment, delta_i, n_list, alpha_list)
        return mistake_duration
    elif type(n_list) == np.ndarray:
        mistake_duration = chen_estimate_for_n_array(enviornment, delta_i, n_list, alpha_list)
        return mistake_duration
    else:
        mistake_duration = chen_estimate_for_single_value(enviornment, delta_i, n_list, alpha)
        return mistake_duration


if __name__ == '__main__':
    df = pd.read_csv(r'.\data\Node0\trace.csv')
    df = df[df.site == 8]
    arrival_time_array = np.array(df.timestamp_receive)

    delta_i = 100000000.0
    n_list = np.array([i for i in range(1, 1001)])
    # n_list = 1000
    # alpha_list = np.array([i for i in range(10001)], dtype=float)
    alpha_list = 10000

    mistake_duration = chen_estimate(arrival_time_array, delta_i, n_list, alpha_list)

    # print(mistake_duration)

    plt.plot(n_list, mistake_duration)
    plt.show()