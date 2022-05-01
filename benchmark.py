def gen_linear(max_value, min_value, max_score, min_score):
    slope = (max_score - min_score) / (max_value - min_value)
    intersect = max_score - slope * max_value

    def linear(x):
        score = slope * x + intersect
        return score if 0 <= score <= 100 else 0 if score < 0 else 100

    return linear


def calc_score(metric_data, weights=(0.1, 0.2, 0.2, 0.1, 0.1, 0.15, 0.15)):
    #  np.mean(mistake_duration_array), np.mean(detection_time_array), np.mean(pa_array), np.mean(cpu_time_array), \
    #  np.mean(memory_array), np.std(detection_time_array), np.std(pa_array)
    mistake_duration_func = gen_linear(9337.38, 2356274.1, 90, 60)
    detection_time_func = gen_linear(99.98, 105.75, 90, 60)
    pa_func = gen_linear(0.9979, 0.6833, 90, 60)
    cpu_time_func = gen_linear(0.33, 0.53, 90, 60)
    memory_func = gen_linear(84.63, 113.12, 90, 60)
    detection_time_std_func = gen_linear(0.32, 2.39, 90, 60)
    pa_std_func = gen_linear(0.0008, 0.0841, 90, 60)

    funcs = (mistake_duration_func, detection_time_func, pa_func, cpu_time_func, memory_func,
             detection_time_std_func, pa_std_func)

    names = ("mistake duration", "detection time", "pa", "CPU time", "memory usage", "detection time std", "pa std")

    scores = {}
    total_score = 0
    for i in range(len(metric_data)):
        unweighted_score = funcs[i](metric_data[i])
        scores[names[i]] = round(unweighted_score, 1)
        total_score += round(unweighted_score * weights[i], 1)
    scores["total"] = total_score
    return scores


def feed_to_visual(algo_name, metric_data, visual_data=None, weights=(0.1, 0.2, 0.2, 0.1, 0.1, 0.15, 0.15)):
    # visual data is the argument you can directly pass into the functions in visualization.py
    if visual_data is None:
        visual_data = {}
    visual_data.update({algo_name: calc_score(metric_data, weights)})
    return visual_data


if __name__ == '__main__':
    accural_data = (9364.899149998326, 105.74858808928572, 0.9979379611895526, 0.6029575892857143, 110.89264787946429,
                    1.6750364820071866, 0.0008348593499185055)
    bertier_data = (644043.3404513125, 100.91581011049107, 0.9112516167575638, 0.375, 82.63825334821429,
                    1.059675334140229, 0.02535474631119393)
    chen_data = (2353438.4988998906, 100.09092747600445, 0.7423359876953095, 0.294921875, 82.54171316964286,
                 0.9009301070789003, 0.08329813139516726)
    visual_input = {}
    feed_to_visual("accural", accural_data, visual_input)
    feed_to_visual("bertier", bertier_data, visual_input)
    feed_to_visual("chen", chen_data, visual_input)
    print(visual_input)
