import sys
sys.path.append('./Module')
import base
import main_menu
import threading



if __name__ == '__main__':
    device_num=base.get_device_num()
    if (len(device_num)==0):
        print("\ndevices not exist, re-plug USB or reboot please")
    else:
        threading.Thread(target=base.is_exist).start()
        main_menu.MainMenu(main_menu.MainMenu.menu_array).run()

