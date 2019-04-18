import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#data=pd.read_csv('data/20w.csv')#导入csv文件


data = pd.read_csv('data/20w.csv',encoding='utf-8')

table = pd.pivot_table(data,index="adapter_name",values=['not Partition (old_code)','partition(new code)','cross-partition(new code)','cross-partition(old code)'])

print(table)

df = pd.DataFrame(table)

print(df.plot())
plt.xticks(rotation=270)
plt.grid()
plt.title('20W test data')
plt.show()