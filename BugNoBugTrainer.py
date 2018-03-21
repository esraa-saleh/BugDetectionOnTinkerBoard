import model
import UI
'''
Assumes there is a directory with examples
'''
def main():

    # dataDirPath = '/home/esraa/PycharmProjects/radioSignalPestDet/bug_no_bug_examples_small'
    sig_OK = True
    while(sig_OK):
        wordLabelTypes = ['clean', 'bug']
        # wordLabelTypes = ['clean', 'ad', 'slar', 'blar', 'pu']
        #
        # bugNoBugMap = {'clean': 0, 'ad': 1,
        #                'pu': 1, 'slar': 1,
        #                'blar': 1}

        UI.trainWelcome()
        dataDirPath = UI.requestDataDirPath()

        if(dataDirPath != 'q'):
            acc, accClasses, misClass = model.crossValSVMModel(dataDirPath = dataDirPath, wordLabelTypes=wordLabelTypes)
            print accClasses

        else:
            sig_OK = False


if __name__ == '__main__':
    main()