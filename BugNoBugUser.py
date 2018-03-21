import pickle
import UI
import SignalWrite
import SignalProcess
import SignalRead
from model import getFeaturesFromSeries
import SettingsDataReader
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

        SignalWrite.writeSignal(currFile=fileNameSig, sampleRate=samplingRate, centerFreq=centerFreq, gain= gain, timeSignal=timeSig)
        spec, freqs, t = SignalRead.extractSpecFromIQFile(inFile=fileNameSig, sampleRate=samplingRate, centerFreq=centerFreq,
                                                          specMinFreq=minFreq, specMaxFreq=maxFreq)
        series = SignalProcess.centerOfMassMethodSeries(spec, freqs)

        # series = SignalProcess.extractResonantWithFit(spec=spec,freqList=freqs, spreadDenom=spreadDenom)
        # series = SignalProcess.centerOfMassMethodSeries(spec, freqs)

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