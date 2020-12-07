import RPi.GPIO as GPIO
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def light_on(pin):
        # print("the light is blink~~~~~~~")
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)


def light_off(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

if __name__ == '__main__':
    main()