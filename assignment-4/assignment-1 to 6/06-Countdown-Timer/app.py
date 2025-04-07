import time

def countdown(t):
    while t > 0:
        mins, secs = divmod(t, 60)   
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')  
        time.sleep(1)   
        t -= 1  
    print("00:00")  


time_in_seconds = int(input("Enter the time in seconds: "))
countdown(time_in_seconds)
