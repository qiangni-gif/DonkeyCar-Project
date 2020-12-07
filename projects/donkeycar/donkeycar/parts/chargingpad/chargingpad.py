from donkeycar.parts.chargingpad.pi_bps.main import make_cps_relay_on, make_cps_relay_off, light_on, light_off
from  donkeycar.parts.chargingpad.PCF8591 import PCF8591, convertion

class ChargingPad(object):
    
    def __init__(self):
        self.current_charging_state = False
        self.count= 0
        self.current_led_state = False
        self.PCF8591 = PCF8591
        light_off(20)

    def run(self, charging_state_in):

        #print("charging_state_in: ",charging_state_in)
        if charging_state_in is True:
            if not self.current_charging_state :
                if (self.count % 10 == 0):
                    print("count: ",self.count)
                    try:
                        res = make_cps_relay_on()
                        print("res:", res)
                        if res["desc"] == "success":
                            self.current_charging_state = True
                        else:
                            self.current_charging_state = False   
                    except:
                        print("unable to send msg")

                    
                self.count = self.count + 1         
        else:
            if self.current_charging_state :
                if (self.count % 10 == 0):
                    print("count: ",self.count)
                    try:
                        res = make_cps_relay_off()
                        print("res:", res)
                        if res["desc"] == "success":
                            self.current_charging_state = False
                        else:
                            self.current_charging_state = True
                    except:
                        print("unable to send msg")
                    
                self.count = self.count + 1

        A = convertion(1)
        if (A >= 200):
            print("reading is: ",A)
            light_on(20)
        else:
            light_off(20)
        #print("charging_state_out is :",self.current_charging_state)
        return self.current_charging_state

    def shutdown(self):
        pass