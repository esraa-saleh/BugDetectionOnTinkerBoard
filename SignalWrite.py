import numpy as np
import UI
import sys
import os
import SignalProcess
import SignalRead
import json
import gc


'''
Function: writeSignal
Purpose : sends a commandline command to write to a file a number of samples
          given the time interval, gain, sampling rate and center frequency

Input   : currFile, string, file name of file in which signal (IQ data) will be stored 
          sampleRate, int, sampling rate for signal writing
          timeSignal, int, time span of signal (if you are doing this on a raspberry pi, 
          pay attention to memory requirements )
          centerFreq, int, center frequency in hertz
          gain, int, gain for signal recording which is usually put at 40

Output  :   N/A

Files Written : currFile, which contains IQ data gathered

'''
def writeSignal(currFile, sampleRate, timeSignal, centerFreq, gain):

    totalNumSamples = int(timeSignal * sampleRate)
    print "sudo hackrf_transfer -f " + str(centerFreq) + " -g "+str(gain)+" -s " + str(sampleRate) + " -n " + str(
        totalNumSamples) +" -r "+currFile

    os.system("sudo hackrf_transfer -f " + str(centerFreq) + " -g "+str(gain)+" -s " + str(sampleRate) + " -n " + str(
        totalNumSamples) +" -r "+currFile)





'''
The motivation for having this function is to avoid holding more 
than a single spectrogram or time series in memory

Function : spaceEfficientSignalToSeries
Purpose  : To get IQ signals, extract time series, and write that time series to a file

Input    : currIQFile, string, name of file to write an IQ signal to
           currSeriesFile, string, after extracting a time series from a spectrogram from an IQ signal,
           that series will be saved to currSeriesFile
           sampleRate, int, sampling rate while recording the IQ signal
           timeSignal, int, time span of the signal
           centerFreq, int, center frequency to record on given in hertz
           gain, int, gain for recording a signal which is usually set at 40

Output   : N/A

Files Written: currSeriesFile, contains the extracted time series
'''
#TODO: don't cut the first second from series, cut from spectrogram

def spaceEfficientSignalToSeries(currIQFile, currSeriesFile, sampleRate, timeSignal,
                                 centerFreq, gain):
    writeSignal(currFile=currIQFile, sampleRate=sampleRate, timeSignal=timeSignal+1, centerFreq=centerFreq,
                gain=gain)

    spec, freqList, t = SignalRead.extractSpecFromIQFile(inFile = currIQFile, sampleRate = sampleRate,
                                                     centerFreq = centerFreq)
    os.remove(currIQFile)
    series = SignalProcess.centerOfMassMethodSeries(spec=spec, freqList=freqList)
    index = 0
    while(t[index]<1.0):
        index+=1
    
    series = series[index:]
    t=  t[index:]

    series = SignalProcess.rollingAverage(series, 10)
    t = SignalProcess.rollingAverage(t, 10)
    UI.plotResFreqs(t, series)
    del spec
    del freqList
    gc.collect()
    writeSeriesToFile(currSeriesFile, series, t)
    del series
    del t
    gc.collect()



'''
Function: collectOneTypeExamples

Purpose : to collect and write a given number of examples (i.e. time series expressing shifts in resonant frequencies of the cavity) 
          which could be examples corresponding to a kernel with or without a bug

Input   : numExamples, int, number of examples desired from a single class
          iQStartFileName, string, the string in the beginning of the name of an iq example file
          seriesFileStartName, string, the string in the beginning of the name of a series example file
          extension, string, the string expressing the file extension of examples to be written
          sampleRate, int, the sampling rate given to the hackrf which records examples as IQ data, parameter is usually at 2500000
          timeSignal, int, number of seconds defining the length of examples
          centerFreq, int, the center frequency of measuremnets
          gain, int, the gain for recording measurements, usually left at 40

Output  : sigOK, boolean, in case the user decided to end measurement taking abruptly, the function returns a boolean indicating 
          whether all desired measuremnts were done
          

'''


def collectOneTypeExamples(numExamples, iQFileStartName, seriesFileStartName, extension, sampleRate, timeSignal, centerFreq, gain):
    sigOK = 1
    for i in range(numExamples):
        currIQFile = iQFileStartName+str(i)+extension
        currSeriesFile = seriesFileStartName+str(i)+extension

        spaceEfficientSignalToSeries(currIQFile=currIQFile, currSeriesFile=currSeriesFile, sampleRate= sampleRate,
                                         timeSignal=timeSignal, centerFreq=centerFreq,
                                         gain=gain)

        if (i < numExamples - 1):
            sigOK = UI.requestNextKernel()
            if(not sigOK):
                return not sigOK
    
    return sigOK



