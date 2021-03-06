import base
import os
from time import sleep
import threading

class Wifi(base.Base):
    wifi_menu_array="Connect WiFi",\
                "Change Country",\
                "Scan WiFi List",\
                "Refresh Connection",\
                "Wifi Message",\
                "Wifi Name Change",\
                "Back"

    wifi_name=" "

    def is_wifi_stable(self):
        while True:
            wlan_info=os.popen('adb shell ifconfig').read()
            if (wlan_info.split('\n\n')[18].split(' ')[0]=="wlan0" and len(wlan_info.split('\n\n')[19].split("Bcast"))>1):
                print("\twifi is stable")
                os.system('''adb shell "adk-message-send 'connectivity_wifi_completeonboarding{}'"''')
                print("\tEnter to Continue")
                exit(0)
            sleep(1)

    def wifi_connect(self):
        wifissid=input("\nEnter ssid:")
        wifipassw=input("Enter Password:")
        os.system('''adb shell "adk-message-send 'connectivity_wifi_onboard{}'"''')
        sleep(1)
        wifi_msg_str=('''adb shell "adk-message-send 'connectivity_wifi_connect {ssid:\\"%s\\" password: \\"%s\\" homeap:true}'"''')\
                    %(wifissid,wifipassw)
        os.system(wifi_msg_str)
        sleep(2)
        threading.Thread(target=self.is_wifi_stable).start()

    def __wifi_country_change(self):
        nation_name=os.popen('adb shell adkcfg -f /data/adk.connectivity.wifi.db read connectivity.wifi.onboard_ap_country_code').read()
        print("\tCurrent Nation Name: "+nation_name)
        nation_name=input("Enter Nation Name:")
        os.system('''adb shell "adk-message-send 'connectivity_wifi_onboard{}'"''')
        sleep(1)
        wifi_msg_str=('adb shell adkcfg -f /data/adk.connectivity.wifi.db write connectivity.wifi.onboard_ap_country_code %s --ignore')\
                      %nation_name
        os.system(wifi_msg_str)
        sleep(1)
        os.system('''adb shell "adk-message-send 'connectivity_wifi_onboard{}'"''')

    def __wifi_scan(self):
        threading.Thread(target=base.monitor).start()
        os.system('''adb shell "adk-message-send 'connectivity_wifi_scan{}'"''')

    def __wifi_name_refresh(self):
        wifi_comd_str='''adb shell "cat /etc/misc/wifi/wpa_supplicant.conf | grep -w 'ssid'"'''
        wifi_ssid=os.popen(wifi_comd_str).read()
        if (len(wifi_ssid.split('"')) > 1):
            self.wifi_name=wifi_ssid.split('"')[1]

    def wifi_message(self):
        wifi_message=os.popen('adb shell wpa_cli status').read()
        print("\tCurrent Nation Name: "+wifi_message)

    def wifi_name_change(self):
        wifi_name=os.popen('adb shell adkcfg -f /data/adk.connectivity.wifi.db read connectivity.wifi.onboard_ap_ssid_prefix').read()
        print("\tCurrent wifi Name: "+wifi_name)
        wifi_name=input("Enter wifi Name:")
        os.system('''adb shell "adk-message-send 'connectivity_wifi_onboard{}'"''')
        sleep(1)
        wifi_msg_str=('adb shell adkcfg -f /data/adk.connectivity.wifi.db write connectivity.wifi.onboard_ap_ssid_prefix %s --ignore')\
                      %wifi_name
        os.system(wifi_msg_str)
        sleep(1)
        os.system('''adb shell "adk-message-send 'connectivity_wifi_onboard{}'"''')

    def run(self):
        while True:
            self.__wifi_name_refresh()
            print("\tWiFi Connection")
            print("\tConnecting: "+str(self.wifi_name))
            self.display()
            self.get_num()
            if (self.input is 0):
                continue
            elif (self.input is 1):
                self.wifi_connect()
            elif (self.input is 2):
                self.__wifi_country_change()
            elif (self.input is 3):
                self.__wifi_scan()
            elif (self.input is 4):
                continue
            elif (self.input is 5):
                self.wifi_message()
            elif (self.input is 6):
                self.wifi_name_change()
            elif (self.input is 7):
                break
            else:
                print("error")
