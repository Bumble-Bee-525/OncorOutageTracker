import os
import datetime
import matplotlib.pyplot as plt
from numpy import arange
import pandas
import time
import re


#set reference date
referenceDate = datetime.datetime(2024, 5, 28, 12, 0, 0)
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# get time since the reference date for a file
def getTimeSinceReference(fName):
    time = fName.split(".")[0]
    time = time.split("-")
    if time[4] == "PM" and not time[2] == "12":
        time[2] = int(time[2]) + 12
    
    if time[4] == "AM" and time[2] == "12":
        time[2] = 0

    time = datetime.datetime(2024, months.index(time[0]) + 1, int(time[1]), int(time[2]), int(time[3]))

    time = time - referenceDate
    time = time.total_seconds() / 3600
    time = round(time, 2)
    return time

# set the paths for unprocessed and processed 
settingsFile = open("settings.txt", "r")
unprocessedFolder = settingsFile.readline().replace("\n", "")
processedFolder = settingsFile.readline().replace("\n", "")
downloadPath = settingsFile.readline().replace("\n", "")
maxHours = int(settingsFile.readline().replace("\n", ""))
figWidth = int(settingsFile.readline().replace("\n", ""))
settingsFile.close()

def processNewData():
    # get all filenames of unprocessed files
    filenames = os.listdir(unprocessedFolder)
    print(filenames)
    #sort files by order by date
    filenames.sort(key=getTimeSinceReference)

    #get outage db
    outageDB = open("csvfiles/outagesOverTime.csv", "a")
    peopleDB = open("csvfiles/sadPeopleOverTime.csv", "a")

    # for each unprocessed outage file...
    for filename in filenames:
        if filename.endswith(".txt"):
            #open file
            fileHandle = open("unprocessed/" + filename, "r")
            
            # get number of outages
            data = fileHandle.readline().split(",")
            outages = data[0]
            people = data[1]
            print(data)

            #get time of record
            time = getTimeSinceReference(filename)        

            # add to csv
            outageDB.write("\n")
            outageDB.write(str(time) + "," + outages)

            peopleDB.write("\n")
            peopleDB.write(str(time) + "," + people)
            fileHandle.close()

            # move file to processed folder
            os.rename(unprocessedFolder + "/" + filename, processedFolder + "/" + filename)

    outageDB.close()
    peopleDB.close()

    outageDict = pandas.read_csv("csvfiles/outagesOverTime.csv")
    xLabel = outageDict.columns[0]
    yLabel = outageDict.columns[1]

    #configure axes
    plt.figure("Oncor Outages Over Time", figsize=(figWidth, 6))
    plt.xlim(0, maxHours)
    plt.ylim(0, 16500)
    plt.xticks(arange(0, maxHours, 5))
    plt.yticks(arange(0, 16500, 1000))
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    #configure labels/titles
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title("Outages over Time (since May 28, 12:00 PM)")

    #plot data
    plt.plot(outageDict[xLabel].tolist(), outageDict[yLabel].tolist(), color="blue")

    # draw lines every 24 hours
    for i in range(24, maxHours + 1, 24):
        plt.axvline(x = i, color = 'y', label = 'axvline - full height')

    #shade nights (optional)
    '''for i in range(12, maxHours + 1, 24):
        plt.axvspan(i, i + 12, color='b', alpha=0.5, lw=0)'''

    plt.axvline(x = 80, color = 'r', label = 'axvline - full height')

    #display
    plt.savefig("images/outageOverTime.png")
    #plt.show()


#processNewData()

while True:
    print("checking")
    downloads = os.listdir(downloadPath)
    newItems = []

    # for each file, check if it's an oncor update
    for file in downloads:
        if len(file) > 6 and file.endswith(".txt"):
            if file[0:3] in months and re.match("[a-zA-Z]{3}-[0-9]+-[0-9]+-[0-9]+-[AP]M", file[0:-4]):
                #if it's an update, add it to the list
                newItems.append(file)

    #if a new file has been downloaded
    if len(newItems) > 0:
        #move new files into unprocessed directory
        print("processing")
        for newItem in newItems:
            os.rename(downloadPath + "/" + newItem, unprocessedFolder + "/" + newItem)
        processNewData()

    time.sleep(60)
