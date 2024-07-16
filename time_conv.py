import time
from datetime import datetime

current_time_seconds = time.time()

# print(current_time_seconds)
print((int)(datetime.now().timestamp()*1000))

current_time_milliseconds = int(current_time_seconds * 1000)

print("Current time in milliseconds:", current_time_milliseconds)

def get_epoc_time(input_date_time):
    try:
        date_format = "%Y-%m-%d %H:%M:%S"
        
        past_datetime = datetime.strptime(input_date_time, date_format)
        
        time_since_epoch_milliseconds = int(past_datetime.timestamp() * 1000)
        
        # print(f"Time since epoch in milliseconds: {time_since_epoch_milliseconds}")
        return time_since_epoch_milliseconds
    except ValueError:
        print("Invalid date format. Please try again.")


start_time = input("Enter startTime in YYYY-MM-DD HH:MM:SS format only ")
epoc_start_time = get_epoc_time(start_time)
if epoc_start_time is not None: print(epoc_start_time)

end_time = input("Enter endTime in YYYY-MM-DD HH:MM:SS format only ")
epoc_end_time = get_epoc_time(end_time)
if epoc_end_time is not None: print(epoc_end_time)
