# import time
# from datetime import datetime

# current_time_seconds = time.time()

# # print(current_time_seconds)
# print((int)(datetime.now().timestamp()*1000))

# current_time_milliseconds = int(current_time_seconds * 1000)

# print("Current time in milliseconds:", current_time_milliseconds)

# def get_epoc_time(input_date_time):
#     try:
#         date_format = "%Y-%m-%d %H:%M:%S"
        
#         past_datetime = datetime.strptime(input_date_time, date_format)
        
#         time_since_epoch_milliseconds = int(past_datetime.timestamp() * 1000)
        
#         # print(f"Time since epoch in milliseconds: {time_since_epoch_milliseconds}")
#         return time_since_epoch_milliseconds
#     except ValueError:
#         print("Invalid date format. Please try again.")


# start_time = input("Enter startTime in YYYY-MM-DD HH:MM:SS format only ")
# epoc_start_time = get_epoc_time(start_time)
# if epoc_start_time is not None: print(epoc_start_time)

# end_time = input("Enter endTime in YYYY-MM-DD HH:MM:SS format only ")
# epoc_end_time = get_epoc_time(end_time)
# if epoc_end_time is not None: print(epoc_end_time)


from datetime import datetime, timedelta

def calculate_time_difference_in_seconds(given_time_str):
    given_time_components = given_time_str.split(':')
    
    if len(given_time_components) != 3:
        print("Invalid time format. Please provide the time in 'HH:MM:SS' format.")
        return None
    
    given_time = datetime.strptime(f"{given_time_str}", "%H:%M:%S")
    
    current_time = datetime.now()
    
    time_difference = given_time - current_time
    
    return abs(time_difference)


# Current time: 2023-05-24 14:30:00
time_diff_seconds = calculate_time_difference_in_seconds("16:45:00")
print(f"Time difference in seconds: {time_diff_seconds}")  

time_diff_seconds = calculate_time_difference_in_seconds("12:00:00")
print(f"Time difference in seconds: {time_diff_seconds}") 
