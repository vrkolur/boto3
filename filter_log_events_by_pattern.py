import boto3
# from datetime import datetime, timedelta, timezone

def filter_log_events_by_pattern(log_group_name, start_time=None, end_time=None, filter_pattern="401 Unauthorized"):
    client = boto3.client('logs')
    
    # if start_time is None:
    #     start_time = datetime.now(timezone.utc) - timedelta(minutes=60)  
    # if end_time is None:
    #     end_time = datetime.now(timezone.utc) 
    
    response = client.filter_log_events(
        logGroupName=log_group_name,
        startTime = start_time,
        filterPattern = filter_pattern,
        endTime = end_time,
        limit=10
    )

    # print(response)
    
    filtered_events = []
    
    for event in response['events']:
        if filter_pattern in event['message']:
            filtered_events.append(event)
    
    return filtered_events

log_group_name = "/aws/elasticbeanstalk/Boost-Prod/var/log/web.stdout.log"
filtered_events = filter_log_events_by_pattern(log_group_name,1719014400000,1719100799000)

for event in filtered_events:
    print(event)
