import can_Common.can_BT
import RPi.GPIO as GPIO

def get_Light():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN)

    if GPIO.input(18):
        return True
    else:
        return False
