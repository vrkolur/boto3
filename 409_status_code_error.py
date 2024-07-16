import boto3
import time
from prettytable import PrettyTable
from datetime import datetime
import sys


def get_epoc_time(input_date_time):
    try:
        date_format = "%Y-%m-%d %H:%M:%S"
        
        past_datetime = datetime.strptime(input_date_time, date_format)
        
        time_since_epoch_milliseconds = int(past_datetime.timestamp() * 1000)
        
        return time_since_epoch_milliseconds
    except ValueError:
        print("Invalid date format. Please try again.")


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
        print('Waiting for query to complete ...')
        time.sleep(2)
        response = client.get_query_results(
            queryId=query_id
        )

    return response['results']

log_group_name = "/aws/elasticbeanstalk/Boost-Prod/var/log/web.stdout.log"

# Get the start time
start_time = input("Enter startTime in YYYY-MM-DD HH:MM:SS format only:")
epoc_start_time = get_epoc_time(start_time)

#  Get the end time 
end_time = input("Enter endTime in YYYY-MM-DD HH:MM:SS format only:")
epoc_end_time = get_epoc_time(end_time)

# Filter Pattern
filter_pattern = "filter @message like /409 CONFLICT/ | parse @message'c.p.n.s.p.MetadataConsumerProcessor      : *:* :' as test,guid| stats count(*) by guid"
# filter_pattern = "filter @message like /409 CONFLICT/ | limit 5"


# Get the response
response = filter_events(log_group_name, epoc_start_time, epoc_end_time, filter_pattern)

# print(response)


table = PrettyTable()
table.field_names = ['guid','count']

count=0
threshold_count = 1 # default threshold
if len(sys.argv) == 2:
   threshold_count=(int)(sys.argv[1])

for i in range(0,len(response)):
    try:
        if (int)(response[i][1]['value']) >= threshold_count:
            count+=1
            table.add_row([response[i][0]['value'][:10],response[i][1]['value']])
    except IndexError:
        pass

# Print the result
# print(threshold_count)
print(table)
print(count)



# 2024-06-22 00:00:00
# 2024-06-22 23:59:59