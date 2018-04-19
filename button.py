import ASUS.GPIO as GPIO
import time


def BUTTON_WATCH(pin):
    sig = 1
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.ASUS)
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    time.sleep(0.25)
    while True:
        sig = GPIO.input(pin)
        print(str(sig))
        time.sleep(0.01)

#BUTTON_WATCH(17)


def listenButtonPress(pin):
    sig = 1
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.ASUS)
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    time.sleep(0.25)
    while(sig != 0):
        sig = GPIO.input(pin)
        print(str(sig))
        time.sleep(0.0025)



def listenButtonHold(pin):
    # keep track of 5 most recent button press values,
    # if all are 0, then consider it a hold
    pass



