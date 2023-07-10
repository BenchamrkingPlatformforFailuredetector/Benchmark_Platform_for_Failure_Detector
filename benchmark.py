def gen_linear(max_value, min_value, max_score, min_score):
    slope = (max_score - min_score) / (max_value - min_value)
    intersect = max_score - slope * max_value

    def linear(x):
        score = slope * x + intersect
        return score if 0 <= score <= 100 else 0 if score < 0 else 100

    return linear


def calc_score(metric_data, weights=(0.2, 0.15, 0.2, 0.15, 0.1, 0.1, 0.1)):
    mistake_duration_func = gen_linear(9337.38, 2356274.1, 90, 60)
    detection_time_func = gen_linear(99.98, 105.75, 90, 60)
    pa_func = gen_linear(0.9979, 0.6833, 90, 60)
    cpu_time_func = gen_linear(0.33, 0.53, 90, 60)
    memory_func = gen_linear(84.63, 113.12, 90, 60)
    detection_time_std_func = gen_linear(0.32, 2.39, 90, 60)
    pa_std_func = gen_linear(0.0008, 0.0841, 90, 60)

    funcs = (detection_time_func, detection_time_std_func, pa_func, pa_std_func, mistake_duration_func,
             cpu_time_func, memory_func)

    names = ("detection time", "detection time std", "pa", "pa std", "mistake duration", "CPU time", "memory usage")

    scores = {}
    total_score = 0
    for i in range(len(metric_data)):
        unweighted_score = funcs[i](metric_data[i])
        scores[names[i]] = float(f"{round(unweighted_score, 1):.1f}")
        total_score += round(unweighted_score * weights[i], 1)
    total_score = float(f"{total_score:.1f}")
    scores["total"] = total_score
    return scores


def feed_to_visual(algo_name, metric_data, visual_data=None, weights=(0.2, 0.15, 0.2, 0.15, 0.1, 0.1, 0.1)):
    # visual data is the argument you can directly pass into the functions in visualization.py
    if visual_data is None:
        visual_data = {}
    visual_data.update({algo_name: calc_score(metric_data, weights)})
    return visual_data


if __name__ == '__main__':
    accural_data = (105.74858808928572, 1.6750364820071866, 0.9979379611895526, 0.0008348593499185055,
                    9364.899149998326, 0.6029575892857143, 110.89264787946429)
    bertier_data = (100.91581011049107, 1.059675334140229, 0.9112516167575638, 0.02535474631119393, 644043.3404513125,
                    0.375, 82.63825334821429)
    chen_data = (100.09092747600445, 0.9009301070789003, 0.7423359876953095, 0.08329813139516726,
                 2353438.4988998906, 0.294921875, 82.54171316964286)
    visual_input = {}
    feed_to_visual("accural", accural_data, visual_input)
    feed_to_visual("bertier", bertier_data, visual_input)
    feed_to_visual("chen", chen_data, visual_input)
    print(visual_input)
