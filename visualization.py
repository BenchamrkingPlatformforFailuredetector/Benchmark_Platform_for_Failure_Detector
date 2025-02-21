import matplotlib.pyplot as plt
import pandas as pd


def horizontal_bar_chart(scores, metrics=None):
    scores: pd.DataFrame = pd.DataFrame(scores)
    if metrics is None:
        metrics = scores.index  # ['total', 'detection time', 'pa', 'mistake duration', 'CPU time', 'memory usage']

    x_data = scores.keys()  # ['Accural', 'Chen', 'Olivier']

    bar_width = 0.1  # width of a single bar, can be dynamic
    interval = 0.01  # interval within a group of bars

    for i, m in enumerate(reversed(metrics)):
        y_data = scores.loc[m]
        y_range = [i * bar_width + i * interval + p for p in range(len(x_data))]
        plt.barh(y=y_range, width=y_data, height=bar_width, label=m)
        for x, y in zip(y_range, y_data):
            x_position = y + 1  # manually set
            y_position = x - 0.03  # manually set
            plt.text(x_position, y_position, y, ha='center', va='bottom')

    plt.xticks([i for i in range(0, 110, 10)])  # [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    y_ticks = [((len(metrics) - 1) * bar_width + (len(metrics) - 1) * interval) / 2 + p for p in range(len(x_data))]
    plt.yticks(y_ticks, x_data)

    plt.ylabel("Algorithm")
    plt.xlabel("Score")
    plt.title("Performance Overview")

    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend(reversed(handles), reversed(labels))

    plt.show()


def line_chart(scores, metrics=None):
    scores: pd.DataFrame = pd.DataFrame(scores)
    if metrics is None:
        x_data = scores.index  # ['total', 'detection time', 'pa', 'mistake duration', 'CPU time', 'memory usage']
    else:
        x_data = metrics

    algorithms = scores.keys()  # ['Accural', 'Chen', 'Olivier']

    for a in algorithms:
        y_data = scores[a][x_data]

        plt.plot(x_data, y_data, label=a, marker='o')
        for x, y in zip(x_data, y_data):
            plt.text(x, y, y, ha='center', va='bottom')

    plt.yticks([i for i in range(0, 110, 10)])  # [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    plt.xlabel("Metric")
    plt.ylabel("Score")
    plt.title("Performance Overview")

    plt.legend()
    plt.show()


if __name__ == '__main__':
    # data = {
    #     "Accural": {"total": 100, "detection time": 100, "pa": 100, "mistake duration": 100, "CPU time": 100,
    #                 "memory usage": 100},
    #     "Chen": {"total": 80, "detection time": 90, "pa": 80, "mistake duration": 70, "CPU time": 95,
    #              "memory usage": 60},
    #     "Olivier": {"total": 90, "detection time": 75, "pa": 95, "mistake duration": 80, "CPU time": 70,
    #                 "memory usage": 80},
    # }

    data = {
        'accural': {'detection time': 60.0, 'detection time std': 70.4, 'pa': 90.0, 'pa std': 90.0,
                    'mistake duration': 90.0, 'CPU time': 49.1, 'memory usage': 62.3, 'total': 74.2},
        'bertier': {'detection time': 85.1, 'detection time std': 79.3, 'pa': 81.7, 'pa std': 81.2,
                    'mistake duration': 81.9, 'CPU time': 83.2, 'memory usage': 92.1, 'total': 83.1},
        'chen': {'detection time': 89.4, 'detection time std': 81.6, 'pa': 65.6, 'pa std': 60.3,
                 'mistake duration': 60.0, 'CPU time': 95.3, 'memory usage': 92.2, 'total': 76.9}
    }

    df = pd.DataFrame(data)

    horizontal_bar_chart(df)
    line_chart(df)
