import argparse
import glob
import os
import sys
import pickle
import time


def main():

    time.sleep(3)

    # Input:
    traces_dir = args.t  # "C:\Users\Administrator\PycharmProjects\Benchmark_Platform_for_Failure_Detector\data"
    extension_dir = args.E  # "C:\Users\Administrator\PycharmProjects\Benchmark_Platform_for_Failure_Detector\Extension"
    record_file = args.R  # "C:\Users\Administrator\PycharmProjects\Benchmark_Platform_for_Failure_Detector\Extension\record.py"

    # How to iterate through a directory:
    # results = glob.glob(os.path.join(extension_dir, "*.txt"))
    # for r in results:
    #     base_name = os.path.basename(r)
    #     print(base_name)
    # print(results)

    # Output:
    # Data must look like this!
    # {fd_name: (detection time, detection time std, pa, pa std, mistake duration, cpu, memory)}
    data = {"accural": (105.74858808928572, 1.6750364820071866, 0.9979379611895526, 0.0008348593499185055,
                        9364.899149998326, 0.6029575892857143, 110.89264787946429),
            "bertier": (100.91581011049107, 1.059675334140229, 0.9112516167575638, 0.02535474631119393,
                        644043.3404513125, 0.375, 82.63825334821429),
            "chen": (100.09092747600445, 0.9009301070789003, 0.7423359876953095, 0.08329813139516726,
                     2353438.4988998906, 0.294921875, 82.54171316964286)}
    pickle.dump(data, sys.stdout.buffer)  # Must include this line!


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    cwd = os.getcwd()
    parser.add_argument("-t", default=os.path.join(cwd, "data"), help="Directory to traces folder")
    parser.add_argument("-E", default=os.path.join(cwd, "Extension"), help="Directory to Extension folder")
    parser.add_argument("-R", default=os.path.join(cwd, "Extension\\record.py"), help="Path to Record file")
    args = parser.parse_args()
    main()
