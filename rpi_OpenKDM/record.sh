#!/bin/sh

echo 'Started data recording window...'

# python3 record_data.py &
# sleep 10
# PID=$!
# kill $PID


# PID=$
# echo "killing $PID"
# kill -9 $(ps aux | grep -v grep | grep "record_data.py" | awk '{print $2}')


yad --form --title "OpenKDM" --window-icon=128.png --width=300 --height=300 --center \
	--text="Start data recording the sensor data." \
 	--field="Start recording":fbtn "python3 record_data.py &" \
	--field="Stop recording":fbtn "bash kill.sh" \
	--button=gtk-cancel:1
