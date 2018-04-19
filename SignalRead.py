import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as pl
import os
import numpy as np
import UI

#TODO: eliminate need for pandas
import pandas as pd
import SignalWrite
import SignalProcess


pl.ioff()

'''
Purpose: reading a binary file of IQ data and returning it as a complex numbered time series
'''
def iqDataFromFile(filename):
    # np.fromfile is for reading binary data
    x = np.fromfile(filename, np.uint8) - np.float32(127.5) #by subtracting a float32 the resulting array will also be float32
    #add real part to imaginary part to make a complete array
    x = x[::2] + 1j*x[1::2]
    return x


def extractSpecNumLabelsFromFiles(specFileNames, labelsTypes):
    labels = np.empty(len(specFileNames), dtype='int')
    for i in range(len(specFileNames)):
        base = os.path.splitext(os.path.basename(specFileNames[i]))[0]
        labelAssigned = False

        l = 0
        while(labelAssigned==False and l< len(labelsTypes)):
            if(labelsTypes[l] in base):
                labels[i] = l
                labelAssigned =True
            l += 1


        if(labelAssigned==False):
            print "Error: files were not named according to the expected naming convention...refer to the README.md"
            exit(1)

    return labels


def extractSingleFileID(aFile):
    base = os.path.splitext(os.path.basename(aFile))[0]
    print aFile
    idPart = []
    currChar = base[-1]
    currIndex = -1
    while (currChar != '_' and abs(currIndex) < len(base)):
        idPart.append(currChar)
        currIndex -= 1
        currChar = base[currIndex]
    idPart.reverse()
    fileID = int(''.join(idPart))
    return fileID


def extractFileIDs(allFiles):
    #expects files in the format : label_id.txt
    ids = np.empty(len(allFiles), dtype='int')
    for i in range(len(allFiles)):
        ids[i] = extractSingleFileID(allFiles[i])
    return ids

def spectrogramCutForFreqRange(minFreq, maxFreq, freqList, spec):
    ind, = np.where((freqList >= minFreq) & (freqList <= maxFreq))
    spec = spec[ind[0]:ind[len(ind) - 1], :]
    freqList = freqList[ind[0]: ind[len(ind) - 1]]

    return spec, freqList

def extractSpecFromIQFile(inFile, sampleRate, centerFreq=None, specMinFreq = None, specMaxFreq = None):
    sig = iqDataFromFile(inFile)   
    
    cmap = pl.get_cmap('inferno')

    spectrum, freqs, t, im = pl.specgram(sig, Fs=sampleRate, Fc=centerFreq, NFFT=1048, cmap=cmap)


    #These two statements are in case someone specifies only a single side of the desired frequency range
    if(specMinFreq is not None  and specMaxFreq is None):
        specMaxFreq = max(freqs)

    elif(specMaxFreq is not None and specMinFreq is None):
        specMinFreq = min(freqs)


    #Because of the statemnets before, this will execute if at least one side of the frequency range is specified
    if(specMinFreq is not None and specMinFreq is not None):
        spectrum, freqs = spectrogramCutForFreqRange(specMinFreq, specMaxFreq, freqs, spectrum)

    return spectrum, freqs, t


def extractSpecFromSpecFile(inFile):
    df = pd.read_csv(inFile, header=None)
    freqs = df.iloc[:, 0]
    freqs = np.array(freqs.values)
    df.drop(df.columns[[0]], axis=1, inplace=True)
    return freqs, df.values


def extractTimeVectorOnly(inFile):
    df = pd.read_csv(inFile, header= None)
    time = df.iloc[:, 0]
    return time

def extractSeriesOnly(inFile):
    df = pd.read_csv(inFile, header= None)
    series = df.iloc[:, 1]
    return series


def extractTimeSeriesFromFile(inFile):
    df = pd.read_csv(inFile, header= None)
    time = df.iloc[:, 0]
    series = df.iloc[:, 1]
    return time, series


