import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

file = 'mosei.csv'
df = pd.read_csv(file)
sentiments = df['sentiment']

dict = {'-3':0, "-2":0, '-1':0, "0":0, '1':0, '2':0, '3':0}

for idx in range(len(sentiments)): 
    sent = np.ceil(sentiments[idx])
    dict[str(int(sent))] += 1

print(idx)
print(dict)

comb_dict = {}
comb_dict['neg'] = dict['-3'] + dict['-2']
comb_dict['weakly_neg'] = dict['-1']
comb_dict['neutral'] = dict['0']
comb_dict['weakly pos'] = dict['1']
comb_dict['pos'] = dict['2'] + dict['3']

print(comb_dict)

fig = plt.figure(figsize = (10, 5))
plt.bar([-2, -1, 0, 1, 2], comb_dict.values(), color='blue', width=0.4)
plt.show()