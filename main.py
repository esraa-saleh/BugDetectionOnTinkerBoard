import BugNoBugTrainer
import BugNoBugUser
import SignalWrite
import UI

def main():
    selection = UI.mainMenu()
    if(selection == 1):
        SignalWrite.mainUserPrompts()

    elif(selection == 2):
        #fitting
        BugNoBugTrainer.main()
    elif(selection == 3):
        BugNoBugUser.main()

if __name__ == '__main__':
    main()