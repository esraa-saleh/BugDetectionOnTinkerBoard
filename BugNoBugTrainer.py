import model
import UI
'''
Assumes there is a directory with examples
'''
def main():

    # dataDirPath = '/home/esraa/PycharmProjects/radioSignalPestDet/bug_no_bug_examples_small'
    wordLabelTypes = ['no_bug', 'bug']
    # wordLabelTypes = ['clean', 'ad', 'slar', 'blar', 'pu']
    #
    # bugNoBugMap = {'clean': 0, 'ad': 1,
    #                'pu': 1, 'slar': 1,
    #                'blar': 1}

    UI.trainWelcome()
    dataDirPath = UI.requestDataDirPath()
    acc, accClasses, misClass = model.crossValSVMModel(dataDirPath = dataDirPath, wordLabelTypes=wordLabelTypes)

    print acc

if __name__ == '__main__':
    main()