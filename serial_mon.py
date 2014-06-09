#Imports the serial lib's
import serial

#Import the string handling lib's
import string

#Import the mysql lib's
import MySQLdb


# Port and speed settings
port = "/dev/ttyACM0"

#Initialise variables.
complete_string = ""
humidity = 0
temp = 0
dbupdate = 0

#database values
database = "yourdb"
db_user = "youruser"
db_pass = "yourpassword"

# Set up the serial port 9600 (8N1=Default)
ser = serial.Serial(port,9600)

#function to split the string and work out which value to update
def process_string(string_to_process):
  words = string.split(string_to_process)
  #use the global values
  global humidity
  global temp
  global dbupdate
    
  #check to see if we are getting what we want otherwise it will crash
  if words[0] == "a:":
    #if the value has changed since the last time update the global value
    if humidity != float(words[1]):
        humidity = float(words[1])
        # if the value has changed set the DB update flag
        dbupdate = 1   
  
  if words[0] == "b:":    
    #if the value has changed since the last time update the global value
    if temp != float(words[1]):
        temp = float(words[1])
        # if the value has changed set the DB update flag
        dbupdate = 1
  return

def write_to_db():
    #use global var's
    global dbupdate
    global humidity
    global temp
    
    db = MySQLdb.connect("localhost", db_user, db_pass, database)
    cursor = db.cursor()
    

    # If there has been an update update the DB
    if dbupdate == 1:
        if (temp != 0) and (humidity != 0):
            print("Humidity = "+str(humidity)+"%")
            print("Temperature = "+str(temp)+"C")
            #reset the DB flag to 0
            dbupdate = 0
            #build the sql string
            sql = "INSERT INTO cabin_values \
            (temp, humidity, timestamp) VALUES \
            ('%f', '%f', now()) " % \
            (temp, humidity)
            print(sql)
            try:
                cursor.excute(sql)
                db.commit()
            except:
                db.rollback()
    db.close()            
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
