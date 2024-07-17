import boto3 
import json 
from datetime import datetime
import datetime 
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Update the info at lambda_handeler only 

def lambda_handler(event, context):
    logs_client  = boto3.client('logs')
    time_duration = '4h' 
    log_group_name = "/aws/containerinsights/aws-dev-eks-cluster/application"
    # filter_pattern = "filter @message like /401 Unauthorized/ and @message like /guid/ | parse @message '\"orgID\":*,' as orgId | stats count(*) by orgId"
    filter_pattern  = 'filter @message like /error/'
    increase_threshold_count_by = 20000
    # Enter in HH:MM:SS format only (24 hr clock format)
    cron_job_scheduled_at= '00:00:00'
    alarm_handler(event, log_group_name, filter_pattern, increase_threshold_count_by, time_duration, cron_job_scheduled_at)

cloudwatch_client = boto3.client('cloudwatch')
lambda_client = boto3.client('lambda')



def get_alarm_description(alarm_name):

    response = cloudwatch_client.describe_alarms(
        AlarmNames=[alarm_name]
    )

    # This will store the alarm Information
    alarm_information = {}

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
            "StateValue" : alarm['StateValue']
        }
    else:
        exit(0)
    return alarm_information

# Here increase count is new_threshold
def update_alarm_status(alarm_information, new_threshold ):
    # Perform put_metric_data here
    # chage the status and update the threshold by provided unit

    # get the ARN of the lambda function
    lambda_function_name = 'list-log-group-names'
    lambda_response = lambda_client.get_function(FunctionName=lambda_function_name)
    lambda_arn = lambda_response['Configuration']['FunctionArn']

    # Put your arn here
    notification_arn = 'arn:aws:sns:us-east-1:126263378245:Alarm_status'

    # Any value to be updated put it here 
    alarm_name = alarm_information
    metric_name = alarm_information['MetricName']
    namespace = alarm_information
    statistic = 'Sum'
    period = 60
    evaluation_periods = 1
    old_threshold = alarm_information['Threshold']
    comparison_operator = 'GreaterThanThreshold'

    response = cloudwatch_client.put_metric_alarm(
        AlarmName=alarm_name,
        MetricName=metric_name,
        Namespace=namespace,
        Statistic=statistic,
        Period=period,
        EvaluationPeriods=evaluation_periods,
        Threshold= (old_threshold + new_threshold),
        ComparisonOperator=comparison_operator,
        TreatMissingData='notBreaching',
        AlarmActions=[lambda_arn, notification_arn],
        AlarmDescription='Alarm to monitor Lambda errors and invoke a function'
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
    


def get_epoc_time(input_date_time):
    try:
        date_format = "%Y-%m-%d %H:%M:%S"
        
        past_datetime = datetime.datetime.strptime(input_date_time, date_format)
        
        time_since_epoch_milliseconds = int(past_datetime.timestamp() * 1000)
        
        return time_since_epoch_milliseconds
    except ValueError:
        print("Invalid date format. Please try again.")
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
def calculate_duration_from_now(time_duration):
    now = datetime.datetime.now()
    # duration_in_seconds = convert_into_seconds(time_duration)
    duration_in_seconds = 300
    trailing_time = now - datetime.timedelta(seconds=duration_in_seconds)
    return trailing_time.strftime("%Y-%m-%d %H:%M:%S")


# Filter the action based on the alarm trigged (privide values els defalut value will be selected)
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
    # This return response shold be in json format
    return response['results']

def alarm_handler(event, log_group_name, filter_pattern, new_threshold, time_duration, cron_job_scheduled_at ):
    # get the alarm information
    alarm_information = get_alarm_description(event['alarmData']['alarmName'])
    if alarm_information['StateValue'] == 'ALARM':
        update_alarm_status(alarm_information, new_threshold)

        # get the current time and convert it into epoc time
        now = datetime.datetime.now()
        end_time = now.strftime("%Y-%m-%d %H:%M:%S")
        epoc_end_time = get_epoc_time(end_time)

        start_time = calculate_duration_from_now(time_duration)
        epoc_start_time = get_epoc_time(start_time)
        response = filter_events(log_group_name, start_time, end_time, filter_pattern)
        logger.info(f"Lambda called Successfullt and the no of errors are: {len(response)}")
