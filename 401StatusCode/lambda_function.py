import boto3 
import json 
from datetime import datetime, timedelta
import datetime 
import time


# Update the info at lambda_handeler only 

def lambda_handeler(event, context):
    logs_client  = boto3.client('logs')
    time_duration = '4h' 
    log_group_name = "/aws/lambda/aws-prod-gb-boostNotifyQueueProcessor" 
    filter_pattern = "filter @message like /401 Unauthorized/ and @message like /guid/ | parse @message '\"orgID\":*,' as orgId | stats count(*) by orgId"
    increase_threshold_count_by = 20
    # Enter in HH:MM:SS format only (24 hr clock format)
    cron_job_scheduled_at= '00:00:00'

cloudwatch_client = boto3.client('cloudwatch')
lambda_client = boto3.client('lambda')



def get_alarm_description(alarm_name, timestamp):
    alarm_name = 'lambda_error_alarm'
    alarm_type = 'MetricAlarm'

    response = cloudwatch_client.describe_alarms(
        AlarmNames=[alarm_name],
        AlarmTypes=[alarm_type]
    )
    if response['MetricAlarms']:
        alarm = response['MetricAlarms'][0]
        alarm_information = {
            "AlarmName" : alarm['AlarmName'],
            "MetricName" : alarm['MetricName'],
            "Namespace" : alarm['Namespace'],
            "Statistic" : alarm['Statistic'],
            "Period" : alarm['Period'],
            "EvaluationPeriods" : alarm['EvaluationPeriods'],
            "Threshold" : alarm['Threshold'],
            "ComparisonOperator" : alarm['ComparisonOperator'],
            "AlarmDescription" : alarm['AlarmDescription'],
            "AlarmTime" : timestamp,
            "StateValue" : alarm['StateValue']
        }
    else:
        exit(0)
    return alarm_information

# Here increase count is new_threshold
def update_alarm_status(new_threshold, alarm_information ):
    # Perform put_metric_data here
    # chage the status and update the threshold by provided unit

    # get the ARN of the lambda function
    lambda_function_name = 'list-log-group-names'
    lambda_response = lambda_client.get_function(FunctionName=lambda_function_name)
    lambda_arn = lambda_response['Configuration']['FunctionArn']

    # Put your arn here
    notification_arn = 'arn:aws:sns:us-east-1:126263378245:Alarm_status'

    # Any value to be updated put it here 
    alarm_name = 'lambda_error_alarm'
    metric_name = 'lambda_demo_error_pattern'
    namespace = 'filter_demo'
    statistic = 'Sum'
    threshold = 14
    period = 60
    evaluation_periods = 1
    comparison_operator = 'GreaterThanThreshold'

    response = cloudwatch_client.put_metric_alarm(
        AlarmName=alarm_name,
        MetricName=metric_name,
        Namespace=namespace,
        Statistic=statistic,
        Period=period,
        EvaluationPeriods=evaluation_periods,
        Threshold=threshold,
        ComparisonOperator=comparison_operator,
        TreatMissingData='notBreaching',
        AlarmActions=[lambda_arn, notification_arn],
        AlarmDescription='Alarm to monitor Lambda errors and invoke a function',
        OKActions=[notification_arn]
    )
    if response is not None:
        return 1 if response['ResponseMetadata']['HTTPStatusCode'] == 200 else 0
    else:
        return 0



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


# for the trailing time or the future time of cron job scheduled 

# def calculate_absolute_time_difference_in_seconds(given_time_str):
#     given_time_components = given_time_str.split(':')
    
#     if len(given_time_components) != 3:
#         print("Enter in the corrent format")
#         exit(0)
    
#     given_time = datetime.strptime(f"{given_time_str}", "%H:%M:%S")
    
#     current_time = datetime.now()
    
#     time_difference = given_time - current_time
    
#     return abs(time_difference.total_seconds())

# calculate 
def calculate_duration_from_now(selected_duration):
    now = datetime.datetime.now()
    duration_in_seconds = convert_into_seconds(selected_duration)
    trailing_time = now - datetime.timedelta(seconds=duration_in_seconds)
    return trailing_time.strftime("%Y-%m-%d %H:%M:%S")


# Filter the action based on the alarm trigged (privide values els defalut valu is selected)
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
    # TO-DO
    # This return response shold be in the form if json data 
    return response['results']

def alarm_handeler(event, new_threshold, cron_job_time, new_metric_data):
    # get the alarm information
    alarm_information = get_alarm_description('lambda_error_alarm', event['time'])
    if alarm_information['StateValue'] == 'ALARM':
        update_alarm_status(4000, alarm_information)