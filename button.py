import ASUS.GPIO as GPIO
import time

def listenButtonPress(pin):
    sig = 1
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.ASUS)
    GPIO.setup(pin, GPIO.IN)
    while(sig != 0):
        sig = GPIO.input(pin)
        print(str(sig))
        time.sleep(0.25)



def listenButtonHold(pin):
    # keep track of 5 most recent button press values,
    # if all are 0, then consider it a hold
    pass



