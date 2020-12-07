import RPi.GPIO as GPIO
import time
from .conf import Conf_led_flash_pin

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def light_on():
    print("the light is blink~~~~~~~")
    GPIO.setup(Conf_led_flash_pin, GPIO.OUT)
    GPIO.output(Conf_led_flash_pin,GPIO.HIGH)


def light_off():
    print("the light is off~~~~~~~")
    GPIO.setup(Conf_led_flash_pin, GPIO.OUT)
    GPIO.output(Conf_led_flash_pin, GPIO.LOW)

if __name__ == '__main__':
    main()