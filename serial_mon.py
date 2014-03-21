#Imports the serial lib's
import serial

# Port and speed settings
port = "/dev/AMA0"

# Set up the serial port 9600 (8N1=Default)
ser = serial.Serial(port,9600)

# Enter a while true loop
while 1:
    # Read from the serial port
    value = ser.read()
    # prints what it has read from the serial port
    print value
    # Prints a seperater line so I can see what it defines as a seperater 
    # I think it read the carrage return as a seperater.
    print("---------\n")    