import matplotlib.pyplot as pl
import sys
import pandas as pd
import os
import numpy as np
def rollingAverage(series, kernelLen):
    rolled = np.empty(len(series) - kernelLen -1)
    for i in range(kernelLen-1, len(series)):

        rolled[i - kernelLen -1] = np.average(series[i-(kernelLen-1):i])
    return rolled



if __name__ == '__main__':
    readPath = sys.argv[1]
    # readPath = '/home/esraa/PycharmProjects/radioSignalPestDet/bug_no_bug_examples'
    # readPath = '/home/esraa/PycharmProjects/radioSignalPestDet/BugDetectorProgram/simulationExamplesSeries'
    # writePath = sys.argv[2]



    dataFiles = os.listdir(readPath)

    allDF = []
    maxFreq = float("-inf")
    minFreq = float("inf")

    for f in dataFiles:
        xyDataDF = pd.read_csv(readPath+"/"+ f)
        # currFMax = max(xyDataDF.iloc[:, 1])
        # currFMin = min(xyDataDF.iloc[:, 1])
        #
        # if(currFMax > maxFreq):
        #     maxFreq = currFMax
        # if(currFMin < minFreq):
        #     minFreq = currFMin
        allDF.append(xyDataDF)

    # minMaxMap = {'slar_6_fit.txt': [3.771, 3.773], 'blar_8_fit.txt':[3.799, 3.803], 'ad_5b_fit.txt': [3.772, 3.774], 'cleanKernel2.txt': [0, 3.9]}
    colors = ['red', 'blue']


    for i in range(len(allDF)):


        # if(dataFiles[i] in minMaxMap):
        xyDataDF = allDF[i]
        # pl.plot(xyDataDF.iloc[:, 0], xyDataDF.iloc[:,1])
        rolled = rollingAverage(xyDataDF.iloc[:, 1], 100)
        # rolled = xyDataDF.iloc[:, 1]
        shiftDist = min(rolled)
        #
        for x in range(len(rolled)):
            rolled[x] = rolled[x]-shiftDist+0.000001

        t = np.arange(len(rolled))
        if('clean' in dataFiles[i]):
            color = colors[0]
        else:
            color = colors[1]
        pl.plot(t, rolled, color)

        # pl.suptitle(dataFiles[i])
        pl.xlabel("Time (s)")
        pl.ylabel("Frequency (GHz)")
        # pl.ylim([minFreq - ((maxFreq - minFreq)/10), maxFreq + ((maxFreq - minFreq)/10)])
        # pl.ylim([minMaxMap[dataFiles[i]][0], minMaxMap[dataFiles[i]][1]])
        # pl.savefig(writePath+"/"+dataFiles[i]+".png", dpi = 600)
        # pl.cla()



    pl.show()

