#! /bin/bash

readonly alexa_menu_array=("Alexa Onboard" "alexa_onboard"\
			"Alexa Quit" "alexa_quit"\
			"Back" "break")

function alexa_onboard () {
	gnome-terminal -x adb shell "adk-message-monitor -a"
	sleep 1
	gnome-terminal -x adb shell "adk-message-send 'voiceui_start_onboarding{client:\"AVS\"}'"
}

function alexa_quit () {
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
