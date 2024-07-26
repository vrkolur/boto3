import boto3
import sys
from datetime import datetime
import datetime
import time
from prettytable import PrettyTable

if len(sys.argv) <3:
    print("Wrong no of arguments")
    exit(0)

def convert_into_seconds(duration_str):
    
    if duration_str[-2].isdigit():
        print(duration_str[:(len(duration_str))-2])
        duration_map = {'h': 3600, 'd': 86400, 'w': 604800}
        try:
            multiplier, unit = duration_str[:-1], duration_str[-1].lower()
            return int(multiplier) * duration_map[unit]
        except KeyError:
            print("Error at time conversion")
            exit(0)
    else :
        print("Wrong syntax")
        exit(0)

def calculate_duration_from_now(selected_duration):
    now = datetime.datetime.now()
    duration_in_seconds = convert_into_seconds(selected_duration)
    trailing_time = now - datetime.timedelta(seconds=duration_in_seconds)
    return trailing_time.strftime("%Y-%m-%d %H:%M:%S")


def check_for_status_code(user_choice):
    valid_options = [401, 403, 409]
    try:
        if user_choice in valid_options:
            return user_choice
        else:
            print("Invalid option. Please enter 401, 403 or 409")
            exit(0)
    except ValueError:
        print("Please enter a number.")
        exit(0)


def get_epoc_time(input_date_time):
    try:
        date_format = "%Y-%m-%d %H:%M:%S"
        
        past_datetime = datetime.datetime.strptime(input_date_time, date_format)
        
        time_since_epoch_milliseconds = int(past_datetime.timestamp() * 1000)
        
        return time_since_epoch_milliseconds
    except ValueError:
        print("Invalid date format. Please try again.")
        exit(0)



def filter_events(log_group_name, start_time = 1719014400000, end_time = 1719100799000, filter_pattern = "fields @timestamp, @message, @logStream, @log| sort @timestamp desc| limit 10000"):
    client = boto3.client('logs')
    
    start_query_response = client.start_query(
        logGroupName=log_group_name,
        startTime=start_time,  
        endTime=end_time,    
        queryString = filter_pattern
    )
        
    query_id = start_query_response['queryId']

    response = None

    while response == None or response['status'] == 'Running':
        # print('Waiting for query to complete ...')
        time.sleep(2)
        response = client.get_query_results(
            queryId=query_id
        )

    return response['results']


def handle_status_code(status_code,log_group_name,start_time,end_time,filter_pattern):
    actions = {
        401: lambda: filter_events(log_group_name,start_time,end_time,filter_pattern[0]),
        403: lambda: filter_events(log_group_name,start_time,end_time,filter_pattern[1]),
        409: lambda: filter_events(log_group_name,start_time,end_time,filter_pattern[2]),
    }
    
    action = actions.get(status_code, lambda: "Invalid status code")
    result = action()
    return result


filter_pattern=[]
filter_pattern.append("filter @message like /401 Unauthorized/ and @message like /guid/ | parse @message '\"orgID\":*,' as orgId | stats count(*) by orgId")
# filter_pattern.append("filter @message like /403 Forbidden/ and @message like /guid/ | parse @message '\"orgID\":*,' as orgId | parse @message '\"guid\":\"*' as guid | stats count(*) by guid, orgId")
filter_pattern.append("filter @message like /403 Forbidden/ and @message like /guid/ | parse @message '\"orgID\":*,' as orgId | stats count(*) by orgId")
filter_pattern.append("filter @message like /409 CONFLICT/ | parse @message'c.p.n.s.p.MetadataConsumerProcessor      : *:* :' as test,guid| stats count(*) by guid")
# AWS logGroupName
log_group_name = "/aws/elasticbeanstalk/Boost-Prod/var/log/web.stdout.log"


threshold_count = 1 # default value
if len(sys.argv)==5:
    threshold_count = (int)(sys.argv[3])
    log_group_name = sys.argv[4]
elif len(sys.argv)==4:
    threshold_count = (int)(sys.argv[3])


status_code =  check_for_status_code((int)(sys.argv[1]))

# To get end_time i.e Current_time
now = datetime.datetime.now()
end_time = now.strftime("%Y-%m-%d %H:%M:%S")
epoc_end_time = get_epoc_time(end_time)

# get start_time is the trailing time 
start_time = calculate_duration_from_now(sys.argv[2])
epoc_start_time = get_epoc_time(start_time)

# get the response from the api
response = handle_status_code(status_code,log_group_name, epoc_start_time, epoc_end_time, filter_pattern)

# generate in the form of a table
table = PrettyTable()
table.field_names = ['orgID','count']
count=0
for i in range(0,len(response)):
    try:
        if (int)(response[i][1]['value']) >= threshold_count:
            count+=1
            table.add_row([response[i][0]['value'][:10],response[i][1]['value']])
    except IndexError:
        pass

print(table)
print('\n'+'Table Length: '+ (str)(count) +'\n')

# 2024-06-22 00:00:00
# 2024-06-22 23:59:59

# Errors if any
# 1. You can query only of the provided (401,403,409).
# 2. If you don't get any results try changing the filter_pattern then try 
# 3. Refresh the aws access key if security issue.
# 4. If you want to add status code into the program to query follow the below:
    # 1. ask_for_status_code, change code here 
    # 2. handle_status_code, create a lambda functio for the new query_pattern you want to create
    # 3. Append your filter pattern into this list: 'filter_pattern []'

# Quick Tip:
    # 1. logGroupName is hard coded, change it manually
    # 2. only trailing time is allowed
    # 3. Please follow the syntax Carefully 
        # 1. SYNTAX 'python file.py status_code trailing_time threshold ' (allowed h,d and w)
    # 4. In future more new filter_pattern needs to be added then, change the filter_pattern list to a map data structure (map the status codes to the filter pattern)

