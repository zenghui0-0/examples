import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

plt.title('Scores by group and gender')

N = 13
ind = np.arange(N)  #[ 0  1  2  3  4  5  6  7  8  9 10 11 12]
plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'G13'))

plt.ylabel('Pass rate')
#plt.yticks(np.arange(0, 100, 20))

Bottom = (52, 49, 48, 47, 44, 43, 41, 41, 40, 38, 36, 31, 29)
Center = (38, 40, 45, 42, 48, 51, 53, 54, 57, 59, 57, 64, 62)
Top = (10, 11, 7, 11, 8, 6, 6, 5, 3, 3, 7, 5, 9)

d = []
for i in range(0, len(Bottom)):
    sum = Bottom[i] + Center[i]
    d.append(sum)

width = 0.35  # 设置条形图一个长条的宽度
p1 = plt.bar(ind, Bottom, width, color='blue') 
p2 = plt.bar(ind, Center, width, bottom=Bottom,color='green')  
p3 = plt.bar(ind, Top, width, bottom=d,color='red')


#纵轴设置为百分比
plt.gca().yaxis.set_major_formatter(PercentFormatter(100))

plt.legend((p1[0], p2[0], p3[0]), ('Bottom', 'Center', 'Top'),loc = 3)

plt.show()
