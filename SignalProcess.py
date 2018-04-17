import numpy as np
import UI
from scipy.optimize import curve_fit
import matplotlib.pyplot as pl



'''
Function : extractSimpleResonant

Purpose  : to obtain a series consisting of the resonant frequency for every timestep 
           This is done by the simple definition of resonant frequency: For a timestep, it is the frequency at
           which the maximum "transmission coefficient" occurs.
Input    : spectrogram, matrix (list of lists) of transmission coefficients
           freqs, list or array of frequencies, such that each frequency corresponds to single row in the spectrogram matrix
           minFreq, float, minimum  frequency allowed 
           maxFreq, float, maximum frequency allowed

Output   : series, numpy array, sequence of values where each is the resonant frequency at a single timestep according
           to the definition of a simple resonant frequency in the Purpose.
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
'''
Function : extractResonantWithFit

Purpose  : produes a time series from a spectrogram. The time series should reflect shifts in the widest
           bright band. Every column from the spectrogram is summarized by a single value obtained
           by fitting a gaussian on the graph of that column vs. the parallel frequency list, and then
           obtaining the frequency at which the peak of the guassian occurs.

Input    : spec, matrix (list of lists) of transmission coefficients
           freqList, list or array of frequencies, such that each frequency corresponds to single row in the spectrogram matrix
           spreadDenom, float, constant used to estimate the spread

Output   : series, numpy array, time series reflecting shifts in the widest bright band of the spectrogram

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

'''
Function : centerOfMassMethodSeries

Purpose  : produes a time series from a spectrogram. The time series should reflect shifts in the widest
           bright band. Every column from the spectrogram is summarized by a single value obtained
           by operations described in detail in code comments

Input    : spec, matrix (list of lists) of transmission coefficients
           freqList, list or array of frequencies, such that each frequency corresponds to single row in the spectrogram matrix

Output   : series, numpy array, time series reflecting shifts in the widest bright band of the spectrogram

'''
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

'''
Function: extractResWithCenterOfMassMultSpecs

Purpose : extract series from multiple spectrograms using the technique given by the function : centerOfMassMethodSeries

Input   : specs, matrices (list of lists) of transmission coefficients
          freqLists, list of frequency lists (parallel to specs list), where each frequency list corresponds to a single spectrogram

Output  : allSeries, list of numpy arrays, each numpy array is a time series extracted from a corresponding spectrogram using the 
          center of mass method as was mentioned in the Purpose.
'''
def extractResWithCenterOfMassMultSpecs(specs, freqLists):
    process = 'extracting series from every spectrogram given...'
    UI.declareProcessStart(process)
    allSeries = []
    for i in range(len(specs)):
        allSeries.append(centerOfMassMethodSeries(spec=specs[i], freqList=freqLists[i]))
    UI.declareProcessDone(process)
    return allSeries


'''
Function: rollingAverage

Purpose : given a time series and a time window, obtain a new series by sliding a time window (by one timestep) across the given series and obtaining
          the mean series value within that time frame

Input   : series, list or array, a sequence of values
          kernelLen, int, the number of "time steps" or just the width of the frame that will be sliding 

Output  : rolled, list or array, a sequence of values that are the result of the rolling average function

'''
def rollingAverage(series, kernelLen):
    rolled = np.empty(len(series) - kernelLen)
    for i in range(0, len(series)- kernelLen):
        rolled[i] = np.mean(series[i:i+kernelLen])
    return rolled


'''
Function: magnitudesRatesOfChange

Purpose : to obtain a sequence that reflects the magnitudes of rates of change between every two consecutive sequence 
          values seperated by window-1 values.
          
Input   : series, list or array, sequence of values
          time, parallel list or array to series, sequence of time values (approximation of when each value from the series was recorded)
          window, int, parameter that defines the separation required between two time seris points in order to calculate the rate of change
          between them

Output  : rates, numpy array, sequence of rates as examplained in the Purpose
'''
def magnitudesRatesOfChange(series, time, window = 10):
    if(len(series) != len(time)):
        print "ERROR: length of time series given does not equal length of time array"
        exit(1)

    rates = np.empty(len(series)- window, dtype = 'float64')
    for i in range(0, len(series) - window):
        rates[i] = abs((series[i+window]- series[i])/(time[i+window - time[i]]))
    
    return rates


