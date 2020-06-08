[ -f yad_data.list ] && rm yad_data.list

while IFS=, read -r field1 field2
do
    echo $field1 >> yad_data.list
    echo $field2 >> yad_data.list

done < sensor_data.csv

yad --height=300 --list --column=Angle --column=Acceleration < yad_data.list
