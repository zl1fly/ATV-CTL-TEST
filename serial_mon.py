#Imports the serial lib's
import serial
import string

# Port and speed settings
port = "/dev/ttyACM0"

# Set up the serial port 9600 (8N1=Default)
ser = serial.Serial(port,9600)
complete_string = ""

def process_string(string_to_process):
  print(string_to_process)
  words = string.split(string_to_process)
  #print(words[0]+"\n")
  #print(words[1]+"\n")
  return


# Enter a while true loop
while 1:
    # Read from the serial port
    value = ser.read()

    if value == "\n":
      process_string(complete_string)
      complete_string = ""
    else:
      complete_string = complete_string + value
