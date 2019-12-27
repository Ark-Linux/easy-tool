import base
import main_menu
from time import sleep
import threading
import os

def is_exist():
    while True:
        device_num=base.get_device_num()
        if (len(device_num)==0):
            os._exit(0)
        sleep(1)

if __name__ == '__main__':
    device_num=base.get_device_num()
    if (len(device_num)==0):
        print("\ndevices not exist, re-plug USB or reboot please")
    else:
        threading.Thread(target=is_exist).start()
        main_menu.MainMenu(main_menu.MainMenu.menu_array).run()

