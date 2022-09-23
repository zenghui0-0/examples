import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
 
category_names = [ 'PASS', 'ABORT', 'RUNNING', 'FAIL']
results = {
    "first": [20, 34, 30, 35], #119
    "second": [25, 32, 34, 20], #111
    "third": [21, 31, 37, 21],   #110
    "fourth":[26, 31, 35, 27]   #119
}

def survey(results, category_names):
    # get labels
    labels = list(results.keys())
    # get data
    data = np.array(list(results.values()))
    # sum all data
    sums = np.sum(data, axis=1)
    # color array
    category_colors = plt.get_cmap('RdYlGn')(np.linspace(0.85, 0.15, data.shape[1]))

    # initail starts as 0
    starts = np.zeros(len(labels))
    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        height = data[:, i] / sums
        print(i, height, starts)
        plt.bar(labels, height, bottom=starts, width=0.5, label=colname, color=color)
        xcenters = starts + height / 2
        r, g, b, _ = color
        text_color = "white" if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(xcenters, data[:, i])):
            plt.text(y, x, str(int(c)), ha='center', va='center', color=text_color, rotation=90)
        starts = starts + height

    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    # set legend
    plt.legend(category_names, loc = 3)
    plt.xticks(range(len(category_names)), labels)
    plt.ylabel('Pass rate')
    plt.title('Libgv promotion test result')
    plt.show()

survey(results, category_names)
