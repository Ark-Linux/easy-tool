#! /bin/bash

readonly alexa_menu_array=("Alexa Onestep Onboard" "alexa_onestep_onboard"\
			"Alexa Activate" "alexa_activate"\
			"Alexa InActivate" "alexa_inactivate"\
			"Back" "break")

function monitor () {
	while :
	do
		pid=`ps -ef | grep -w "is_wifi_stable.sh" | grep -v "grep" | awk '{print $2}'`
		if [[ -z ${pid} ]];then
			return 1;
		fi
		sleep 3
	done
}

function alexa_onestep_onboard () {
	./script/bt.sh 2
	sleep 1
	./script/wifi.sh 1
	sleep 1
	monitor
	read -p "Any key to Continue when AVSLED flash GREEN twice" p
	gnome-terminal -x adb shell "adk-message-monitor -a"
	sleep 1
	gnome-terminal -x adb shell "adk-message-send 'voiceui_start_onboarding{client:\"AVS\"}'"
}

function alexa_activate () {
	gnome-terminal -x adb shell "adk-message-monitor -a"
	sleep 1
	gnome-terminal -x adb shell "adk-message-send 'voiceui_start_onboarding{client:\"AVS\"}'"
}

function alexa_inactivate () {
	gnome-terminal -x adb shell "adk-message-monitor -a"
	sleep 1
	gnome-terminal -x adb shell "adk-message-send 'voiceui_delete_credential {client:\"AVS\"}'"
	sleep 1
	gnome-terminal -x adb shell "systemctl restart voiceUI"
}

function alexa_menu () {
	while :
	do
		clear
		echo "      Alexa"
		echo ""
		for ((i=0; i<$[${#alexa_menu_array[*]}/2]; i++))
		do
			echo "      $[$i+1]. ${alexa_menu_array[$[${i}*2]]}"
		done
		echo ""
		read -p "Enter Number:" alexaNum
		if [ $[${alexaNum}-1] -lt $[${#alexa_menu_array[*]}/2] ]
                then
			clear
			${alexa_menu_array[$[$[$alexaNum-1]*2+1]]}
                else
                        echo "Enter Error"
                fi
	done
}

alexa_menu
