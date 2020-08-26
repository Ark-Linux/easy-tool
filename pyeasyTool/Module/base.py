import subprocess
import os
import platform
from time import sleep

class Base:
    def __init__(self,array):
        self.array=array
    def display(self):
        for i in range(len(self.array)):
            print("\t%d. %s"%(i+1,self.array[i]))
    def get_num(self):
        menu_num=input("Enter Number:")
        if (len(menu_num) == 0):
            self.input=0
        else:
            if ((int(menu_num)-1) < len(self.array)):
                self.input=int(menu_num)
            else:
                self.input=0

def __env_check():
    if platform.system() == 'Windows':
        return True
    else:
        return False

def get_device_num():
    command_info=os.popen('adb devices').read()
    device_num=command_info.split("\t")[0].split("\n")[1]
    return device_num

def monitor():
    if __env_check():
        subprocess.call('adb shell "adk-message-monitor -a"', creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        os.popen('''gnome-terminal -x adb shell "adk-message-monitor -a"''')

def is_exist():
    while True:
        device_num=get_device_num()
        if (len(device_num)==0):
            os._exit(0)
        sleep(1)
