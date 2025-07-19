import os
import datetime
import matplotlib.pyplot as plt
from numpy import arange
import pandas

sadPeopleDict = pandas.read_csv("csvfiles/sadPeopleOverTime.csv")
xLabel = sadPeopleDict.columns[0]
yLabel = sadPeopleDict.columns[1]

settingsFile = open("settings.txt", "r")
settingsFile.readline()
settingsFile.readline()
settingsFile.readline()
maxHours = int(settingsFile.readline().replace("\n", ""))
figWidth = int(settingsFile.readline().replace("\n", ""))
settingsFile.close()

#configure axes
plt.figure("Sad People Over Time", figsize=(figWidth, 6))
plt.xlim(0, maxHours)
plt.ylim(0, 150000)
plt.xticks(arange(0, maxHours, 5))
plt.yticks(arange(0, 150000, 50000))
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

#configure labels/titles
plt.xlabel(xLabel)
plt.ylabel(yLabel)
plt.title("Sad People Over Time (since May 28, 12:00 PM)")

#plot data
plt.plot(sadPeopleDict[xLabel].tolist(), sadPeopleDict[yLabel].tolist(), color="blue")

# draw lines every 24 hours
for i in range(24, maxHours + 1, 24):
    plt.axvline(x = i, color = 'y', label = 'axvline - full height')

#shade nights (optional)
'''for i in range(12, maxHours + 1, 24):
    plt.axvspan(i, i + 12, color='b', alpha=0.5, lw=0)'''

plt.axvline(x = 80, color = 'r', label = 'axvline - full height')

#display
plt.savefig("images/sadPeopleOverTime.png")
plt.show()