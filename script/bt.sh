#! /bin/bash

readonly bt_menu_array=(
			#"BT Enable" bt_enable\
			#"BT Disable" bt_disable\
			#"BT Discoverable" bt_enter_discoverable\
			#"BT Undiscoverable" bt_exit_discoverable\
			#"BT Connect" bt_connect\
			#"BT Disconnect" bt_disconnect\
			#"BT Reconnect" bt_reconnect\
			"BT Name Modify" bt_name\
			"BT Address Modify" bt_address_modify\
			#"BT Track Play Pause Toggle" bt_track_play_pause_toggle\
			#"BT Track Previous" bt_track_previous\
			#"BT Track Next"	bt_track_next\
			"Back" break)

readonly bt_address_modify_menu_array=("Default Address" "bt_solid_address"\
				       "Random Address" "bt_random_address"\
				       "Back" "break")

readonly addr_array=("70:c9:4e:b7:f6:54"\
			"70:c9:4e:7f:63:7a"\
			"70:c9:4e:5b:b3:fe"\
			"70:c9:4e:5b:b9:4e"\
			"70:c9:4e:7f:6d:0e")

function bt_enable () {
	clear
	gnome-terminal -x adb shell "adk-message-send 'connectivity_bt_enable {}'"
	echo "		Enable Success"
	read -p "Any Key to Continue" p
	clear
}

function bt_disable () {
	clear
	gnome-terminal -x adb shell "adk-message-send 'connectivity_bt_disable {}'"
	echo "		Disable Success"
	read -p "Any Key to Continue" p
	clear
}

function bt_enter_discoverable () {
	clear
	read -p "	Input Discoverable Timeout:(seconds)" timeout
	gnome-terminal -x adb shell "adk-message-send 'connectivity_bt_setdiscoverable {timeout : $timeout }'"
	echo "		Enter Discoverable Success, Setting Timeout: $timeout seconds"
	read -p "Any Key to Continue" p
	clear
}

function bt_exit_discoverable () {
	clear
	gnome-terminal -x adb shell "adk-message-send 'connectivity_bt_exitdiscoverable {}'"
	echo "		Exit Discoverable Success"
	read -p "Any Key to Continue" p
	clear
}

function bt_connect () {
	gnome-terminal -x adb shell "adk-message-send 'connectivity_bt_connect {}'"
}

function bt_disconnect () {
	clear
	gnome-terminal -x adb shell "adk-message-send 'connectivity_bt_disconnect {}'"
	echo "		Disconnect Success"
	read -p "Any Key to Continue" p
	clear
}

function bt_reconnect () {
	clear
	gnome-terminal -x adb shell "adk-message-send 'connectivity_bt_connect {}'"
	echo "		Reconnecting"
	read -p "Any Key to Continue" p
	clear
}

function bt_random_address () {
	clear
	echo "          Address Modify"
	echo ""
	bt_address_str="70:c9:4e:66"
	for((i=0; i<2; i++))
	do
		bt_address_str+=":`openssl rand -hex 1`"
	done
	adb shell setprop persist.vendor.service.bdroid.bdaddr $bt_address_str
	echo "Setting Success"
	getaddr=`adb shell getprop persist.vendor.service.bdroid.bdaddr`
	echo "Current BT ADDR: ${getaddr}"
	read -p "Any Key to Continue" p
	clear
}

function bt_solid_address () {
	clear
	echo "          Address Modify"
	echo ""
	for ((i=0; i<${#addr_array[*]}; i++))
	do
		echo "$[$i+1]  ADDR$[$i+1] : ${addr_array[${i}]}"
	done
	read -p "Enter Number:" btAddr
	if [ $[${btAddr}-1] -lt ${#addr_array[*]} ]
	then
		adb shell setprop persist.vendor.service.bdroid.bdaddr ${addr_array[$[${btAddr}-1]]}
	else
		echo "Enter Error"
	fi
	echo "Setting Success"
	getaddr=`adb shell getprop persist.vendor.service.bdroid.bdaddr`
	echo "Current BT ADDR: ${getaddr}"
	read -p "Any Key to Continue" p
	clear
}

function bt_address_modify () {
	clear
	echo "          Address Modify"
	echo ""
	for ((i=0; i<$[${#bt_address_modify_menu_array[*]}/2]; i++))
	do
		echo "      $[$i+1]. ${bt_address_modify_menu_array[$[$i*2]]}"
	done
	echo ""
	read -p "Enter Number:" menuNum
	if [ $[${menuNum}-1] -lt $[ ${#bt_address_modify_menu_array[*]}/2 ] ]
	then
		${bt_address_modify_menu_array[$[$[$menuNum-1]*2 +1]]}
	else
		echo "Enter Error"
	fi
	
}

function bt_name () {
	clear
	echo "          Name Modify"
	read -p "Enter New BT Name:" btName
	if [[ -n $btName ]];then
		gnome-terminal -x adb shell "adk-message-send 'connectivity_bt_setname {name:\"$btName\"}'"
	fi
	read -p "Any Key to Continue" p
	clear
}

function bt_track_play_pause_toggle () {
	gnome-terminal -x adb shell "adk-message-send 'audio_track_play_pause_toggle {}'"
}

function bt_track_previous () {
	gnome-terminal -x adb shell "adk-message-send 'audio_track_previous {}'"
}

function bt_track_next () {
	gnome-terminal -x adb shell "adk-message-send 'audio_track_next {}'"
}

function bt_menu () {
	while :
	do
		echo "          BT Menu"
		echo ""
		currBTName=`adb shell adkcfg -f /data/adk.connectivity.bt.db read connectivity.bt.device_name`
		getaddr=`adb shell getprop persist.vendor.service.bdroid.bdaddr`
		echo "   Current BT Name: $currBTName"
		echo "   Current BT Adddress: $getaddr"
		echo ""
		for ((i=0; i<$[${#bt_menu_array[*]}/2]; i++))
		do
			echo "      $[$i+1]. ${bt_menu_array[$[$i*2]]}"
		done
		echo ""
		read -p "Enter Number:" menuNum
		if [ $[${menuNum}-1] -lt $[ ${#bt_menu_array[*]}/2 ] ]
		then
			${bt_menu_array[$[$[$menuNum-1]*2 +1]]}
		else
			echo "Enter Error"
		fi
	done
}

if [[ -z ${1} ]];then
	bt_menu
else
	adb shell setprop persist.vendor.service.bdroid.bdaddr ${addr_array[$[${1}-1]]}
fi
