# -*- coding: utf-8 -*-
import os
import whl

THIS_VERSION="3.0"
menu_array="Set LED Pattern",\
           "WiFi Connection",\
           "Alexa Onboard",\
           "BT Modify",\
           "Development",\
           "Reboot",\
           "Quit"

class Base:
    def __init__(self,array):
        self.array=array
    def display(self):
        for i in range(0,len(self.array),1):
            print("\t%d. %s"%(i+1,self.array[i]))
    def get_num(self):
        menuNum=eval(input("Enter Number:"))
        if ((menuNum-1) < len(self.array)):
            self.input=menuNum

    def run(self):
        while True:
            print("\tVersion: %s"%THIS_VERSION)
            print("\tDevice : %s exist"%deviceNum)
            self.display()
            self.get_num()
            if (self.input is 1):
                print("Set LED Pattern")
            elif (self.input is 2):
                wifiMenu=whl.Wifi(whl.wifi_menu_array)
                wifiMenu.run()
            elif (self.input is 3):
                alexaMenu=whl.Alexa()
                alexaMenu.run()
            elif (self.input is 4):
                btMenu=whl.Bt(whl.bt_menu_array)
                btMenu.run()
            elif (self.input is 5):
                print("Development")
            elif (self.input is 6):
                os.system('adb reboot')
            elif (self.input is 7):
                break
            else:
                print("error")



if __name__ == '__main__':
    commandInfo=os.popen('adb devices').read()
    deviceNum=commandInfo.split("\t")[0].split("\n")[1]

    if (len(deviceNum)==0):
        print("devices not exist, re-plug USB or reboot please")
    else:
        mainMenu=Base(menu_array)
        mainMenu.run()



