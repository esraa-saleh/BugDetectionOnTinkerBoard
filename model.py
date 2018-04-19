import numpy as np
import SignalRead
import os
import random
from scipy.stats import kurtosis, skew
from random import shuffle
import copy
from sklearn.svm import SVC
from random import randint
import pickle
from sklearn import preprocessing
from pathlib2 import Path
from collections import Counter
import json
import yaml


NUM_FEATURES =2

'''
Function: calculateThresh

Purpose : to calculate a threshold based on series from clean examples. The threshold is the average difference between
          a clean example's series' min and max.

Input   : seriesDirPath, string, path to the directory containing series files
          threshCalcFiles, list of strings, all names of files that contain series reserved for threshold calculation
          saveThresh, boolean, optional parameter useful for saving the threshold in a file that can be used later

Output  : thresh, float, the caluculated threshold as described in the purpose

'''
def calculateThresh(seriesDirPath, threshCalcFiles, saveThresh = True):
    count = 0
    total = 0
    for i in range(len(threshCalcFiles)):
        if ('clean' in threshCalcFiles[i]):
            count += 1
            series = SignalRead.extractSeriesOnly(seriesDirPath + '/' + threshCalcFiles[i])
            total += max(series) - min(series)
    thresh = total / count


    #save thresh to settings file
    if(saveThresh):

        settingsPath = 'model_data_settings' + '.txt'
        settingsPathObj = Path(settingsPath)
        newEntry = {'thresh': thresh}

        if(settingsPathObj.exists()):
            with open(settingsPath) as setFile:
                settingsDict = yaml.safe_load(setFile)
            settingsDict.update(newEntry)

        else:
            settingsDict = newEntry

        with open(settingsPath, 'w') as setFile:
            setFile.write(json.dumps(settingsDict))

    return thresh



#def getSeriesFromFile(inFile):
#    _, series = SignalRead.extractSeriesFromFile(inFile)
#    return series


'''
Function: getFeaturesFromSeries

Purpose : to calculate features based on a given series

Input   : series, list or array of floats, a sequence of values where each is expected to be frequency 
          thresh, float, a threshold that will be used in calculating the score feature

Output  : features, numpy array, all the features that were calulated on the given series

'''
def getFeaturesFromSeries(series, thresh):

    features = np.empty(NUM_FEATURES, dtype='float64')
    features[0] = kurtosis(series)
    # %90 ACCURACY FOR BOTH CATEGORIES WHEN NUMCOLS = 100
    features[1] = scoreSeries(series, 100, thresh)
    return features

'''
Function: getOneExampleFromFile

Purpose : given a file that has a time series, this function obtains features calculated based on that time series

Input   : inFile, string, name of file containing the series from which features will be extracted
          thresh, float, threshold as calculated by the function: calculateThresh

Output  : features, numpy array, sequence of all features needed to describe an example

'''

def getOneExampleXFromFile(inFile, thresh):
    series = SignalRead.extractSeriesOnly(inFile)
    print inFile
    features = getFeaturesFromSeries(series, thresh)
    return features


'''
Function: getAllLabelsFromFiles

Purpose : to obtain numerical  labels from a list of file names assuming the file names were representative
          of the class that

Input   : inFilesList, list or array of strings, sequence of strings each bieng a file name 
          labelTypes, list or array of strings, sequence of strings each bieng a keyword for a 
          certain class that is expectd to appear in the given file list

Output  : list of ints, sequence of numercial labels that is parallel to inFilesList such that each element
          of inFilesList corresponds the numerical label at the same index. Each label indicates the classs that
          a file belongs to

'''

def getAllLabelsFromFiles(inFilesList, labelTypes):
    return SignalRead.extractSpecNumLabelsFromFiles(inFilesList, labelTypes)



'''


'''

def getXYFromFiles(thresh, dirPath, allFiles, labelTypes):
    X = np.empty(shape=(len(allFiles), NUM_FEATURES), dtype='float64')

    for i in range(len(allFiles)):
        features = getOneExampleXFromFile(dirPath + '/' + allFiles[i], thresh)
        for x in range(len(features)):
            X[i][x] = features[x]

    Y = getAllLabelsFromFiles(allFiles, labelTypes)
    return X, Y




