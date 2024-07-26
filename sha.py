import datetime
from datetime import datetime
import time

def absolute_time_differnence(cron_job_scheduled_at):
    # now = datetime.now()
    curr_time = time.strftime("%H:%M:%S", time.localtime())
    given_time = datetime.strptime(cron_job_scheduled_at, '%H:%M:%S')
    time_difference = given_time - curr_time
    time_difference =  abs(time_difference.total_seconds())
    print(time_difference)
    time_difference = time_difference/60 
    # only muliple of 60 is accepted or 0,15,30
    return (int)(time_difference)*60

print(absolute_time_differnence("18:00:00"))

# curr_time = time.strftime("%H:%M:%S", time.localtime())

# print("Current Time is :", curr_time)
