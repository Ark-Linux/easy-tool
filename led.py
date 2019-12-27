import base
import os
import sqlite3

class Led(base.Base):
    led_menu_array=("Set Normal Pattern",\
               "Set Indicate Pattern",\
               "Set Reverse Pattern",\
               "Back")

    def list_pattern(self):
        num=0
        list=[]
        os.system('adb pull /data/adk.led.db .')
        conn=sqlite3.connect('./adk.led.db')
        database=conn.cursor()

        while True:
            sql_str=("select * from config_table where key='ui.led.pattern.%d.type';")%num
            database.execute(sql_str)
            info=database.fetchall()
            if (len(info) == 0):
                 break
            list.append(info)
            num=num+1
        self.pattern_list=list
        self.num=num
        database.close()

    def set_normal_pattern(self):
        num_list=[]
        for i in range(self.num):
            if (self.pattern_list.__getitem__(i).__getitem__(0)[1]=="trail"\
            or self.pattern_list.__getitem__(i).__getitem__(0)[1]=="pulse"\
            or self.pattern_list.__getitem__(i).__getitem__(0)[1]=="basic"):
                print("Enter Pattern Number "+str(i)+" to Set * "+self.pattern_list.__getitem__(i).__getitem__(0)[1]+" * Pattern")
                num_list.append(i)

        pattern_num=eval(input("\nEnter Pattern Number:"))
        if (pattern_num in num_list):
            led_msg_str=('''adb shell "adk-message-send 'led_start_pattern{pattern:%d}'"''')%pattern_num
            os.system(led_msg_str)
        else:
            print("Enter Error")

    def set_indicate_pattern(self):
        num_list=[]
        for i in range(self.num):
            if (self.pattern_list.__getitem__(i).__getitem__(0)[1]=="direction"):
                print("Enter Pattern Number "+str(i)+" to Set * "+self.pattern_list.__getitem__(i).__getitem__(0)[1]+" * Pattern")
                num_list.append(i)

        pattern_num=eval(input("\nEnter Pattern Number:"))
        if (pattern_num in num_list):
            led_msg_str=('''adb shell "adk-message-send 'led_indicate_direction_pattern{pattern:%d direction:0}'"''')%pattern_num
            os.system(led_msg_str)
        else:
            print("Enter Error")

    def set_reverse_pattern(self):
        num_list=[]
        for i in range(self.num):
            if (self.pattern_list.__getitem__(i).__getitem__(0)[1]=="reverse"):
                print("Enter Pattern Number "+str(i)+" to Set * "+self.pattern_list.__getitem__(i).__getitem__(0)[1]+" * Pattern")
                num_list.append(i)

        pattern_num=eval(input("\nEnter Pattern Number:"))
        if (pattern_num in num_list):
            led_msg_str=('''adb shell "adk-message-send 'led_reverse_direction_pattern{pattern:%d direction:0}'"''')%pattern_num
            os.system(led_msg_str)
        else:
            print("Enter Error")


    def run(self):
        while True:
            print("\tSet LED Pattern\n")
            self.display()
            self.get_num()
            self.list_pattern()
            if (self.input is 0):
                continue
            elif (self.input is 1):
                self.set_normal_pattern()
            elif (self.input is 2):
                self.set_indicate_pattern()
            elif (self.input is 3):
                self.set_reverse_pattern()
            elif (self.input is 4):
                break
            else:
                print("error")
