from datetime import datetime
import datetime 
import time

def absolute_time_differnence(cron_job_scheduled_at):
    now = datetime.datetime.now()
    given_time = datetime.datetime.strptime(cron_job_scheduled_at, "%H:%M:%S")
    time_difference = given_time - now
    # time_difference =  abs(time_difference.total_seconds())
    # time_difference_in_minutes = (int)(time_difference/60 )
    # only muliple of 60 is accepted or 0,15,30
    return (time_difference)

# print(absolute_time_differnence('00:00:00'))

# hr -> 3600
# min -> 60
# sec -> 1


# current_time = now.strftime("%H:%M:%S")

# print(current_time)

def calculate_absolute_time_difference(corn_job_scheduled_at):
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_time = current_time.split(':')  
    given_time = corn_job_scheduled_at.split(':')
    hours_to_sec = abs((int)(current_time[0])-(int)(given_time[0]))*3600
    minutes_to_sec = abs((int)(current_time[1])-(int)(given_time[1]))*60    
    seconds_to_sec = abs((int)(current_time[2])-(int)(given_time[2]))
    sum = (int)((hours_to_sec+minutes_to_sec+seconds_to_sec)/60)
    return int(sum)*60

print(calculate_absolute_time_difference('23:18:45'))