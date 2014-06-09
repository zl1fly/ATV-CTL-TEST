#Imports the serial lib's
import serial

#Import the string handling lib's
import string

# Port and speed settings
port = "/dev/ttyACM0"

# Set up the serial port 9600 (8N1=Default)
ser = serial.Serial(port,9600)

#Initialise variables.
complete_string = ""
humidity = 0
temp = 0

#function to split the string and work out which value to update
def process_string(string_to_process):
  words = string.split(string_to_process)
  #print(words[0]+"\n")
  #print(words[1]+"\n")
  what = words[0]
  parameter = words[1]
  if what == "a:":
    humidity = parameter
  if what == "b:":
    temp = parameter   
  return

def write_to_db()
    print("Humidity = "+humidity+"%")
    print("Temperature = "+temp+"C")

# Enter a while true loop
while 1:
    # Read from the serial port
    value = ser.read()

    #Check to see if the character read from the serial port is a newline
    #If it is a line feed then call process the string function
    if value == "\n":
      #Process the string
      process_string(complete_string)
      complete_string = ""
      write_to_db()
    #Otherwise concatenate the string
    else:
      complete_string = complete_string + value
