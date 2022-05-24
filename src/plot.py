from __future__ import unicode_literals

import matplotlib.pyplot as plt
import numpy as np
import random
from bidi.algorithm import get_display
wordcount = open('../data/word_count/count.txt', 'r', encoding='utf8').read().splitlines()
x = []
y = []
for i in range(10):
    row = wordcount[i].split(' : ')
    y.append(int(row[1]))
    x.append(get_display(row[0]))

rnd = []
for i in range(10):
    r = random.random()
    b = random.random()
    g = random.random()
    rnd.append((r, g, b))
plt.bar(x, y, width=0.7, bottom=None, align='center', data=None ,color = rnd )
plt.xticks(fontsize=6)

plt.savefig('../data/plot_img/plot.png')

plt.show()