import boto3 
import json 
from datetime import datetime
import datetime 
import time
import logging
# import tabulate
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Alarm Names are:
    # 1. 401_status_code_error 
    # 2. 403_status_code_error
    # 3. Add new ones if you find any.
    # The threshold is updating almost 3 time check why?


# Update the info at lambda_handeler only 
def lambda_handler(event, context):
    try:
        # logs_client = boto3.client('logs')
        time_duration = '4h'
        log_group_name = "/aws/containerinsights/aws-dev-eks-cluster/application"
        filter_pattern = 'filter @message like /error/'
        increase_threshold_count_by = 20000
        cron_job_scheduled_at = '17:31:00'
        alarm_handler(event, log_group_name, filter_pattern, increase_threshold_count_by, time_duration, cron_job_scheduled_at)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e


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
def update_alarm_status(alarm_information, new_threshold, time_duration ):
    # Perform put_metric_data here
    # chage the status and update the threshold by provided unit

    # get the ARN of the lambda function
    lambda_function_name = 'list-log-group-names'
    lambda_response = lambda_client.get_function(FunctionName=lambda_function_name)
    lambda_arn = lambda_response['Configuration']['FunctionArn']

    # Put your arn here
    notification_arn = 'arn:aws:sns:us-east-1:126263378245:Alarm_status'

    # Any value to be updated put it here 
    alarm_name = alarm_information['AlarmName']
    metric_name = alarm_information['MetricName']
    namespace = alarm_information['Namespace']
    statistic = 'Sum'
    # period max can be 1d or 86400 seconds.
    period = time_duration
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
    return response
    

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


# calculate 
def calculate_duration_from_now(time_duration):
    now = datetime.datetime.now()
    duration_in_seconds = convert_into_seconds(time_duration)
    # duration_in_seconds = 300
    trailing_time = now - datetime.timedelta(seconds=duration_in_seconds)
    return trailing_time.strftime("%Y-%m-%d %H:%M:%S")

# This is discarded because the time is calculated from 1970 
# def absolute_time_differnence(cron_job_scheduled_at):
#     now = datetime.datetime.now()
#     given_time = datetime.datetime.strptime(cron_job_scheduled_at, "%H:%M:%S")
#     time_difference = given_time - now
#     time_difference =  abs(time_difference.total_seconds())
#     time_difference_in_minutes = (int)(time_difference/60 )
#     # only muliple of 60 is accepted or 0,15,30
#     return (int)(time_difference_in_minutes)*60


def calculate_absolute_time_difference(corn_job_scheduled_at):
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_time = current_time.split(':')  
    given_time = corn_job_scheduled_at.split(':')
    hours_to_sec = abs((int)(current_time[0])-(int)(given_time[0]))*3600
    minutes_to_sec = abs((int)(current_time[1])-(int)(given_time[1]))*60    
    seconds_to_sec = abs((int)(current_time[2])-(int)(given_time[2]))
    sum = (int)((hours_to_sec+minutes_to_sec+seconds_to_sec)/60)
    # The Alarm Update period field only expects multiples of 60 hence.
    return int(sum)*60


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
        abs_time_period = calculate_absolute_time_difference(cron_job_scheduled_at)
        # alarm_update_response = update_alarm_status(alarm_information, new_threshold, (int)(abs_time_period))

        # if alarm_update_response['ResponseMetadata']['HTTPStatusCode'] == 200:
        #     # get the current time and convert it into epoc time
        #     now = datetime.datetime.now()
        #     end_time = now.strftime("%Y-%m-%d %H:%M:%S")
        #     epoc_end_time = get_epoc_time(end_time)

        #     start_time = calculate_duration_from_now(time_duration)
        #     epoc_start_time = get_epoc_time(start_time)
        #     response = filter_events(log_group_name, epoc_start_time, epoc_end_time, filter_pattern)
        #     if response is not None:
        #         logger.info(f"Lambda called Successfullt and the number of errors are: {len(response)}")
        #     else:
        #         logger.info("Error Fetching Data")
        # else:
        #     logger.info("Error at updating the alarm status")
