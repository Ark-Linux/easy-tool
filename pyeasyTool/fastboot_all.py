#! /usr/bin/python
# -*- coding: UTF-8 -*-

import os
import platform
import subprocess

class FastbootImage:
    __current_dir = "./" #os.getcwd()
    __packge_name = "release_pkg"
    __system_environment = "Linux"
    __image_table = (('xbl.elf', 'xbl_a'),               ('pmic.elf', 'pmic_a'),                 ('logfs_ufs_8mb.bin', 'logfs'),\
                     ('BTFM.bin', 'bluetooth_a'),        ('NON-HLOS.bin', 'modem_a'),            ('dspso.bin', 'dsp_a'),\
                     ('rpm.mbn', 'rpm_a'),               ('cmnlib.mbn', 'cmnlib_a'),             ('cmnlib64.mbn', 'cmnlib64_a'),\
                     ('devcfg.mbn', 'devcfg_a'),         ('keymaster64.mbn', 'keymaster_a'),     ('tz.mbn', 'tz_a'),\
                     ('uefi_sec.mbn', 'uefisecapp_a'),   ('storsec.mbn', 'storsec'),             ('abl.elf', 'abl_a'),\
                     ('boot.img', 'boot_a'),             ('persist.img', 'persist'),             ('system.img', 'system_a'),\
                     ('systemrw.img', 'systemrw'),       ('cache.img', 'cache'),                 ('usrdata.img', 'userdata') )
 
    def __check_image(self):
        print("check image")
        check_result = True
        for image in self.__image_table:
            image_file = self.__current_dir + self.__packge_name + "/" + image[0]
            if os.path.exists(image_file) == False:
                print("Fail: The image is not exist:",image)
                check_result = False
        return check_result
    
    def __find_devices(self):
        device_info = []
        find_result = True
        print("find evices")
        devices_list = os.popen('adb devices').readlines()
        for i in range(len(devices_list)):
            if devices_list[i].find('\tdevice') != -1:
                device_info.append(devices_list[i].split('\t')[0])
        if len(device_info) <= 0:
            find_result = False
        else:
            print("Find devices ID:", device_info)
        return find_result

    def __check_environment(self):
        check_result = True
        if platform.system() == 'Linux':
            self.__system_environment = 'Linux'
        elif platform.system() == 'Windows':
            self.__system_environment = 'Windows'
        else:
            check_result = False
        return check_result

    def __into_fastboot_mode(self):
        os.popen('adb reboot bootloader')
        if self.__system_environment == 'Windows':
            os.popen('fastboot.exe devices')
        elif self.__system_environment == 'Linux':
            os.popen("sudo fastboot devices")

    def __fastboot_process(self):
        platform_comment = ""
        if self.__system_environment == 'Windows':
            platform_comment = "fastboot.exe "
        elif self.__system_environment == 'Linux':
            platform_comment = "sudo fastboot " 
        for image in self.__image_table:
            print("downloading image:",image[0])
            fastboot_comment = platform_comment + 'flash ' + image[1] + ' ./' + self.__packge_name + '/' + image[0]
            os.popen(fastboot_comment)
        print("system reboot")
        fastboot_comment = platform_comment + "reboot"
        os.popen(fastboot_comment)

    def run(self):
        if self.__check_image() == True:
            if self.__find_devices() == True: 
                if self.__check_environment() == True:
                    self.__into_fastboot_mode()
                    self.__fastboot_process()
                else:
                    print("Fail: The script does not support the current system!")
            else:
                print("Fail: No find devices!")
        else:
            print("Fail: Some image don't exist!")
    
# fastboot_image = FastbootImage()
# fastboot_image.run()




