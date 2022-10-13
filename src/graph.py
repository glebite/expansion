"""
"""
import time
offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
offset = offset / 60 / 60 * -1
import pandas as pd
from matplotlib import pyplot as plt
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
df = pd.read_csv("../data.txt", header=None)
df.columns = ['Date', 'Okay', 'Blocked', 'Down', 'Other']
partial_df = df.tail(32)
print(partial_df.tail(1))
partial_df.plot(x='Date', y = ['Okay', 'Blocked', 'Down', 'Other'])
plt.grid()
plt.title('Criteria over time')
plt.ylabel('Criteria count')
plt.xlabel(f'Time (GMT{offset})')
plt.xticks(rotation=90)
plt.savefig('graph.png')
