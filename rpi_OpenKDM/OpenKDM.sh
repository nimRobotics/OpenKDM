#!/bin/sh

echo 'Launched OpenKDM...'

yad --form --title "OpenKDM" --window-icon=128.png --width=300 --height=300 --center \
	--text="Welcome! choose an option to begin with." \
 	--field="Set Motor Speed":fbtn "bash speed.sh" \
	--field="Record Data":fbtn "bash record.sh" \
	--field="Retrive Data":fbtn "bash retrive.sh" \
	--button=gtk-cancel:1
