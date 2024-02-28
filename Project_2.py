###################################################################
# Computer Project #11
# Calendar assistant that records and updates events for the user
# Fill the calendar instance with events
# Create instances of the event class
# Create a calender class 
# Implement the classes into the main code to be used
# Display closing messages
###################################################################

#from p11_calendar import P11_Calendar
from p11_event import P11_Event
from p11_calendar import P11_Calendar


CAL_TYPE = ['meeting','event','appointment','other']

MENU = '''Welcome to your own personal calender.
  Available options:
    (A)dd an event to calender
    (D)elete an event
    (L)ist the events of a particular date
    (Q)uit'''


def check_time(time,duration):
    """
       Tests if the time and duration are valid
       value: Time (string), duration (int)
       Returns: True or False (bool)
    """
    day_start = 360 #start time in minutes (6 * 60)
    day_end = 1020 # end time in minutes (17 * 60)
    # first make sure time is valid
    try:
        #check if time is well formed
        if time == None:
            return False    #return False if not valid
        timeList = time.split(':') #time

        #perform sanity check on duration. If not int then exception
        if duration < 1:
            return False

        #calculate time in munutes
        sTime=(int(timeList[0])*60)+int(timeList[1])
        #check the time fits in the 6am to 5pm window
        if ((sTime >= day_start) and ((sTime + duration) <= day_end)):
            return True
        return False
    except:
        return False

            
def event_prompt():
    """
       Prompts for an event until the valid one is entered
       value: None
       Returns: event (p11_event)
    """
    while (True):
        #prompt user to enter date,time, duration and type
        date = input('Enter a date (mm/dd/yyyy): ')
        time = input('Enter a start time (hh:mm): ')
        duration = input('Enter the duration in minutes (int): ')
        e_type = input("Enter event type [\'meeting\',\'event\',\'appointment\',\'other\']: ")
        
        #check if time/duratiion are in valid range
        if(check_time(time,int(duration)) == False):
            print('Invalid event. Please try again.')
            continue
        #attempt to create the event
        e = P11_Event(date, time, int(duration), e_type) #event object
        if (e.valid == True):
            print ("Add Event")
            break
        else:
            print('Invalid event. Please try again.')
            continue
    #return event object
    return e

def main():
    c= P11_Calendar()
    while True:
        #print main menu display 
        print(MENU)
        #allow user to input an option
        opt = input ("Select an option: ") #option
        l_opt= opt.lower() #lower option
        #test to see what option is entered
        if l_opt == "a":
            #if a is entered, call the event prompt function
            evnt= event_prompt() #event
            #add event to the calender
            if(c.add_event(evnt) == True):
                print ('Event successfully added.')
            else:
                print("*****Error in add_event")

        if l_opt == "d":
            #print delete message
            print ("Delete Event")
            #prompt user for date and time 
            dt =input ("Enter a date (mm/dd/yyyy): ") #date enter
            st= input ("Enter a start time (hh:mm): ") #start enter
            #call the delete function from the calender
            if (c.delete_event(dt,st) == True):
                #if true, display the event deleted message
                print ("Event successfully deleted.")
            else: 
                #else, print the error message
                print ("Event was not deleted.")
        if l_opt == "l":
            print ("List Events")
            #user prompted to enter date for listing
            dt= input("Enter a date (mm/dd/yyyy): ") #date
            #call day_schedule method to create list of day events
            evnt_list = c.day_schedule(dt)
            #test for no events in the list
            if (len(evnt_list) ==0):
                #no events returned, print no events
                print ("No events to list on  " + dt)
                continue
            #print each event
            for x in evnt_list:
                print (x)
        if l_opt == "q":
            #quit the program
            break
    
if __name__ == '__main__':
     main()