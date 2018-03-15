import pickle
import UI
import SignalWrite
import SignalProcess
import SignalRead
from model import getFeaturesFromSeries

def main():
    clf = pickle.load(open('savedModel', 'rb'))
    UI.userDetectionWelcome()

    fileNameSig = 'userSignal.txt'
    samplingRate, centerFreq, gain, timeSig = UI.setupPrompts()
    sig_OK = UI.requestNextKernel()
    # spreadDenom = 0.000001


    #fileName, series, timeList, showProgress = True

    while(sig_OK):
        #record the signal
        SignalWrite.writeSignal(currFile=fileNameSig, sampleRate=samplingRate, centerFreq=centerFreq, gain= gain, timeSignal=timeSig)
        spec, freqs, t = SignalRead.extractSpecFromIQFile(inFile=fileNameSig, sampleRate=samplingRate, centerFreq=centerFreq)
        # series = SignalProcess.extractResonantWithFit(spec=spec,freqList=freqs, spreadDenom=spreadDenom)
        series = SignalProcess.centerOfMassMethodSeries(spec, freqs)
        x = getFeaturesFromSeries(series=series)

        pred = clf.predict([x])
        #pred can either be 1 (bug) or 0 (no bug)
        print pred
        UI.showPrediction(pred[0])
        sig_OK = UI.requestNextKernel()

if __name__ == '__main__':
    main()