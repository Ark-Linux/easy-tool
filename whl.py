# -*- coding: utf-8 -*-
import easyTool
import os
import time
import random
import subprocess
import threading

wifi_menu_array="Connect WiFi",\
                "Change Country",\
                "Scan WiFi List",\
                "Refresh Connection",\
                "Back"

addr_array="70:c9:4e:b7:f6:54",\
			"70:c9:4e:7f:63:7a",\
			"70:c9:4e:5b:b3:fe",\
			"70:c9:4e:5b:b9:4e",\
			"70:c9:4e:7f:6d:0e"

bt_menu_array="BT Name Modify",\
                "BT Address Modify",\
			    "Back"

bt_address_modify_menu_array="Default Address",\
                            "Random Address",\
				            "Back"

class Wifi(easyTool.Base):
    wifi_name=" "
    def wifi_connect(self):
        wifissid=input("Enter ssid:")
        wifipassw=input("Enter Password:")
        os.system('''adb shell "adk-message-send 'connectivity_wifi_onboard{}'"''')
        time.sleep(1)
        wifi_msg_str=('''adb shell "adk-message-send 'connectivity_wifi_connect {ssid:\\"%s\\" password: \\"%s\\" homeap:true}'"''')\
                    %(wifissid,wifipassw)
        os.system(wifi_msg_str)

    def wifi_country_change(self):
        nation_name=os.popen('''adb shell adkcfg -f /data/adk.connectivity.wifi.db read connectivity.wifi.onboard_ap_country_code''').read()
        print("\tCurrent Nation Name: "+nation_name)
        nation_name=input("Enter Nation Name:")
        os.system('''adb shell "adk-message-send 'connectivity_wifi_onboard{}'"''')
        time.sleep(1)
        wifi_msg_str=('adb shell adkcfg -f /data/adk.connectivity.wifi.db write connectivity.wifi.onboard_ap_country_code %s --ignore')\
                    %nation_name
        os.system(wifi_msg_str)
        time.sleep(1)
        os.system('adb reboot')

    def wifi_scan(self):
        os.system('adb shell "adk-message-monitor -a"')
        os.system('''adb shell "adk-message-send 'connectivity_wifi_scan{}'"''')

    def wifi_name_refresh(self):
        wifi_comd_str='''adb shell "cat /etc/misc/wifi/wpa_supplicant.conf | grep -w 'ssid'"'''
        wifi_ssid=os.popen(wifi_comd_str).read()
        self.wifi_name=wifi_ssid.split('"')[1]

    def run(self):
        while True:
            self.wifi_name_refresh()
            print("\tWiFi Connection")
            print("\tConnecting: "+self.wifi_name)
            self.display()
            self.get_num()
            if (self.input is 1):
                self.wifi_connect()
            elif (self.input is 2):
                self.wifi_country_change()
            elif (self.input is 3):
                self.wifi_scan()
            elif (self.input is 4):
                continue
            elif (self.input is 5):
                break
            else:
                print("error")

class Btaddress(easyTool.Base):
    def bt_solid_address(self):
        print("\tAddress Modify\n")
        for i in range(0,len(addr_array),1):
            print("\t%d. %s"%(i+1,addr_array[i]))
        menuNum=eval(input("Enter Number:"))
        if ((menuNum-1) < len(addr_array)):
            self.input=menuNum
            bt_msg_str=("adb shell setprop persist.vendor.service.bdroid.bdaddr "+addr_array[self.input-1])
            os.system(bt_msg_str)
            getaddr=os.popen('adb shell getprop persist.vendor.service.bdroid.bdaddr').read()
            print("\tSetting Success")
            print("\tCurrent BT ADDR: "+getaddr)
        else:
            print("Error")

    def bt_random_address(self):
        print("\tAddress Modify\n")
        get_old_addr=os.popen('adb shell getprop persist.vendor.service.bdroid.bdaddr').read()
        bt_address_str=("70:c9:4e:"+hex(random.randint(91,183)).split('x')[1])
        for i in range(2):
            bt_address_str+=":"+"".join([random.choice("0123456789abcdef") for i in range(2)])
        bt_msg_str=("adb shell setprop persist.vendor.service.bdroid.bdaddr "+bt_address_str)
        os.system(bt_msg_str)
        get_new_addr=os.popen('adb shell getprop persist.vendor.service.bdroid.bdaddr').read()
        if (get_old_addr is not get_new_addr):
            print("\tSetting Success")
            print("\tCurrent BT ADDR: "+get_new_addr)

    def run(self):
        while True:
            print("\tAddress Modify\n")
            self.display()
            self.get_num()
            if (self.input is 1):
                self.bt_solid_address()
            elif (self.input is 2):
                self.bt_random_address()
            elif (self.input is 3):
                break
            else:
                print("error")

class Bt(easyTool.Base):
    def bt_name_modify(self):
        print("\tName Modify\n")
        bt_name=input("Enter New BT Name:")
        if (len(bt_name)!=0):
            bt_msg_str=('''adb shell "adk-message-send 'connectivity_bt_setname {name:\\"%s\\"}'"''')%bt_name
            os.system(bt_msg_str)

    def run(self):
        while True:
            print("\tBT Menu\n")
            currBTName=os.popen('adb shell adkcfg -f /data/adk.connectivity.bt.db read connectivity.bt.device_name').read()
            getaddr=os.popen('adb shell getprop persist.vendor.service.bdroid.bdaddr').read()
            print("\tCurrent BT Name:"+currBTName.split('\n')[0])
            print("\tCurrent BT Adddress:"+getaddr.split('\n')[0])
            self.display()
            self.get_num()
            if (self.input is 1):
                self.bt_name_modify()
            elif (self.input is 2):
                btaddrMenu=Btaddress(bt_address_modify_menu_array)
                btaddrMenu.run()
            elif (self.input is 3):
                break
            else:
                print("error")

class Alexa:
    def alexa_onboard(self):
        #alexa_msg_str='''adb shell "adk-message-send 'voiceui_start_onboarding{client:\"AVS\"}'"'''
        #subprocess.call('adb shell "adk-message-monitor -a"', creationflags=subprocess.CREATE_NEW_CONSOLE)
        #os.system('adb shell "adk-message-monitor -a"')
        while True:
            print("Thread")
            time.sleep(1)

    def run(self):
        t=threading.Thread(target=self.alexa_onboard())
        t.start()

        #subprocess.call('''adb shell "adk-message-send 'voiceui_start_onboarding{client:\"AVS\"}'"''', creationflags=subprocess.CREATE_NEW_CONSOLE)
        print("main")
