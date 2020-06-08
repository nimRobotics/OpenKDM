#!/bin/sh

echo 'Started speed setting window...'

n=4

ANSWER=`yad --title "OpenKDM" --window-icon=128.png --width=300 --height=300 --center \
	--text="Please set the motor speed for experiment." \
	--form --separator=' ' --field="Motor speed (rpm):NUM" 1\!1..8\!1\!0 `

exval=$?
# echo $exval
case $exval in
   0) 
	echo '[1/'$n'] Updating motor speed (rpm)...'
	sed "/int speed_rpm/c\int speed_rpm=$ANSWER;" speed_control/speed_control.ino -i

	echo '[2/'$n'] Compiling arduino sketch...'
	arduino-cli compile --fqbn arduino:avr:uno /home/pi/Desktop/OpenKDM/speed_control/

	echo '[3/'$n'] Uploading arduino sketch (uno)...'
	arduino-cli upload --port /dev/ttyACM0 --fqbn arduino:avr:uno /home/pi/Desktop/OpenKDM/speed_control/
	echo '[4/'$n'] Process finshed. Check traceback for errors...'
	;;
   *) echo "Motor speed not updated...";;
esac




# sed '/int speed_rpm/c\int speed_rpm=4;' speed_control/speed_control.ino -i

# echo '[2/'$n'] Compiling arduino sketch...'
# arduino-cli compile --fqbn arduino:avr:uno /home/pi/Desktop/OpenKDM/speed_control/

# echo '[1/'$n'] Uploading arduino sketch (uno)...'
# arduino-cli upload --port /dev/ttyACM0 --fqbn arduino:avr:uno /home/pi/Desktop/OpenKDM/speed_control/
