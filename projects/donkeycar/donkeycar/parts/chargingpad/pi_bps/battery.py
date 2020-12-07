from ctypes import *

#load the shared object file

#adder = CDLL('./lipo_fuleguage-v10.so')
 
def get_battery_level():
    #battery_level = adder.read_percent()
    battery_level = 20
    print ("the get_battery_level:",battery_level)
    return battery_level

if __name__ == '__main__':
    main()