#! /bin/bash

readonly process_array=("bt.sh"\
			"alexa.sh"\
			"development.sh"\
			"led.sh"\
			"wifi.sh"\
			"is_wifi_stable.sh")

function processKill () {
	pid=`ps -ef | grep -w $1 | grep -v "grep" | awk '{print $2}'`
	kill -9 $pid
}

function processExist () {
	pid=`ps -ef | grep -w $1 | grep -v "grep" | awk '{print $2}'`
	if [[ -n ${pid} ]]
	then
		processKill $1 ;
	fi
}

while : 
do
	is_exist=`adb devices | grep -w "device"`
        if [[ -z ${is_exist} ]]
        then
		processKill easyTool.sh ;
		for ((i=0; i<${#process_array[*]}; i++))
		do
			processExist ${process_array[$i]} ;
		done
		processKill is_exist.sh ;
	else
		pid=`ps -ef | grep -w "easyTool.sh" | grep -v "grep" | awk '{print $2}'`
		if [[ -z ${pid} ]]
		then
			for ((i=0; i<${#process_array[*]}; i++))
			do
				processExist ${process_array[$i]} ;
			done
			processKill is_exist.sh ;
		fi
        fi
	sleep 1s
done
