import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


def percentage_stacked_columns(results, category_names, legends=None, to_files=False):
    # get labels
    labels = list(results.keys())
    # get data
    data = np.array(list(results.values()))
    # sum all data
    sums = np.sum(data, axis=1)
    # color array
    category_colors = plt.get_cmap('RdYlGn')(np.linspace(0.85, 0.15, data.shape[1]))
    # set style
    plt.style.use('dark_background')
    # remove some frames
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.bottom'] = False
    plt.rcParams['axes.spines.right'] = False

    # initail starts as 0
    starts = np.zeros(len(labels))
    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        length = data[:, i] / sums
        try:
            plt.barh(labels, length, left=starts, height=0.5, label=colname, color=color)
        except Exception as e:
            print("Error: Failed to percentage stacked columns chart wiht matplotlib.")
            return None
        y_centers = starts + length / 2
        r, g, b, _ = color
        text_color = "white" if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(y_centers, data[:, i])):
            plt.text(x, y, str(int(c)), ha='center', va='center', color=text_color)
        starts = starts + length
    # set grid
    plt.grid(axis='x', linestyle='--')
    # set x ray as percentage
    plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
    # set legend
    if legends is not None:
        plt.legend(legends, loc=3)
    plt.yticks(range(len(labels)), labels)
    plt.xlabel('Pass rate')
    plt.title('Libgv promotion test result')
    if to_files:
        tmp_file = "/tmp/plt_percentage_stacked_columns_chart.jpg"
        plt.savefig(tmp_file)
        plt.cla()
        return tmp_file
    return None

def line_chart(results, category_names, to_files=False):
    # set style
    plt.style.use('dark_background')
    #set grid
    plt.grid(axis='both', linestyle='--')
    # draw chart
    try:
        plt.plot(category_names, results, 'w', marker="D", markersize=5, label="rate")
    except Exception as e:
        print("Error: Failed to create line chart wiht matplotlib.")
        return None
    plt.title('PASS RATE')
    plt.legend(loc=3)
    for x1, y1 in zip(category_names, results):
        plt.text(x1, y1, str(y1), ha='center', va='bottom', fontsize=10)
    #set y ray as percentage
    plt.gca().yaxis.set_major_formatter(PercentFormatter(100))
    if to_files:
        tmp_file = "/tmp/plt_line_chart.jpg"
        plt.savefig(tmp_file)
        plt.cla()
        return tmp_file
    return None

if __name__ == "__main__":
    category_names = ['PASS', 'ABORT', 'RUNNING', 'FAIL']
    results = {
        "first": [20, 34, 30, 35],  # 119
        "second": [25, 32, 34, 20],  # 111
        "third": [21, 31, 37, 21],  # 110
        "fourth": [26, 31, 35, 27]  # 119
    }
    percentage_stacked_columns(results, category_names, legends=category_names)
    plt.show()
    plt.cla()
    results2 = [88, 77, 66, 99]
    line_chart(results2, category_names)
