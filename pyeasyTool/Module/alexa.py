import base
import wifi
import bt
import threading
from time import sleep
import os

class Alexa(base.Base):
    alexa_menu_array="Alexa OneStep Activate",\
                "Alexa Activate",\
                "Alexa InActivate",\
                "Back"

    def __alexa_activate(self):
        threading.Thread(target=base.monitor).start()
        sleep(1)
        os.system('''adb shell "adk-message-send 'voiceui_start_onboarding{client:\\"AVS\\"}'"''')
    
    def __alexa_inactivate(self):
        threading.Thread(target=base.monitor).start()
        sleep(1)
        os.system('''adb shell "adk-message-send 'voiceui_delete_credential {client:\"AVS\"}'"''')
        sleep(1)
        os.system('''adb shell "systemctl restart voiceUI"''')
    
    def __alexa_onestep_activate(self):
        self.bt_instance = bt.BtAddress(bt.Bt.bt_address_modify_menu_array)
        self.wifi_instance = wifi.Wifi(wifi.Wifi.wifi_menu_array)
        self.bt_instance.bt_solid_address()
        sleep(1)
        self.wifi_instance.wifi_connect()
        sleep(1)
        pause=input("\nAny key to Continue when AVSLED flash GREEN twice")
        self.__alexa_activate()	

    def run(self):
        while True:
            print("\tAlexa Menu\n")
            self.display()
            self.get_num()
            if (self.input is 0):
                continue
            elif (self.input is 1):
                self.__alexa_onestep_activate()
            elif (self.input is 2):
                self.__alexa_activate()
            elif (self.input is 3):
                self.__alexa_inactivate()
            elif (self.input is 4):
                break
            else:
                print("error")
