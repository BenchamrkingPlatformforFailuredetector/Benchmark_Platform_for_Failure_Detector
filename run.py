import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import psutil
import time
import multiprocessing
import copy


def translate(language_file, record_class):
    with open(r'.\Extension\{}.txt'.format(language_file)) as f:
        language = f.read()
    language = language.replace('\n', '')
    language = language.replace(' ', '')
    language_list = language.split(';')
    class_name = record_class.capitalize()
    code = """from Extension.{} import {}\nimport os\nimport psutil\nimport numpy as np\nimport math\n\n""".format(
        record_class, class_name)
    code += """pid = os.getpid()\nnext_expected_arrival_time = enviornment[0]\nmistake_duration = 0\nwrong_count = 0\n"""
    for i in language_list:
        if i != '':
            label = i.split(':')[0]
            content = i.split(':')[1]
            if label == 'Outside':
                # means this content should be added to the code outside the for loop
                for j in content.split(','):
                    if j[0] == 'N':
                        input_list = j.split('=')[1].split('&')
                        str = ','.join(input_list)
                        code += '{}={}({})'.format(record_class, class_name, str)
                    else:
                        code += j + '\n'
                    code += '\n'

                code += 'for arrival_time in enviornment:\n' + '\t{}.append(arrival_time)\n'.format(record_class)

            if label == 'Inside':
                # means this content should be added to the code inside the for loop
                for j in content.split(','):
                    parameter = j.split('=')[0]
                    value = j.split('=')[1].replace('object->', '{}.'.format(record_class)).replace('A', 'arrival_time') \
                        .replace('E', 'next_expected_arrival_time')
                    code += '\t{}={}'.format(parameter, value) + '\n'
                code += '\tif arrival_time > next_expected_arrival_time:\n'
                code += '\t\tmistake_duration += arrival_time - next_expected_arrival_time\n'
                code += '\t\twrong_count += 1\n'

            if label == 'EA':
                # means this content is used to calculate the next expected arrival time
                code += '\tnext_expected_arrival_time={}\n'.format(
                    content.replace('A', 'arrival_time').replace('E', 'next_expected_arrival_time'))

    code += 'detection_time = next_expected_arrival_time - enviornment[-1]\nif detection_time < 0:\n'
    code += '\tdetection_time = 0\npa = (len(enviornment) - wrong_count) / len(enviornment)\n'
    code += 'cpu_time = psutil.Process(pid).cpu_times().system\n'
    code += 'memory = psutil.Process(pid).memory_info().rss / 1024 / 1024\n'

    return code


def run(enviornment, language_file, record_class):
    code = translate(language_file, record_class)
    g = {}
    exec(code, {'enviornment': enviornment, 'delta': 100000000.0}, g)
    return g['mistake_duration'], g['detection_time'], g['pa'], g['cpu_time'], g['memory']


def run_all(language_file, record_class='record'):
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
            results.append(pool.apply_async(run, (arrival_time_array, language_file, record_class,)))

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

    return np.mean(detection_time_array), np.mean(pa_array), np.std(detection_time_array), np.std(pa_array), \
           np.mean(mistake_duration_array), np.mean(cpu_time_array), np.mean(memory_array)


if __name__ == '__main__':
    average_detection_time, average_pa, std_detection_time, std_pa, average_mistake_duration, average_cpu_time, \
    average_memory = run_all('accural', 'newrecord')

    print(f"average mistake duration: {average_mistake_duration:.2f} ms")
    print(f"average detection time: {average_detection_time:.2f} ms")
    print(f"average pa: {average_pa:.2%}")
    print(f"average cpu time: {average_cpu_time:.2f} s")
    print(f"average memory: {average_memory:.2f} MB")
    print(f"std detection time: {std_detection_time:.2f} ms")
    print(f"std pa: {std_pa:.2%}")
