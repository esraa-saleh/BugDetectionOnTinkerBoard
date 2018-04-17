import model
import UI
import os
import random

'''
Description: This is the driver program for fitting data. It performs leave one out cross validation, considering that the sample size is almost always small (i.e. < 100 000 examples). 
Note that you will need to prepare a path to the directory with data.
Using the main driver program to launch this is more elegant, but you may run this alone using: 
    python BugNoBugTrainer.py
Then, follow the instructions.

'''

'''
Function:getFilesWithWord
Purpose : to extract all file names that contain a given word
Input   : allFiles, a list of file names
          word, a string keyword to search for

Output  : theFiles, all files that contain the keyword given

'''
def getFilesWithWord(allFiles, word):
    theFiles = []
    for f in allFiles:
        if(word in f):
            theFiles.append(f)
    return theFiles


'''
Function: mainSettingsFromFile
Purpose : Run the fitting-to-data procedure by reading initial settings from a file
Input   : settingsFile, string that is the name of the file conatining settings

'''

#Almost no interaction in this mode
def mainSettingsFromFile(settingsFile):
    wordLabelTypes = ['clean', 'bug']
    with open(settingsFile, 'r') as f:
        allArgs = f.readlines()
        dataDirPath = allArgs[0].strip()
        allFiles = os.listdir(dataDirPath)
        bugFiles = getFilesWithWord(allFiles, 'bug')
        cleanFiles = getFilesWithWord(allFiles, 'clean')
        #take 30% of clean files for threshold calculation
        random.shuffle(cleanFiles)

        threshCalcFiles = cleanFiles[:int(len(cleanFiles)*0.3)]
        crossValFiles = bugFiles + cleanFiles[int(len(cleanFiles)*0.3):]

        acc, accClasses, misClass = model.crossValSVMModel(dataDirPath = dataDirPath, crossValFiles = crossValFiles, threshCalcFiles = threshCalcFiles, wordLabelTypes=wordLabelTypes)
        print accClasses, misClass


'''
Function: main
Purpose : Run the fitting-to-data procedure by taking in initial settings
from the user with text based prompts and responses
'''

#Interactive mode
def main():

    
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
            allFiles = os.listdir(dataDirPath)
            bugFiles = getFilesWithWord(allFiles, 'bug')
            cleanFiles = getFilesWithWord(allFiles, 'clean')
            #take 30% of clean files for threshold calculation
            random.shuffle(cleanFiles)

            threshCalcFiles = cleanFiles[:int(len(cleanFiles)*0.3)]
            crossValFiles = bugFiles + cleanFiles[int(len(cleanFiles)*0.3):]

            acc, accClasses, misClass = model.crossValSVMModel(dataDirPath = dataDirPath, crossValFiles = crossValFiles, threshCalcFiles = threshCalcFiles, wordLabelTypes=wordLabelTypes)
            print accClasses, misClass

        else:
            sig_OK = False


if __name__ == '__main__':
    main()
