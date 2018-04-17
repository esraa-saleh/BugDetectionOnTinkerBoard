import matplotlib.pyplot as pl
import os
import numpy as np
import UI
#TODO: eliminate need for pandas
import pandas as pd

'''
Tested Feb 12

'''
import SignalWrite
import SignalProcess

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
    #expects files in the format : bug_i.txt or no_bug_i.txt
    ids = np.empty(len(allFiles), dtype='int')
    for i in range(len(allFiles)):
        ids[i] = extractSingleFileID(allFiles[i])
    return ids

def testExtractFileIDs():
    dirData = 'bug_no_bug_dataset'
    allFiles = os.listdir(dirData)
    ids = extractFileIDs(allFiles)
    print allFiles
    print ids

'''
Purpose: given a directory path to spectrograms, get all spectrograms
Assumes that the label types is what the bug/no bug file names start with
'''
# def extractSpecsFromIQDir(inDirPath, sampleRate, centerFreqBug, centerFreqNoBug, bugWordLabel, noBugWordLabel):
#     process = "extracting spectrograms"
#     UI.declareProcessStart(process)
#     allFiles = os.listdir(inDirPath)
#
#     specs = []
#     timeLists = []
#     freqLists = []
#
#     minFreqBug = 0
#     maxFreqBug = 0
#     minFreqNoBug = 0
#     maxFreqNoBug = 0
#
#     for i in range(len(allFiles)):
#         print "extracting spectrogram of file: ", allFiles[i]
#         # s, f, t = extractSpecFromIQFile(inDirPath + "/" + allFiles[i], sampleRate, centerFreq)
#
#         if(allFiles[i].startswith(bugWordLabel)):
#             s, f, t = extractSpecFromIQFile(inDirPath + "/" + allFiles[i], sampleRate, centerFreqBug)
#             if(minFreqBug ==0 and maxFreqBug ==0):
#                 minFreqBug = int(raw_input("Min : "))
#                 maxFreqBug = int(raw_input("Max : "))
#
#             ind, = np.where((f >= minFreqBug) & (f <= maxFreqBug))
#
#         elif(allFiles[i].startswith(noBugWordLabel)):
#             s, f, t = extractSpecFromIQFile(inDirPath + "/" + allFiles[i], sampleRate, centerFreqNoBug)
#             if(minFreqNoBug ==0 and maxFreqNoBug ==0):
#                 minFreqNoBug = int(raw_input("Min : "))
#                 maxFreqNoBug = int(raw_input("Max : "))
#
#             ind, = np.where((f >= minFreqNoBug) & (f <= maxFreqNoBug))
#
#         else:
#             print "Error: None of the IQ files starts with the given category labels, ",bugWordLabel, ", ", noBugWordLabel
#             exit(1)
#
#
#         s = s[ind[0]:ind[len(ind)-1], :]
#         f = f[ind[0]: ind[len(ind)-1]]
#         print f
#         specs.append(s)
#         timeLists.append(t)
#         freqLists.append(f)
#
#     UI.declareProcessDone(process)
#     wordLabels = [bugWordLabel, noBugWordLabel]
#     labels = extractSpecNumLabelsFromFiles(allFiles, wordLabels)
#     ids = extractFileIDs(allFiles)
#     return specs, freqLists, timeLists, labels, ids

# def testExtractSpecsFromIQDir():
#     inDirPath = '/home/esraa/PycharmProjects/radioSignalPestDet/BugDetectorProgram/simulationExamplesIQ'
#     outDirPath = '/home/esraa/PycharmProjects/radioSignalPestDet/BugDetectorProgram/simulationExamplesSeries'
#     sampleRate = 2500000
#     centerFreq = 102503000
#     labelsTypes = ['no_bug', 'bug']
#
#     specs, freqLists, timeLists, labels, ids = extractSpecsFromIQDir(inDirPath, sampleRate, centerFreq, labelsTypes)
#
#     allSeries = SignalProcess.extractResWithCenterOfMassMultSpecs(specs, freqLists)
#     SignalWrite.writeMultSeriesToFiles(outDirPath, allSeries, timeLists, labels, labelsTypes, ids)

def spectrogramCutForFreqRange(minFreq, maxFreq, freqList, spec):
    ind, = np.where((freqList >= minFreq) & (freqList <= maxFreq))
    spec = spec[ind[0]:ind[len(ind) - 1], :]
    freqList = freqList[ind[0]: ind[len(ind) - 1]]

    return spec, freqList

def extractSpecFromIQFile(inFile, sampleRate, centerFreq=None, specMinFreq = None, specMaxFreq = None):
    sig = iqDataFromFile(inFile)

    # totalSamples= len(sig.real)
    #TODO: try NFFT= (smallest power of 2 greater than totalSamples)
    cmap = pl.get_cmap('inferno')
    pl.suptitle('Note the frequency range for which a series will be extracted ')
    spectrum, freqs, t, im = pl.specgram(sig, Fs=sampleRate, Fc=centerFreq, NFFT=1048, cmap=cmap)
    # minFreq = int(raw_input("Min : "))
    # maxFreq = int(raw_input("Max: "))

    #
    # ind, = np.where((freqs >= minFreq) & (freqs <= maxFreq))
    # # print ind
    #
    # spectrum = spectrum[int(ind[0]):int(ind[len(ind)-1]), :]
    # pl.ylim([freqs[int(ind[0])], freqs[int(ind[len(ind)-1])]])
    pl.show()
    pl.close()

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

def extractSeriesFromFile(inFile):
    df = pd.read_csv(inFile, header= None)
    time = df.iloc[:, 0]
    series = df.iloc[:, 1]
    return time, series

# #TODO: run this!
# testExtractSpecsFromIQDir()
