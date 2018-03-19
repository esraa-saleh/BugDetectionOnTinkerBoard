import numpy as np
import UI
# import SignalRead
from scipy.optimize import curve_fit
import matplotlib.pyplot as pl


'''
Tested Feb 12
TODO: Exception handling for the gaussian function parameter optimization
Update: This is not needed since the main program uses the centroid method

'''

'''
Purpose: to obtain a series consisting of the resonant frequency for every timestep 
This is done by the simple definition of resonant frequency: For a timestep, it is the frequency at
which the maximum "transmission coefficient" occurs.
'''
def extractSimpleResonant(spectrogram, freqs, minFreq=None, maxFreq = None):
    series = np.empty(spectrogram.shape[1])
    if(minFreq > maxFreq):
        print "Error: minimum frequency specified is larger than the maximum frequency specified."
        exit(1)


    for i in range(spectrogram.shape[1]):

        col = spectrogram[:, i]
        sortedColIndexList = np.argsort(col)
        sizeIndList = sortedColIndexList.shape[0]
        count = 1
        possMaxAtFreq = freqs[sortedColIndexList[sizeIndList-count]]

        #keep looking for a max at which the corresponding frequency is in the desired band range
        if(minFreq!= None and maxFreq!=None):

            while(possMaxAtFreq < minFreq or possMaxAtFreq > maxFreq):
                count+=1
                possMaxAtFreq = freqs[sortedColIndexList[sizeIndList-count]]

        #if we finally find one, then we add it to the series
        series[i] = possMaxAtFreq

    return series


# The following function is mostly from Alex Reimer
# Translated from MATLAB to Python by Esra'a Saleh

'''
a = peak height
b = peak centre
c = peak width
d = vertical offset
'''

def extractResonantWithFit(spec, freqList, spreadDenom):
    x = freqList
    #Since x is 1d here, then this is the same as  (x(end,1)-x(1,1))/spread_denom
    c =(x[-1] - x[1])/spreadDenom #estimate spread
    #make b the middle measurement of x
    b = x[int(len(x)/2)] #estimate

    series = np.empty(spec.shape[1])
    for i in range(spec.shape[1]):
        #take one column of the spectrogram
        y = spec[:, i]

        #d and a are parameters to fix, in the matlab script
        d = min(y)
        a = max(y) - d

        def gauss(x, b):
            return a*np.exp(-np.power((x-b), 2.0)/(2*(c**2.0)))+d

        popt, pcov = curve_fit(f= gauss, xdata=x, ydata= y, p0=[b])
        yFit = gauss(x, popt[0])

        series[i] = freqList[np.argmax(yFit)]

    return series

def centerOfMassMethodSeries(spec, freqList):
    # prepare a series array of the desired length being the number of columns in the spectrogram
    series = np.empty(spec.shape[1])

    # for every column do
    for col in range(spec.shape[1]):
        # specCol, is a single column at index col
        specCol = spec[:, col]

        # now we are going to normalize the transmission array
        # transmission = specCol / (sum of elements in specCol)
        transmission = np.divide(specCol, np.sum(specCol))

        # compute the center of mass
        # sum (transmission * freqs ), where * denotes element-wise multiplication
        newSig = np.sum(np.multiply(transmission, freqList))

        # insert center of mass into the series array at the correct column
        series[col] = newSig

    return series


def extractResWithCenterOfMassMultSpecs(specs, freqLists):
    process = 'extracting series from every spectrogram given...'
    UI.declareProcessStart(process)
    allSeries = []
    for i in range(len(specs)):
        allSeries.append(centerOfMassMethodSeries(spec=specs[i], freqList=freqLists[i]))
    UI.declareProcessDone(process)
    return allSeries
#
# def extractResWithFitMultSpecs(specs, freqLists, spreadDenom):
#     process = 'extracting series from every spectrogram given...'
#     UI.declareProcessStart(process)
#     allSeries = []
#     for i in range(len(specs)):
#         allSeries.append(extractResonantWithFit(specs[i], freqLists[i], spreadDenom))
#     UI.declareProcessDone(process)
#     return allSeries

# 4 2500000 1 303000000 40
def plotFitsTest():
    # # specFile = 'specFile.txt'
    # #TODO: this cannot be automated, it is obtaned by trial and error
    # #for now we can have a temporary calibration stage
    # spreadDenom = 0.00001
    #
    # iqFile = '/home/esraa/PycharmProjects/radioSignalPestDet/bug_no_bug_dataset/bug_0.txt'
    # spec, f, timeList = SignalRead.extractSpecFromIQFile(inFile=iqFile, sampleRate=2500000, centerFreq=303000000)
    # # f, spec = SignalRead.extractSpecFromSpecFile(specFile)
    #
    # series1 = extractResonantWithFit(spec, f, spreadDenom)
    # t1 = np.arange(0, len(series1))
    #
    #
    # maxS1 = max(series1)
    # minS1 = min(series1)
    #
    # fig, ax1 = pl.subplots(1)
    #
    # ax1.plot(t1, series1)
    # # ax1.set_ylim(minS1,maxS1)
    # pl.show()
    pass

if __name__ == '__main__':

    plotFitsTest()