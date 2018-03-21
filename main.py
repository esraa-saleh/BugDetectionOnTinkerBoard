import BugNoBugTrainer
import BugNoBugUser
import SignalWrite
import UI

def main():
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
    main()