#TODO: deal with len(series)%numCols !=0

def scoreSeries(series, numCols, thresh, distFactor = 1e5):
   
    # distFactor = 1e5, was determined for the actual bugs dataset not the demo

    if(numCols > len(series)):
        print "Error: attempting to split series into columns such that " \
              "the number of columns is more than the number of series points"
        exit(1)

    score = 0
    lenSubSeries = (len(series))//(numCols)
    for i in range(0, numCols, lenSubSeries):
        dist = max(series[i: i+lenSubSeries]) - min(series[i: i+ lenSubSeries])
        if(dist > thresh):
            score += dist*distFactor

    return score


def shuffleXY(X, Y):

    indices = [i for i in range(len(X))]

    shuffle(indices)
    shuffX = []
    shuffY = []
    for i in range(len(indices)):
        shuffX.append(X[indices[i]])
        shuffY.append(Y[indices[i]])

    return shuffX, shuffY, indices

def wordNumDictionaries(wordLabelTypes):
    numOfLabelTypes = len(wordLabelTypes)
    wordToNum = {}
    numToWord = {}
    for i in range(0, numOfLabelTypes):
        wordToNum[wordLabelTypes[i]] = i
        numToWord[i] = wordLabelTypes[i]

    return wordToNum, numToWord

def getClassFrequencies(Y, classesInNums):
    freqsMap = {}
    # initialize map
    for x in range(len(classesInNums)):
        freqsMap.update({classesInNums[x]: 0})

    for i in range(len(Y)):
        if(Y[i] in classesInNums):
            freqsMap[Y[i]] +=1

    return freqsMap

def applyAdditionalMapping(lowerNumToWordMap, higherNumToWordMap, Y):
    # Y has nums corresponding to distinct file types
    # firstMap maps a number to a word label
    # second map will map that word to a new number (usually for grouping categories)
    map2WordLabels = set(higherNumToWordMap.keys())
    for i in range(len(Y)):

        if(lowerNumToWordMap[Y[i]] in map2WordLabels):
            Y[i] = higherNumToWordMap[lowerNumToWordMap[Y[i]]]
    return Y


def trainTestLOOCV(index, X, Y):
    X = np.array(X)
    Y = np.array(Y)
    testX = X[index]
    testY = Y[index]

    size = len(Y)
    indices = np.arange(size)
    trainX = X[indices[indices != index]]
    trainY = Y[indices[indices != index]]
    # trainX, testX = scaleTrainTestX(trainX, [testX])
    # print trainX
    return trainX, trainY, testX, testY


def scaleTrainTestX(trainX, testX):
    scaler = preprocessing.StandardScaler().fit(trainX)
    trainX = scaler.transform(trainX)
    testX = np.reshape(testX, (1, -1))
    testX = scaler.transform(testX)
    return trainX, testX



# TODO: make final model fit on all
def leaveOneOutCV(X, Y, classes, classFreqs, classifier,yOneHot = False, saveModel = True):
    print Y
    accClasses = {aKey: 0 for aKey in classes}
    sumAcc = 0
    numTrials = len(X)

    trialToSave = randint(0, numTrials)

    misClassifiedIndices = []
    for p in range(numTrials):
        #single example in each test

        trainX, trainY, testX, testY = trainTestLOOCV(p, X, Y)
        # trainX, testX = scaleTrainTestX(trainX, testX)
        # print trainX

        clf = copy.copy(classifier)
        clf.fit(trainX, trainY)


        #saves the randomly chosen model
        if(p == trialToSave and saveModel == True):
            print "Saving the model..."
            pickle.dump(clf, open('savedModel', 'wb'))

        # test
        correct = 0
        # use when not scaling
        # pred = clf.predict([testX])
        # use when doing scaling
        pred = clf.predict(testX)

        # predProba = clf._predict_proba([testX])
        # print "Prediction probabilities: ", predProba

        if(yOneHot):
            # pred is a one hot vector
            result = np.argmax(pred)
            true = np.argmax(testY)

        else:
            result = pred[0]
            true = testY

        print result, true

        if (result == true):
            correct += 1
            accClasses[result] += 1

        else:
            # print result
            misClassifiedIndices.append(p)


        sumAcc += float(correct)

    acc = sumAcc/numTrials
    for ind in range(len(classes)):

        accClasses[classes[ind]] = float(accClasses[classes[ind]]) / float(classFreqs[ind])
        print accClasses[classes[ind]], classFreqs[ind]

    return acc, accClasses, misClassifiedIndices



