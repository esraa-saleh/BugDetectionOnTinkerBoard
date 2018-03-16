import numpy as np
import UI
import sys
import os
import SignalProcess
import SignalRead

'''
Tested Feb 12
'''


'''
Purpose: sends a commandline command to write to a file a number of samples
given the time interval, gain, sampling rate and center frequency

'''
def writeSignal(currFile, sampleRate, timeSignal, centerFreq, gain):

    totalNumSamples = int(timeSignal * sampleRate)
    print "sudo hackrf_transfer -f " + str(centerFreq) + " -g "+str(gain)+" -s " + str(sampleRate) + " -n " + str(
        totalNumSamples) +" -r "+currFile

    os.system("sudo hackrf_transfer -f " + str(centerFreq) + " -g "+str(gain)+" -s " + str(sampleRate) + " -n " + str(
        totalNumSamples) +" -r "+currFile)


'''
Purpose: recording bugs and no bugs examples
'''
def collectExamples(outDir, sampleRate, timeSignal, gain, numBugsExamples, numNoBugsExamples, bugCenterFrequency = 0, noBugCenterFrequency =0,
                    bugFileLabel = 'bug_', noBugFileLabel = 'clean_'):

    process = "collecting examples"
    UI.declareProcessStart(process)
    print "num bug examples: ", numBugsExamples
    print "num no bug examples: ", numNoBugsExamples
    extension = ".txt"
    if(numBugsExamples > 0 and bugCenterFrequency > 0):
        fileStartName = outDir + "/" + bugFileLabel
        sigOK = UI.noticeCollectBugsExamples()
        if(not sigOK):
            exit(1)

        for i in range(numBugsExamples):
            currFile = fileStartName+str(i)+extension
            writeSignal(currFile= currFile, sampleRate= sampleRate, timeSignal=timeSignal, centerFreq=bugCenterFrequency, gain=gain)
            if (i < numBugsExamples - 1):
                sigOK = UI.requestNextKernel()
                if(not sigOK):
                    exit(1)

    if(numNoBugsExamples > 0 and bugCenterFrequency>0):

        fileStartName = outDir+"/"+ noBugFileLabel
        sigOK = UI.noticeCollectNoBugsExamples()

        if (not sigOK):
            exit(1)

        for i in range(numNoBugsExamples):
            currFile = fileStartName+str(i)+extension
            writeSignal(currFile= currFile, sampleRate= sampleRate, timeSignal=timeSignal, centerFreq=noBugCenterFrequency, gain=gain)


            if(i<numNoBugsExamples-1):
                sigOK = UI.requestNextKernel()
                if(not sigOK):
                    exit(1)

    if ((bugCenterFrequency < 0 and numBugsExamples > 0) or (noBugCenterFrequency < 0 and numNoBugsExamples > 0)):
        print "Error: cannot have a center frequency less than or equal to 0"
        exit(1)

    UI.declareProcessDone(process)


#series is a numpy array
def writeSeriesToFile(fileName, series, timeList, showProgress = True):
    timeAndSeries = np.column_stack((timeList, series))

    np.savetxt(fname=fileName+".txt", X=timeAndSeries, delimiter=',')
    if(showProgress==True):
        UI.declareProcessDone("saving series to csv file " + fileName)



def writeMultSeriesToFiles(dirPath, multSeries, multTimeLists, labelsNums, labelTypesWords, ids):
    process = "writing series to files"
    UI.declareProcessStart(process)

    if(len(multTimeLists)!= len(multSeries)):
        print "Error: number of elements in collection of time lists does not \n " \
              "match number of elements in collection of series..."
        exit(1)


    for i in range(len(multSeries)):
        #convert numerical label to word label
        wordLabel = labelTypesWords[labelsNums[i]]
        fileName = dirPath+ '/' + wordLabel+'_'+str(ids[i])
        writeSeriesToFile(fileName, multSeries[i], multTimeLists[i], showProgress=False)

    UI.declareProcessDone(process)


def writeSpectrogramToFile():
    pass



def collectAndWrite(iqDirPath, seriesDirPath, sampleRate, timeSignal, gain, numBug, numNoBug):
    # defining our classification labels
    labelsTypes = ['clean_', 'bug_']

    #get raw iq data recorded into iqDirPath
    bugCenterFreq = 0
    noBugCenterFreq = 0
    if(numBug > 0):
        bugCenterFreq = UI.requestBugCenterFrequency()

    if(numNoBug > 0 ):
        noBugCenterFreq = UI.requestNoBugCenterFrequency()


    collectExamples(outDir=iqDirPath, sampleRate=sampleRate,timeSignal= timeSignal,gain=gain,numBugsExamples=numBug,
                    numNoBugsExamples=numNoBug, bugCenterFrequency= bugCenterFreq,
                    noBugCenterFrequency= noBugCenterFreq, bugFileLabel=labelsTypes[1], noBugFileLabel = labelsTypes[0])



    #extract a list of spectrograms from the raw iq data directory
    specs, freqLists, timeLists, labelsInNums, ids = SignalRead.extractSpecsFromIQDir(iqDirPath, sampleRate,
                                                                                     bugCenterFreq, noBugCenterFreq,
                                                                                      bugWordLabel= labelsTypes[1], noBugWordLabel=labelsTypes[0])
    print "labels in nums: ", labelsInNums
    print "ids: ", ids

    # spreadDenom = 0.000001
    # spreadDenom = 8.25
    #TODO: look into exception handling for handling the could not find optimal parameters error
    #TODO: such that you can adjust 0.000001 when error comes up

    #turn those spectrograms into series
    specsSeries = SignalProcess.extractResWithCenterOfMassMultSpecs(specs, freqLists)

    #save the series into files in a directory
    writeMultSeriesToFiles(seriesDirPath, specsSeries, timeLists, labelsInNums, labelsTypes, ids)


def mainUserPrompts():
    UI.writeWelcome()
    iqDirPath, seriesDirPath, sampleRate, timeSignal, gain, numBug, numNoBug= UI.requestVarsOFSignalWriting()

    ''''''''''''''''''''''''''''''

    #TODO March 14: Make  this function and all funcs that come within use centerFreqBug and centerFreqNoBug


    ''''''''''''''''''''''''''''''''




    collectAndWrite(iqDirPath, seriesDirPath, sampleRate, timeSignal,  gain, numBug, numNoBug)



'''
Program flow:
receive signal recording parameters from commandline arguments
record n signals according to the parameters specified
'''

def mainCommandLine():
    # Make examples
    # get these as commandline arguments: outDir, n, sampleRate, timeSignal, centerFreq, gain
    UI.writeWelcome()
    if(len(sys.argv)!=8):
        print "Error: Wrong number of arguments. \n" \
              "Command example: python SignalWrite.py iqDirPath, seriesDirPath, sampleRate, timeSignal, centerFreq, gain"
        exit(1)
    iqDirPath = sys.argv[1]
    seriesDirPath = sys.argv[2]
    sampleRate = int(sys.argv[3])
    timeSignal = float(sys.argv[4])
    numBugExamples = int(sys.argv[5])
    numNoBugExamples = int(sys.argv[6])
    gain = int(sys.argv[7])

    collectAndWrite(iqDirPath= iqDirPath,seriesDirPath=seriesDirPath,sampleRate=sampleRate,timeSignal=timeSignal,
                    gain=gain,numBug=numBugExamples, numNoBug=numNoBugExamples)



if __name__ == '__main__':
    mainCommandLine()



