import RPi.GPIO as GPIO
import time
from .conf import Conf_relay_pin

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def relay_on():
    print("relay set to on")
    GPIO.setup(Conf_relay_pin, GPIO.OUT)
    GPIO.output(Conf_relay_pin,GPIO.HIGH)


def relay_off():
    print("relay set to off")
    GPIO.setup(Conf_relay_pin, GPIO.OUT)
    GPIO.output(Conf_relay_pin, GPIO.LOW)