'''
Function: collectExamples

Purpose : to record examples corresponding to infested and clean kernels

Input   : outDirIQ, string, path to the directory in which you would like to have IQ Data (which will be immediately deleted since
          collectOneTypeExamples uses a space efficient function )
          
          outDirSeries, string, path to the directory in which you would like to keep all time series data experssing shifts
          in the resonant frequnecy of the cavity

          sampleRate, int, sampling rate to be used in recording measurements, usually set at 2500000
          timeSignal, int, the time span for a single measurement
          gain, int, the gain for recording measurements, usually set at 40
          numBugsExamples, int, desired number of examples corresponding to an infested kernel
          numNoBugsExamples, int, desired number of examples corresponding to a clean kernel
          bugCenterFrequency, int, center frequency (in hertz) at which you would like to take measurements for an infested kernel
          noBugCenterFrequency, int, center frequency (in hertz) at which you would like to take measurements for a clean kernel
          bugFileLabel, string, a string common to all file names of files containing an example from an infested kernel
          noBugFileLabel, string, a string common to all file names of files containing an example from a clean kernel

Output : N/A

Files Written : The number of files written will be : numBugsExamples + numNoBugsExamples. Each file will correspond to either
                a measurement done on a clean or an infested kernel and will contain a time series expressing shifts in the
                resonant frequencies of the cavity.
'''
def collectExamples(outDirIQ, outDirSeries, sampleRate, timeSignal, gain, numBugsExamples, numNoBugsExamples, bugCenterFrequency = 0, noBugCenterFrequency =0,
                    bugFileLabel = 'bug_', noBugFileLabel = 'clean_'):

    process = "collecting examples"
    UI.declareProcessStart(process)
    print "num bug examples: ", numBugsExamples
    print "num no bug examples: ", numNoBugsExamples
    extension = ".txt"


    if(numBugsExamples > 0 and bugCenterFrequency > 0):

        iQFileStartName = outDirIQ + "/" + bugFileLabel
        seriesFileStartName = outDirSeries + "/" +bugFileLabel
        sigOK = UI.noticeCollectBugsExamples()
        if(not sigOK):
            exit(1)

        sigOK = collectOneTypeExamples(numBugsExamples, iQFileStartName, seriesFileStartName, extension, sampleRate, timeSignal, bugCenterFrequency, gain)
        
        if(not sigOK):
            exit(1)

    if(numNoBugsExamples > 0 and noBugCenterFrequency>0):

        iQFileStartName = outDirIQ + "/" + noBugFileLabel
        seriesFileStartName = outDirSeries + "/" + noBugFileLabel
        sigOK = UI.noticeCollectNoBugsExamples()

        if (not sigOK):
            exit(1)

        sigOK = collectOneTypeExamples(numNoBugsExamples, iQFileStartName, seriesFileStartName, extension, sampleRate, timeSignal, noBugCenterFrequency, gain)

        if(not sigOK):
            exit(1)

    if ((bugCenterFrequency < 0 and numBugsExamples > 0) or (noBugCenterFrequency < 0 and numNoBugsExamples > 0)):
        print "Error: cannot have a center frequency less than or equal to 0"
        exit(1)

    UI.declareProcessDone(process)


'''
Function: writeSeriesToFile

Purpose : to write a given time series to a file

Input   : fileName, string, name of the file to write a time series in
          series, array or list of values (frequencies)
          timeList, parallel array or list of values to the series list, such that each time value is a moment in 
          time corresponding to the recording of a single series value.
          showProgress, boolean, when True the function prints when it completes writing a time series

Output  : N/A

Files Written: a file with the name fileName, that contains the given time series

'''
def writeSeriesToFile(fileName, series, timeList, showProgress = True):
    timeAndSeries = np.column_stack((timeList, series))

    np.savetxt(fname=fileName+".txt", X=timeAndSeries, delimiter=',')
    if(showProgress==True):
        UI.declareProcessDone("saving series to csv file " + fileName)




'''
Function : mainSettingsFromFile

Purpose  : to read in settings for gathering signals from a file and launch the process of creating a dataset

Input    : filePath, string, path to file containing settings for gathering signals

Output   : N/A

Files Written: The number of files written will be : numBugsExamples + numNoBugsExamples. Each file will correspond to either
                a measurement done on a clean or an infested kernel and will contain a time series expressing shifts in the
                resonant frequencies of the cavity.
                A file documenting settings of the dataset will also be written

'''
def mainSettingsFromFile(filePath):

    with open(filePath, 'r') as f:
        allLines = f.readlines()
        for i in range(len(allLines)):
            allLines[i] = allLines[i].strip()
        iqDirPath = allLines[0]
        seriesDirPath = allLines[1]
        sampleRate = int(allLines[2])
        timeSignal = float(allLines[3])
        gain = int(allLines[4])
        numBug = int(allLines[5])
        numNoBug= int(allLines[6])
        bugCenterFreq = int(allLines[7])
        noBugCenterFreq = int(allLines[8])
        print bugCenterFreq
        print noBugCenterFreq

        labelsTypes = ['clean_', 'bug_']
        collectExamples(outDirIQ=iqDirPath, outDirSeries= seriesDirPath, sampleRate=sampleRate, timeSignal= timeSignal, gain=gain, numBugsExamples=numBug,
                    numNoBugsExamples=numNoBug, bugCenterFrequency= bugCenterFreq,
                    noBugCenterFrequency= noBugCenterFreq, bugFileLabel=labelsTypes[1], noBugFileLabel = labelsTypes[0])

        settings = {'sampling_rate': sampleRate, 'signal_time': timeSignal, 'gain': gain, 'series_path': seriesDirPath}

        with open(os.path.basename(seriesDirPath) + 'Settings' + '.txt', 'w') as file:
            file.write(json.dumps(settings))


