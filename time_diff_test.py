from datetime import datetime, timedelta

def calculate_time_difference_in_seconds(given_time_str):
    current_year = datetime.now().year
    given_time_components = given_time_str.split(':')
    
    if len(given_time_components) != 3:
        print("Invalid time format. Please provide the time in 'HH:MM:SS' format.")
        return None
    
    given_time_str_with_year = f"{current_year}-{given_time_str}"
    print(given_time_str_with_year)
    given_time = datetime.strptime(given_time_str_with_year, "%Y-%H:%M:%S")
    
    current_time = datetime.now()
    
    time_difference = given_time - current_time
    
    return abs(time_difference)


test_time = '14:00:00'
res = calculate_time_difference_in_seconds(test_time)
print(res)