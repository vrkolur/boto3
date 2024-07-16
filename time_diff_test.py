from datetime import datetime

def calculate_absolute_time_difference_in_seconds(given_time_str):
    given_time_components = given_time_str.split(':')
    
    if len(given_time_components) != 3:
        print("Enter in the corrent format")
        exit(0)
    
    given_time = datetime.strptime(f"{given_time_str}", "%H:%M:%S")
    
    current_time = datetime.now()
    
    time_difference = given_time - current_time
    
    return abs(time_difference.total_seconds())


some_time = "14:30:00"
abs_differnence = calculate_absolute_time_difference_in_seconds(some_time)

current_time = datetime.now()
a = datetime.now()

current_time = a.strftime("%H:%M:%S")
print(current_time)



