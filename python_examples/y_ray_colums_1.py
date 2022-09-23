import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
 
labels = ['G1', 'G2', 'G3', 'G4', 'G5']
first = [20, 34, 30, 35, 27]
second = [25, 32, 34, 20, 25]
third = [21, 31, 37, 21, 28]
fourth = [26, 31, 35, 27, 21]
#data = [first, second, third, fourth]
data = [first, second]
x = range(len(labels))
width = 0.35
 
# 将bottom_y元素都初始化为0
bottom_y = np.zeros(len(labels))
data = np.array(data)
# 按列计算计算每组柱子的总和，为计算百分比做准备
sums = np.sum(data, axis=0)
print(sums)
color = ["green", "red"]
for i in data:
    print(i)
    # 计算每个柱子的高度，即百分比
    y = i / sums
    plt.barh(x, y, width, color=color.pop(0), left=bottom_y)
    # set text on columns
    #plt.text()
    # 计算bottom参数的位置
    bottom_y = y + bottom_y

#横轴设置为百分比
plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
# set legend
plt.legend(["pass", "fail"], loc = 3)
#plt.legend(["pass", "fail"], frameon=False,bbox_to_anchor=(1.01,1))
plt.yticks(x, labels)
plt.xlabel('Pass rate')
plt.title('Libgv promotion test result')
plt.show()
