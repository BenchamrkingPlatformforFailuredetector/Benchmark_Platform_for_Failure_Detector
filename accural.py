import pandas as pd
import numpy as np
from Extension.record import Record
import matplotlib.pyplot as plt
import scipy.stats as st
import os
import psutil
import time
import multiprocessing
import copy


def accural_estimate_for_single_value(enviornment, delta_i, n, phi):
    pid = os.getpid()

    mistake_duration = 0
    next_expected_arrival_time = enviornment[0]
    record = Record(n)
    wrong_count = 0

    for arrival_time in enviornment:
        record.append(arrival_time)
        difference = record.get_difference()

        if arrival_time > next_expected_arrival_time:
            mistake_duration += arrival_time - next_expected_arrival_time
            wrong_count += 1

        # Then start to calculate the expected arrival time
        if len(difference) == 0:
            # Means there are only one arrival time in the record
            next_expected_arrival_time = arrival_time + delta_i
        elif len(difference) == 1:
            # Means there are only two arrival time in the record
            next_expected_arrival_time = arrival_time + difference[0]
        else:
            mean = np.mean(difference)
            scale = np.std(difference)
            expected_interval = st.norm.ppf(1 - np.power(0.1, phi), loc=mean, scale=scale)
            next_expected_arrival_time = arrival_time + expected_interval

    detection_time = next_expected_arrival_time - enviornment[-1]
    pa = (len(enviornment) - wrong_count) / len(enviornment)
    cpu_time = psutil.Process(pid).cpu_times().system
    memory = psutil.Process(pid).memory_info().rss / 1024 / 1024

    return mistake_duration, detection_time, pa, cpu_time, memory
    # q.put( (mistake_duration, detection_time, pa, cpu_time, memory) )


def accural_estimate_for_phi_array(enviornment, delta_i, n, phi_array):
    length = len(phi_array)
    mistake_duration = np.zeros(length, dtype=float)
    expected_arrival_time = np.array([enviornment[0] for i in range(length)], dtype=float)
    record = Record(n)

    for arrival_time in enviornment:
        record.append(arrival_time)
        difference = record.get_difference()

        duration = -expected_arrival_time + arrival_time
        duration = np.maximum(duration, 0)
        mistake_duration += duration

        # Then start to calculate the expected arrival time
        if len(difference) == 0:
            # Means there are only one arrival time in the record
            expected_arrival_time = arrival_time + delta_i
        elif len(difference) == 1:
            # Means there are only two arrival time in the record
            expected_arrival_time = arrival_time + difference[0]
        else:
            mean = np.mean(difference)
            scale = np.std(difference)
            expected_interval = st.norm.ppf(1 - np.power(0.1, phi_array), loc=mean, scale=scale)
            expected_arrival_time = arrival_time + expected_interval
    return mistake_duration


def accural_estimate_for_n_array(enviornment, delta_i, n_array, phi):
    length = len(n_array)
    mistake_duration = np.zeros(length, dtype=float)
    expected_arrival_time = np.array([enviornment[0] for i in range(length)], dtype=float)
    record_list = [Record(i) for i in n_array]
    interval_list = np.zeros(length, dtype=float)

    for arrival_time in enviornment:
        for inx, record in enumerate(record_list):
            record.append(arrival_time)
            difference = record.get_difference()

            # Then start to calculate the expected arrival time
            if len(difference) == 0:
                # Means there are only one arrival time in the record
                expected_interval = delta_i
            elif len(difference) == 1:
                # Means there are only two arrival time in the record
                expected_interval = difference[0]
            else:
                mean = np.mean(difference)
                scale = np.std(difference)
                expected_interval = st.norm.ppf(1 - np.power(0.1, phi), loc=mean, scale=scale)

            interval_list[inx] = expected_interval

        duration = -expected_arrival_time + arrival_time
        duration = np.maximum(duration, 0)
        mistake_duration += duration

        expected_arrival_time = arrival_time + interval_list
    return mistake_duration


def accural_estimate(enviornment, delta_i, n, phi):
    if type(n) != np.ndarray and type(n) != int:
        raise TypeError('The data type of n can only be numpy array or int')
    if type(phi) != np.ndarray and type(phi) != int:
        raise TypeError('The data type of alpha can only be numpy array or int')

    if type(n) == np.ndarray and type(phi) == np.ndarray:
        raise TypeError('The data type of n and alpha cannot be both array')
    elif type(phi) == np.ndarray:
        mistake_duration = accural_estimate_for_phi_array(enviornment, delta_i, n, phi)
    elif type(n) == np.ndarray:
        mistake_duration = accural_estimate_for_n_array(enviornment, delta_i, n, phi)
    else:
        mistake_duration = accural_estimate_for_single_value(enviornment, delta_i, n, phi)
    return mistake_duration


if __name__ == '__main__':
    delta_i = 100000000.0
    n = 1000
    phi = 10
    node_list = [0, 1, 3, 5, 6, 7, 8, 9]
    pool = multiprocessing.Pool(processes=56)
    results = []
    for i in node_list:
        receive_from_node_list = copy.deepcopy(node_list)
        receive_from_node_list.remove(i)
        for j in receive_from_node_list:
            df = pd.read_csv(r'.\data\Node{}\trace.csv'.format(i))
            df = df[df.site == j]
            arrival_time_array = np.array(df.timestamp_receive)
            results.append(pool.apply_async(accural_estimate_for_single_value, (arrival_time_array, delta_i, n, phi,)))

    pool.close()
    pool.join()
    mistake_duration_list = []
    detection_time_list = []
    pa_list = []
    cpu_time_list = []
    memory_list = []
    for res in results:
        mistake_duration_list.append(res.get()[0] / 1000000)
        detection_time_list.append(res.get()[1] / 1000000)
        pa_list.append(res.get()[2])
        cpu_time_list.append(res.get()[3])
        memory_list.append(res.get()[4])

    mistake_duration_array = np.array(mistake_duration_list)
    detection_time_array = np.array(detection_time_list)
    pa_array = np.array(pa_list)
    cpu_time_array = np.array(cpu_time_list)
    memory_array = np.array(memory_list)

    print(f"average mistake duration: {np.mean(mistake_duration_array):.2f} ms")
    print(f"average detection time: {np.mean(detection_time_array):.2f} ms")
    print(f"average pa: {np.mean(pa_array):.2%}")
    print(f"average cpu time: {np.mean(cpu_time_array):.2f} s")
    print(f"average memory: {np.mean(memory_array):.2f} MB")
    print(f"std detection time: {np.std(detection_time_array):.2f} ms")
    print(f"std pa: {np.std(pa_array):.2%}")

    # df = pd.read_csv(r'.\data\Node0\trace.csv')
    # df = df[df.site == 8]
    # arrival_time_array = np.array(df.timestamp_receive)
    #
    # delta_i = 100000000.0
    # # n = 1000
    # n = 1000
    # phi = 1
    # # phi = np.array([i for i in range(1000)])
    # # phi = phi / 100
    #
    # mistake_duration, detection_time, pa, cpu_time, memory = accural_estimate_for_single_value(arrival_time_array, delta_i, n, phi)
    #
    # print(f"{mistake_duration / 1000000:.2f} ms")
    # print(f"{detection_time / 1000000:.2f} ms")
    # print(f"{pa:.2%}")
    # print(f"{cpu_time:.2f} s")
    # print(f"{memory:.2f} MB")
    # #
    # # # plt.plot(n, mistake_duration)
    # # # plt.show()
