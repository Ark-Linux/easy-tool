import base
import os
import random

class BtAddress(base.Base):
    addr_array=("70:c9:4e:b7:f6:54",\
			    "70:c9:4e:7f:63:7a",\
			    "70:c9:4e:5b:b3:fe",\
			    "70:c9:4e:5b:b9:4e",\
			    "70:c9:4e:7f:6d:0e")

    def bt_solid_address(self):
        print("\tAddress Modify\n")
        for i in range(0,len(BtAddress.addr_array),1):
            print("\t%d. %s"%(i+1,BtAddress.addr_array[i]))
        menuNum=eval(input("Enter Number:"))
        if ((menuNum-1) < len(BtAddress.addr_array)):
            self.input=menuNum
            bt_msg_str=("adb shell setprop persist.vendor.service.bdroid.bdaddr "+BtAddress.addr_array[self.input-1])
            os.system(bt_msg_str)
            getaddr=os.popen('adb shell getprop persist.vendor.service.bdroid.bdaddr').read()
            print("\tSetting Success")
            print("\tCurrent BT ADDR: "+getaddr)
        else:
            print("Error")

    def __bt_random_address(self):
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
            if (self.input is 0):
                continue
            elif (self.input is 1):
                self.__bt_solid_address()
            elif (self.input is 2):
                self.__bt_random_address()
            elif (self.input is 3):
                break
            else:
                print("error")

class Bt(base.Base):
    bt_menu_array="BT Name Modify",\
                "BT Address Modify",\
			    "Back"

    bt_address_modify_menu_array=("Default Address",\
                                "Random Address",\
				                "Back")

    def __bt_name_modify(self):
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
            if (self.input is 0):
                continue
            elif (self.input is 1):
                self.__bt_name_modify()
            elif (self.input is 2):
                BtAddress(Bt.bt_address_modify_menu_array).run()
            elif (self.input is 3):
                break
            else:
                print("error")
