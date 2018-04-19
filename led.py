import ASUS.GPIO as GPIO


def changeLEDState(on, pin):

    GPIO.setmode(GPIO.ASUS)
    GPIO.setup(pin, GPIO.OUT)
    if(on == True):

        GPIO.output(pin, GPIO.HIGH)
        print "LED ON"
    else:

        GPIO.output(pin, GPIO.LOW)
        print "LED OFF"

