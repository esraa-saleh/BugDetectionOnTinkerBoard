import pickle
import UI
import SignalWrite
import SignalProcess
import SignalRead
from model import getFeaturesFromSeries
import SettingsDataReader
import time

'''
Description: If you have a fitted model on data, and you would like to start detecting with that model,
you may use this driver program.
For this iteration of the code, your model needs to be named 'savedModel'.
It is more elegant to let the main.py driver program launch this program, but if you want to run this on its own:
    python BugNoBugUser.py

'''


'''
Function: mainSettingsFromFile
Purpose: a function that drives the detection control flow. 
It reads in settings for detection, records a signal, processes it,
launches a saved model, puts the processed signal into that model,
to obtain a prediction about whether the signal corresponds to a bug signal or not

Input: settingsFile, a file formatted according to the documentation in main.py, that contains detection settings



'''
#TODO: needs to not be interactive (interactive parts will be eliminated when we get buttons and LEDs) 
def mainSettingsFromFile(settingsFile):

    with open(settingsFile, 'r') as f:
        settings = f.readlines()
        settings = [settings[i].strip() for i in range(len(settings))]
        clf = pickle.load(open('savedModel','rb'))
        fileNameSig = 'userSignal.txt'
        settingsPath = 'model_data_settings.txt'
 
        samplingRate = int(settings[0])
        gain = int(settings[1])
        timeSig = int(settings[2])
        centerFreq = int(settings[3])
        UI.collectExampleOnButtonPress()
     
        while(True):
           #record the signal
           time.sleep(5)
           SignalWrite.writeSignal(currFile=fileNameSig, sampleRate=samplingRate, centerFreq=centerFreq, gain= gain, timeSignal=timeSig+1)
        
           spec, freqs, t = SignalRead.extractSpecFromIQFile(inFile=fileNameSig, sampleRate=samplingRate, centerFreq=centerFreq)
        
        
           series = SignalProcess.centerOfMassMethodSeries(spec, freqs)
           # remove the first second - it sometimes contains unintended spikes, for some unknown reason 

           index = 0
           while(t[index]<1.0):
              index+=1

        
           series = series[index:]
           t = t[index:]
           
           # make the time series smoother
           t = SignalProcess.rollingAverage(t, 10)
           series = SignalProcess.rollingAverage(series, 10)
           #TODO: remove plotting bug-no bug indication is done with LEDs
           UI.plotResFreqs(t, series)

           settingsObj = SettingsDataReader.SettingsDataReader(settingsPath=settingsPath)
           thresh = settingsObj.getThresh()

           x = getFeaturesFromSeries(series=series, thresh= thresh)

           pred = clf.predict([x])
           #pred can either be 1 (bug) or 0 (no bug)
           print pred

           #TODO: when changing to indication with LEDs, modify showPrediction from the UI file
           UI.showPrediction(pred[0])

           #TODO: when changing to indication of taking a measuremnet using a button, change requestNextKernel from the UI file
           UI.collectExampleOnButtonPress()

        
'''
Function: main
Purpose: driver of the interactive mode for detection (user interacts with text)

'''

def main():

    clf = pickle.load(open('savedModel', 'rb'))
    UI.userDetectionWelcome()

    fileNameSig = 'userSignal.txt'
    settingsPath = 'model_data_settings.txt'

    samplingRate,gain, timeSig = UI.setupPrompts()
    sig_OK = UI.requestNextKernel()
    # spreadDenom = 0.000001


    #fileName, series, timeList, showProgress = True

    while(sig_OK):
        #record the signal

        minFreq, maxFreq, centerFreq = UI.requestDetectionFreqSetup()
        while(minFreq>maxFreq or maxFreq<centerFreq or centerFreq<minFreq):
            print "Error: frequencies need to satisfy: min frequency < center frequency < max frequency ."
            minFreq, maxFreq, centerFreq = UI.requestDetectionFreqSetup()

        time.sleep(5)
        SignalWrite.writeSignal(currFile=fileNameSig, sampleRate=samplingRate, centerFreq=centerFreq, gain= gain, timeSignal=timeSig+1)
        
        spec, freqs, t = SignalRead.extractSpecFromIQFile(inFile=fileNameSig, sampleRate=samplingRate, centerFreq=centerFreq,
                                                          specMinFreq=minFreq, specMaxFreq=maxFreq)
        print "Spec dimensions: ", spec.shape
        
        series = SignalProcess.centerOfMassMethodSeries(spec, freqs)
        # remove the first second
        
        index = 0
        while(t[index]<1.0):
            index+=1

        
        series = series[index:]
        t = t[index:]
        print "length of series after cut: ", len(series)
        t = SignalProcess.rollingAverage(t, 10)
        series = SignalProcess.rollingAverage(series, 10)

        UI.plotResFreqs(t, series)

        settingsObj = SettingsDataReader.SettingsDataReader(settingsPath=settingsPath)
        thresh = settingsObj.getThresh()

        x = getFeaturesFromSeries(series=series, thresh= thresh)

        pred = clf.predict([x])
        #pred can either be 1 (bug) or 0 (no bug)
        print pred
        UI.showPrediction(pred[0])
        sig_OK = UI.requestNextKernel()

if __name__ == '__main__':
    main()
