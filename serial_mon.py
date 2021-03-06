########################################################
#
# IMPORTANT THIS IS THE SQL to retrieve the latest entry
# select * from cabin_values order by time DESC limit 1;
#
########################################################


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
battery_voltage = 0


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
    global battery_voltage
    
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
        
    if words[0] == "c:":
        if battery_voltage != int(words[1]):
            battery_voltage = int(words[1])
            dbupdate = 1 

    # Add more fields here when required, if you have more 
    # fields or add more fields later.        
 

def write_to_db():
    #use global var's
    global dbupdate
    global humidity
    global temp
    global battery_voltage
    
    db = MySQLdb.connect("localhost", db_user, db_pass, database)
    cursor = db.cursor()
        

    # If there has been an update update the DB
    if dbupdate == 1:
        if (temp != 0) and (humidity != 0) and (battery_voltage != 0):
            print("Humidity = "+str(humidity)+"%")
            print("Temperature = "+str(temp)+"C")
            real_voltage = float(float(battery_voltage)*(0.00488758553275)*7)
            print("Voltage = "+str(real_voltage)+"V")
            
            #reset the DB flag to 0
            dbupdate = 0
            
            #build the sql string inserting the values
            sql = "INSERT INTO cabin_values \
            (temp, humidity, voltage, time) VALUES \
            (%f, %f, %f, now()); " % \
            (temp, humidity, real_voltage)
            
            # Try to execute the SQL, If it fails roll back the SQL code and 
            # do not commit
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
    
    #must remember to close the DB always...
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
