import serial
import csv
import os

if os.path.exists("sensor_data.csv"):
  os.remove("sensor_data.csv")

ser = serial.Serial('/dev/ttyACM0',9600)

while True:
	read_serial=ser.readline()
	data = str(read_serial)
	try:
		# data = data.strip("\'")
		# data = data.strip("b'")
		data = data.split("'")[1]
		data = data.strip('\\r\\n')
		num1, num2 = data.split(" ")
		print(float(num1), float(num2))
		with open('sensor_data.csv', mode='a') as label_file:
			label_writer = csv.writer(label_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			label_writer.writerow([float(num1), float(num2)])
	except:
		print("Data not parsed!")

	
