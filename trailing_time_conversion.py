from datetime import datetime
import datetime
import sys

def convert_into_seconds(duration_str):
    duration_map = {'h': 3600, 'd': 86400, 'w': 604800}
    try:
        multiplier, unit = duration_str[:-1], duration_str[-1].lower()
        return int(multiplier) * duration_map[unit]
    except KeyError:
        raise ValueError("Enter either h, d or w ")

def calculate_duration_from_now(selected_duration):
    now = datetime.datetime.now()
    duration_in_seconds = convert_into_seconds(selected_duration)
    past_time = now - datetime.timedelta(seconds=duration_in_seconds)
    return past_time.strftime("%Y-%m-%d %H:%M:%S")



res = calculate_duration_from_now(sys.argv[1])
print(res)



now = datetime.datetime.now()

formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

print(formatted_time)

