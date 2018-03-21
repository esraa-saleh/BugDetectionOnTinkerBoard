


def askTimeInterval():
    t = float(raw_input("Enter receiving time interval: "))
    return t

def askNumExamples():
     n = int(raw_input("Enter the number of examples needed: "))
     return n

def quitOrContinue(message=''):
    print message
    option = raw_input('---->')
    if (option == "q"):
        return 0
    else:
        return 1

def noticeCollectBugsExamples():
    return quitOrContinue("Make sure that the transmitter is sending BUG examples.\n "
                   "We intend to start collecting examples now. To start type any key. To quit type q. ")



def noticeCollectNoBugsExamples():
    return quitOrContinue("Make sure that the transmitter is sending NO BUG examples.\n"
          "We will start collecting examples now. To start type any key. To quit type q. ")


def requestNextKernel():
    message = "Please insert a kernel to be scanned. Enter q to quit. Enter any other key to continue."
    return quitOrContinue(message)

def requestNumBugNoBugExamples():
    bugNumExamples = int(raw_input("Target number of bug examples: "))
    noBugNumExamples = int(raw_input("Target number of no bug examples: "))

    return bugNumExamples, noBugNumExamples

def declareProcessDone(processName):
    print processName, "done ..."

def declareProcessStart(processName):
    print "Starting", processName , "..."

def userDetectionWelcome():
    print "---------------------------------------------------------------------\n"\
          "==================== Pest In Grain Kernel Detector ==================\n" \
          "---------------------------------------------------------------------\n"

def trainWelcome():
    print "-------------------------------------------------------------------------------\n" \
          "==================== Pest In Grain Kernel - Model Builder =====================\n" \
          "-------------------------------------------------------------------------------\n"

def writeWelcome():
    print "-------------------------------------------------------------------------------\n" \
          "==================== Pest In Grain Kernel - Data set Builder ==================\n" \
          "-------------------------------------------------------------------------------\n"

#TODO: need to change this pipeline to requesting bug/no bug center frequencies
def setupPrompts():
    print "To prepare for detection, we need the following settings:\n"
    samplingRate = raw_input('Sampling Rate       ---> ')
    gain         = raw_input('Gain                ---> ')
    timeSig      = raw_input('Time Span of Signal ---> ')

    return int(samplingRate), int(gain), float(timeSig)



# def requestChangeFrequency():
#     change = raw_input("Would you like to change the center frequency ? (y) yes ,  (any key) No ")
#     if(change == 'y'):
#         frequency = int(raw_input("Center Frequency ---> "))
#         return frequency
#     else:
#         return 0
def requestBugCenterFrequency():
    return int(raw_input('Bug examples center frequency ---> '))

def requestNoBugCenterFrequency():
    return int(raw_input('No bug examples center frequency ---> '))

def requestMinMaxFreqOfCategory(category):
    print "To decide on the range of frequencies of interest for "+category+ ", please enter the following: "
    minFreq = int(raw_input('Min frequency for '+category+' category: '))
    maxFreq = int(raw_input('Max frequency for '+category+' category: '))
    return minFreq, maxFreq

def requestDetectionFreqSetup():
    print "Specify a center frequency: "
    centerFreq = int(raw_input('Center frequency ---> '))
    print "Specify the frequency range to focus on: "
    minFreq = int(raw_input('Min frequency: '))
    maxFreq = int(raw_input('Max frequency: '))

    return minFreq, maxFreq, centerFreq

def showPrediction(bugBool):

    if(bugBool):
        print "There is a BUG in this kernel!"
    else:
        print "There is NO BUG in this kernel!"

def requestDataDirPath():
    dataDirPath = raw_input("Please enter the path to your gathered data (To quit enter q) : ")

    return dataDirPath

def requestVarsOFSignalWriting():
    print "In order to record signals, we need to setup a few variables..."
    iqDirPath = raw_input("Directory Path for IQ Data ---> ")
    seriesDirPath = raw_input("Directory Path for Extracted Time Series ---> ")
    sampleRate = int(raw_input("Sampling rate ---> "))
    timeSignal = float(raw_input("Total time span of a signal ---> "))
    gain = int(raw_input("Gain ---> "))
    numBug, numNoBug = requestNumBugNoBugExamples()

    return iqDirPath, seriesDirPath, sampleRate, timeSignal, gain, numBug, numNoBug

def programBanner():
    print "===========================================================================\n" \
          "=                                                                         =\n" \
          "=                       The Pest Detection Program                        =\n" \
          "=                                                                         =\n" \
          "==========================================================================="

def mainMenu():

    print "\nTo select an option, please enter the number corresponding to it:\n" \
          "1) Build A Bug/NoBug Dataset \n" \
          "2) Fit A Model Based on a Dataset \n" \
          "3) Detect Bugs in Grain Kernels \n" \
          "4) Quit the program"

    selection = int(raw_input("--->"))

    return selection


