from matplotlib import pyplot as plt
import csv
import pandas as pd
import json


df = pd.read_csv("results.csv")
divisions = df.Division
allDivisions = list(set(list(divisions)))

finishTimeData = dict.fromkeys(allDivisions)
for i, _ in finishTimeData.items():
    finishTimeData[i] = []

for i, r in df.iterrows():
    timeStr = r.Final
    components = timeStr.split(":")
    timeMins = (int(components[0]) * 60) + int(components[1]) + (int(components[2]) / 60)
    div = r.Division
    divisionTimes = finishTimeData.get(div)
    finishTimeData.get(div).append(timeMins)

# print(json.dumps(finishTimeData, indent=3))

fig = plt.figure()
ax1 = fig.add_subplot(111)

for i, (div, data) in enumerate(finishTimeData.items()):
    ax1.scatter(data, [i for _ in range(len(data))], label=div)
plt.legend()
plt.show()
