import BugNoBugTrainer
import BugNoBugUser
import SignalWrite
import UI
import sys
import re


'''
Description: This is the main driver of the pest detection control flow. 

This script runs in two modes:
    
    1) interactive mode
       
       This mode will ask for your input to initialize settings
       launch command: python main.py 1

       -Continue according to instructions displayed after launching witht this command

    2) Non-interactive mode
       
       General format of launch command: 
       python main.py 2 selection settingsFile

       where # indicates a pathway, explained below.

       This mode will not ask for your input for initializing settings,
       instead it expects that you have a file with all settings in it.

       - This mode has three pathways:

       a) Build a Dataset
       launch command: python main.py 2 1 DatasetBuildSettings

           - this pathway helps you build a dataset, that you can base your model on.
           - Your text file, DatasetBuildSettings, will have the settings needed.
             It needs to be formatted as follows:
                path to where IQ files can be stored
                path to where extracted series can be stored
                sampling rate
                time of signal (can only be between 1 and 7, if you do not want to run out of memory on a Raspberry Pi)
                number of desired examples from the bug category
                number of desired examples from the clean category
                center frequency for bug examples
                center frequency for clean examples (this might be a duplicate
                of the center frequency for bug examples in most use cases,
                but its so useful to customize for simulations and debugging)

                
                

       b) Fit a model
       launch command: python main.py 2 2 ModelBuildSettings
           
           -this pathway helps you fit a model on the dataset that you gathered.
           - Your text file, ModelBuildSettings, needs to be formatted as folliows:
                 path to the dataset that you gathered

       c) Detect Bugs in Kernels
       launch command: python main.py 2 3 DetectionSettings
       
           -this pathway is for detecting bugs in grain kernels given a model.
           - Your text file, DetectionSettings needs to be formatted as follows:
                 sampling rate
                 gain
                 time for your signal (can only be between 1 and 7, if you do not want to 
                 run out of memory on the Raspberry Pi )
                 center frequency to aim for

'''


def mainTextFileIn():
    selection = int(sys.argv[2])
    settingsFile = sys.argv[3]
    if(selection == 1):
    
        SignalWrite.mainSettingsFromFile(settingsFile)
    
    elif(selection == 2):
        BugNoBugTrainer.mainSettingsFromFile(settingsFile)

    elif(selection == 3):
        BugNoBugUser.mainSettingsFromFile(settingsFile)
    
    else:
        print "ERROR: Invalid selection argument"



def mainInteractive():
    #Welcome message
    UI.programBanner()
    selection = UI.mainMenu()

    quitNow = False
    while(not quitNow):
        if(selection == 1):
            SignalWrite.mainUserPrompts()
            selection = UI.mainMenu()

        elif(selection == 2):
            #fitting
            BugNoBugTrainer.main()
            selection = UI.mainMenu()
        elif(selection == 3):
            BugNoBugUser.main()
            selection = UI.mainMenu()

        elif(selection == 4):
            quitNow = True
            print "Exiting The Pest Detection Program..."

        else:
            print "Invalid choice, try again."
            selection = UI.mainMenu()



if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print "ERROR: incorrect number of arguments. Refer to documentation."
        exit(1)

    mode = int(sys.argv[1])

    if(mode == 1):
        mainInteractive()

    elif(mode == 2):
    
        mainTextFileIn()
    else:
        print "ERROR: Invalid mode argument"
