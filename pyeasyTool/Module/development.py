# -*- coding: utf-8 -*-
import base
import os
import threading

class Development():
    development_menu_list=["Monitor","GPIO Configuration"," ","Back"]

    def display(self):
        mute_value=os.popen('adb shell "cat /sys/class/gpio/gpio42/value"').read()
        if (int(mute_value) == 1):
            self.development_menu_list[2]="Mute"
        else:
            self.development_menu_list[2]="UnMute"
        for i in range(len(self.development_menu_list)):
            print("\t%d. %s"%(i+1,self.development_menu_list[i]))

    def get_num(self):
        menuNum=input("Enter Number:")
        if (len(menuNum)==0 or len(menuNum)>1):
            self.input=0
        else:
            if ((int(menuNum)-1) < len(self.development_menu_list)):
                self.input=int(menuNum)
            else:
                self.input=0

    def __gpio_configuration(self):
        gpio_num=input("Enter GPIO Num:")
        gpio_direction=input("Enter GPIO Direction:")
        gpio_value=input("Enter GPIO Value:")
        gpio_str=('adb shell "echo %s > /sys/class/gpio/export"')%gpio_num
        os.system(gpio_str)
        gpio_str=('adb shell "echo %s > /sys/class/gpio/gpio%s/direction"')%(gpio_direction,gpio_num)
        os.system(gpio_str)
        gpio_str=('adb shell "echo %s > /sys/class/gpio/gpio%s/value"')%(gpio_value,gpio_num)
        os.system(gpio_str)
        gpio_str=('adb shell "echo %s > /sys/class/gpio/unexport"')%gpio_num
        os.system(gpio_str)

    def __mute(self):
        mute_value=os.popen('adb shell "cat /sys/class/gpio/gpio42/value"').read()
        if (int(mute_value) == 1):
            os.system('adb shell "echo 0 > /sys/class/gpio/gpio42/value"')
        else:
            os.system('adb shell "echo 1 > /sys/class/gpio/gpio42/value"')

    def run(self):
        while True:
            print("\tDevelopment\n")
            self.display()
            self.get_num()
            if (self.input is 0):
                continue
            elif (self.input is 1):
                threading.Thread(target=base.monitor).start()
            elif (self.input is 2):
                self.__gpio_configuration()
            elif (self.input is 3):
                self.__mute()
            elif (self.input is 4):
                break
            else:
                print("error")


