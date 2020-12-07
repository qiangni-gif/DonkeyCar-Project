from .battery import get_battery_level
from .make_led_flash import light_on,light_off
from .navigate_car import navigate_to_cps
import requests
from .conf import Conf_led_pin_list, Conf_lowest_battery_level, Conf_url, Conf_relay_on, Conf_relay_off
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
def check_battery_level():
    try:
        bl = get_battery_level()
        if bl <= Conf_lowest_battery_level:
            return "low",bl
        elif bl > Conf_lowest_battery_level and bl < Conf_highest_battery_level:
            return "normal",bl
        else:
            return "full",bl
    except:
        traceback.print_exc()
        return "none",0

def light_led(bl=30):
    led_num =int(bl/10)
    for num in range(led_num):
        print("the num is:",num)
        light_on(Conf_led_pin_list[num])
        light_off(Conf_led_pin_list[num])

def make_cps_relay_on():
    res = requests.get(Conf_url+Conf_relay_on)
    return res.json()

def make_cps_relay_off():
    res = requests.get(Conf_url+Conf_relay_off)
    return res.json()


def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    t = 2
    i = 0
    while True:
        res ,bl= check_battery_level()
        print("battery is",res)
        light_led(bl)
        if res == "low":
            print("enter low")
            navigate_to_cps()
            make_cps_relay_on()
        elif res == "normal":
            pass
        elif res == "full":
            print("enter full")
            make_cps_relay_off()
        relay_pin = GPIO.input(24)
        light_pin = GPIO.input(25)
        print("pin 24 is", relay_pin)
        print("pin 25 is", light_pin)
        i = i+1
        if i == t:
            make_cps_relay_off()
            relay_pin = GPIO.input(24)
            light_pin = GPIO.input(25)
            print("pin 24 is", relay_pin)
            print("pin 25 is", light_pin)
            return False
        

# if __name__ == '__main__':
#     main()