import numpy as np
import UI
from scipy.optimize import curve_fit
import matplotlib.pyplot as pl



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


def rollingAverage(series, kernelLen):
    rolled = np.empty(len(series) - kernelLen)
    for i in range(0, len(series)- kernelLen):
        rolled[i] = np.mean(series[i:i+kernelLen])
    return rolled

def magnitudesRatesOfChange(series, time, window = 10):
    if(len(series) != len(time)):
        print "ERROR: length of time series given does not equal length of time array"
        exit(1)

    rates = np.empty(len(series)- window, dtype = 'float64')
    for i in range(0, len(series) - window):
        rates[i] = abs((series[i+window]- series[i])/(time[i+window - time[i]]))
    
    return rates


