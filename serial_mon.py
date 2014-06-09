#Imports the serial lib's
import serial

#Import the string handling lib's
import string

# Port and speed settings
port = "/dev/ttyACM0"

#Initialise variables.
complete_string = ""
humidity = 0
temp = 0
dbupdate = 0

# Set up the serial port 9600 (8N1=Default)
ser = serial.Serial(port,9600)

#function to split the string and work out which value to update
def process_string(string_to_process):
  words = string.split(string_to_process)
  #use the global values
  global humidity
  global temp
  
  #check to see if we are getting what we want otherwise it will crash
  if words[0] == "a:":
    #if the value has changed since the last time update the global value
    if humidity != float(words[1]):
        humidity = float(words[1])
  
  if words[0] == "b:":    
    #if the value has changed since the last time update the global value
    if temp != float(words[1]):
        temp = float(words[1])
  
  return

def write_to_db():
    global dbupdate
    # Add one to the counter
    dbupdate = dbupdate + 1
    # If we hit 6 iterations 3(seconds +-) then print values
    if dbupdate == 6:
        print("Humidity = "+str(humidity)+"%")
        print("Temperature = "+str(temp)+"C")
        dbupdate = 0
    return

# Main program starts here.
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
