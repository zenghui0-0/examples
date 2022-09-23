import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import mplcyberpunk

"""
category_names = [ 'PASS', 'ABORT', 'RUNNING', 'FAIL']
results = {
    "first": [20, 34, 30, 35], #119
    "second": [25, 32, 34, 20], #111
    "third": [21, 31, 37, 21],   #110
    "fourth":[26, 31, 35, 27],   #119
    "fifth":[21, 31, 37, 21]   #110
}
"""
category_names = ['vg1', 'vg4', '1_520', '4_520', '1_540', '4_540', '1_620', '4_620']
results = {'vg1': [40, 1], 'vg4': [31, 9], '1_520': [42, 5], '4_520': [38, 5], '1_540': [43, 4], '4_540': [32, 11], '1_620': [41, 6], '4_620': [32, 11]}
results2 = [88, 77, 66, 99, 97, 87, 85, 79]

def percentage_stacked_columns(results, category_names):
    # get labels
    labels = list(results.keys())
    # get data
    data = np.array(list(results.values()))
    # sum all data
    sums = np.sum(data, axis=1)
    # color array
    category_colors = plt.get_cmap('RdYlGn')(np.linspace(0.85, 0.15, data.shape[1]))
    # set style
    #plt.figure(figsize=(5,3),facecolor='k')
    #plt.rcParams['axes.facecolor'] = 'k'
    #plt.style.use('cyberpunk')
    #plt.xkcd() # 手绘版
    #plt.style.use('fivethirtyeight')
    plt.style.use('dark_background')
    # set font style
    #plt.rc('font')
    
    
    # remove some frames
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.bottom'] = False
    plt.rcParams['axes.spines.right'] = False

    # initail starts as 0
    starts = np.zeros(len(labels))
    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        length = data[:, i] / sums
        plt.barh(labels, length, left=starts, height=0.5, label=colname, color=color)
        ycenters = starts + length / 2
        r, g, b, _ = color
        text_color = "white" if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(ycenters, data[:, i])):
            plt.text(x, y, str(int(c)), ha='center', va='center', color=text_color)
        starts = starts + length
    #set grid
    plt.grid(axis='x', linestyle='--')
    #set x ray as percentage
    plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
    # set legend
    plt.legend(["pass", "fail"], loc = 3)
    plt.yticks(range(len(list(results.keys()))), labels)
    plt.xlabel('Pass rate')
    plt.title('Libgv promotion test result')
    plt.savefig("./p11.jpg")

def line_chart(results, category_names):
    # set size
    # set style
    plt.style.use('dark_background')
    # set grid
    plt.grid(axis='both', linestyle='--')
    # draw chart
    plt.plot(category_names, results, 'w', marker="D", markersize=5, label="rate")
    plt.title('PASS RATE')
    plt.legend(loc=3)
    for x1, y1 in zip(category_names, results):
        plt.text(x1, y1, str(y1), ha='center', va='bottom', fontsize=10)
    #set y ray as percentage
    plt.gca().yaxis.set_major_formatter(PercentFormatter(100))


#percentage_stacked_columns(results, category_names)
line_chart(results2, category_names)
plt.show()
