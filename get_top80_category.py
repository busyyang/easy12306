import re
import matplotlib.pyplot as plt
import numpy as np

pattern = re.compile(r'[^\u4e00-\u9fa5]')
with open('texts.log', 'r', encoding='utf-8') as f:
    category = f.readlines()

category = [re.sub(pattern, '', c) for c in category]
dict_cat = {}
for c in category:
    if c in dict_cat.keys():
        dict_cat[c] += 1
    else:
        dict_cat[c] = 1

list_cat = sorted(dict_cat.items(), key=lambda x: x[1], reverse=True)
x = np.array(list_cat)[:, 0]
y = np.array(list_cat)[:, 1]

with open('text_top_80.txt', 'w') as f:
    for i in range(80):
        f.writelines([x[i], '\n'])

plt.plot(y)
plt.show()