def crossValSVMModel(dataDirPath, crossValFiles, threshCalcFiles, wordLabelTypes, bugNoBugMap = None):
    #list all file names
    allFiles = os.listdir(dataDirPath)

    #caluculate threshold on isolated set of clean examples
    thresh = calculateThresh(dataDirPath, threshCalcFiles)
    
    # get X and Y...if there is additional mapping,
    # then this Y is the first level (e.g. clean --> 0 , slar ---> 1, ad--->2)
    X, Y = getXYFromFiles(thresh, dataDirPath, allFiles, wordLabelTypes)

    # indices tells us where the original indices moved
    X, Y, indices = shuffleXY(X, Y)

    # obtain the mapping applied to Y as dicts
    wordToNum, numToWord = wordNumDictionaries(wordLabelTypes)

    #if there is an additional mapping required
    if(bugNoBugMap != None):
        # apply mapping (e.g. 0 --> clean --> 0,  1 --> slar --> 1, 2 --> ad--> 1 )
        Y = applyAdditionalMapping(numToWord, bugNoBugMap, Y)

        # get final numerical classes: e.g.  [0,1]
        classesInNums = sorted(list(set(bugNoBugMap.values())))

    else:
        #no additional mapping needed, e.g. []
        classesInNums = sorted(numToWord.keys())

    freqsMap = getClassFrequencies(Y, classesInNums)

    # Gamma 3.0 gives a slightly better result for the bug category
    clf = SVC(kernel='rbf', C=100, gamma=1.0, probability=True)
    print "----------------------------------------"
    print Y
    print [allFiles[indices[x]] for x in range(len(indices))]
    print "----------------------------------------"


    acc, accClasses, misClassifiedIndicies = leaveOneOutCV(X, Y, freqsMap.keys(), freqsMap.values(), clf)

    misClassedFiles = [allFiles[indices[misClassifiedIndicies[i]]] for i in range(len(misClassifiedIndicies))]
    print misClassedFiles
    return acc, accClasses, misClassedFiles


'''
Function : tempTestModel

Purpose  : This function was made to be run when the actual bugs in wheat dataset is being used (the one
           from Alex Reimer). It deals with the different naming convention. This is not needed when the model is 
           being trained on the dataset generated by the Bug Detector program. 

Input    : N/A

Output   : N/A

Print output: prints the overall accuracy, accuracy for each class, and all the misclassified files

'''
def tempTestModel():
    # dataDirPath = '/home/esraa/PycharmProjects/radioSignalPestDet/bug_no_bug_examples'
    # dataDirPath = '/home/esraa/PycharmProjects/radioSignalPestDet/bandSelection/seriesFiles'
    # dataDirPath = '/home/esraa/PycharmProjects/radioSignalPestDet/bug_no_bug_examples_train'
    dataDirPath = '/home/esraa/PycharmProjects/radioSignalPestDet/BugDetectorProgram/CleanVsSlarAdultsBlar'
    # wordLabelTypes = ['no_bug', 'bug']
    wordLabelTypes = ['clean', 'ad', 'slar', 'blar', 'pu']

    bugNoBugMap = {'clean': 0, 'ad': 1, 'pu':1,
                   'slar': 1,
                   'blar': 1}


    acc, accClasses, misClassF = crossValSVMModel(dataDirPath = dataDirPath, wordLabelTypes=wordLabelTypes, bugNoBugMap=bugNoBugMap)
    print acc, accClasses, misClassF