'''
Function : mainUserPrompts

Purpose : to take user input for settings for gathering signals and launch the process of creating a dataset

Input : N/A

Output: N/A

Files Written : The number of files written will be : number of specified examples of infested kernels and clean kernels. Each file will correspond to either
                a measurement done on a clean or an infested kernel and will contain a time series expressing shifts in thei
                resonant frequencies of the cavity.
                A file documenting settings of the dataset will also be written
'''

def mainUserPrompts():
    UI.writeWelcome()
    iqDirPath, seriesDirPath, sampleRate, timeSignal, gain, numBug, numNoBug= UI.requestVarsOFSignalWriting()
    #prompt on bug no bug frequencies

    # defining our classification labels
    labelsTypes = ['clean_', 'bug_']

    #get raw iq data recorded into iqDirPath
    bugCenterFreq = 0
    noBugCenterFreq = 0
    if(numBug > 0):
        bugCenterFreq = UI.requestBugCenterFrequency()

    if(numNoBug > 0 ):
        noBugCenterFreq = UI.requestNoBugCenterFrequency()

 
    collectExamples(outDirIQ=iqDirPath, outDirSeries= seriesDirPath, sampleRate=sampleRate, timeSignal= timeSignal, gain=gain, numBugsExamples=numBug,
                    numNoBugsExamples=numNoBug, bugCenterFrequency= bugCenterFreq,
                    noBugCenterFrequency= noBugCenterFreq, bugFileLabel=labelsTypes[1], noBugFileLabel = labelsTypes[0])

    settings = {'sampling_rate': sampleRate, 'signal_time': timeSignal, 'gain': gain, 'series_path': seriesDirPath}

    with open(os.path.basename(seriesDirPath) + 'Settings' + '.txt', 'w') as file:
        file.write(json.dumps(settings))





'''
Function: mainCommandLine

Purpose : receive signal recording parameters from commandline arguments

Input   : N/A

Output  : N/A

Files Written:  The number of files written will be : number of specified examples of infested kernels and clean kernels. Each file will correspond to either
                a measurement done on a clean or an infested kernel and will contain a time series expressing shifts in the
                resonant frequencies of the cavity.
                A file documenting settings of the dataset will also be written 
'''

def mainCommandLine():
    # Make examples
    # get these as commandline arguments: outDir, n, sampleRate, timeSignal, centerFreq, gain
    UI.writeWelcome()
    if(len(sys.argv)!=10):
        print "Error: Wrong number of arguments. \n" \
              "Command example: python SignalWrite.py iqDirPath, seriesDirPath, sampleRate, timeSignal, centerFreq, gain"
        exit(1)
    iqDirPath = sys.argv[1]
    seriesDirPath = sys.argv[2]
    sampleRate = int(sys.argv[3])
    timeSignal = float(sys.argv[4])
    numBug = int(sys.argv[5])
    numNoBug = int(sys.argv[6])
    bugCenterFreq = float(sys.argv[7])
    noBugCenterFreq = float(sys.argv[8])
    gain = int(sys.argv[9])
    
    labelsTypes = ['clean_', 'bug_']


    collectExamples(outDirIQ=iqDirPath, outDirSeries= seriesDirPath, sampleRate=sampleRate, timeSignal= timeSignal, gain=gain, numBugsExamples=numBug,
                    numNoBugsExamples=numNoBug, bugCenterFrequency= bugCenterFreq,
                    noBugCenterFrequency= noBugCenterFreq, bugFileLabel=labelsTypes[1], noBugFileLabel = labelsTypes[0])

    settings = {'sampling_rate': sampleRate, 'signal_time': timeSignal, 'gain': gain, 'series_path': seriesDirPath}

    with open(os.path.basename(seriesDirPath) + 'Settings' + '.txt', 'w') as file:
        file.write(json.dumps(settings))

    



if __name__ == '__main__':
    mainUserPrompts()



