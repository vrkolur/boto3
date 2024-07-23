from datetime import datetime

# Convert the time strings to datetime objects
time1 = datetime.strptime('02:00:00', '%H:%M:%S')
time2 = datetime.strptime('16:00:00', '%H:%M:%S')
c = datetime.now()
current_time = c.strftime('%H:%M:%S')

print(current_time)

# Calculate the time difference
time_diff = time2 - time1

# Convert the time difference to seconds
seconds = abs(time_diff.total_seconds())

print(f"Time difference in seconds: {seconds}")
