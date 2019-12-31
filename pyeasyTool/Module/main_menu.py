import os
import base
import led
import wifi
import alexa
import bt
import development
import fastboot_all

class MainMenu(base.Base):
    this_version="3.0"
    menu_array=("Set LED Pattern",\
                "WiFi Connection",\
                "Alexa Onboard",\
                "BT Modify",\
                "Development",\
                "Fastboot Flash",\
                "Reboot",\
                "Quit")

    def run(self):
        while True:
            print("\tVersion: %s"%self.this_version)
            print("\tDevice : %s exist"%base.get_device_num())
            self.display()
            self.get_num()
            if (self.input is 0):
                continue
            elif (self.input is 1):
                led.Led(led.Led.led_menu_array).run()
            elif (self.input is 2):
                wifi.Wifi(wifi.Wifi.wifi_menu_array).run()
            elif (self.input is 3):
                alexa.Alexa().run()
            elif (self.input is 4):
                bt.Bt(bt.Bt.bt_menu_array).run()
            elif (self.input is 5):
                development.Development().run()
            elif (self.input is 6):
                fastboot_all.FastbootImage().run()
            elif (self.input is 7):
                os.system('adb reboot')
                os._exit(0)
            elif (self.input is 8):
                os._exit(0)
            else:
                print("error")
                continue







