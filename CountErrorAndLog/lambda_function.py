import boto3 
import json 
from datetime import datetime
import datetime 
import time
import logging
# import tabulate
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    time_duration = '4h'
    log_group_name = "/aws/containerinsights/aws-dev-eks-cluster/application"
    filter_pattern = 'filter @message like /error/'
    # increase_threshold_count_by = 20000
    # cron_job_scheduled_at = '17:31:00'
    # alarm_information = get_alarm_description(event['alarmData']['alarmName'])
    now = datetime.datetime.now()
    end_time = now.strftime("%Y-%m-%d %H:%M:%S")
    epoc_end_time = get_epoc_time(end_time)

    start_time = calculate_duration_from_now(time_duration)
    epoc_start_time = get_epoc_time(start_time)
    response = filter_events(log_group_name, epoc_start_time, epoc_end_time, filter_pattern)
    logger.info("Length of the response: %d", json.dumps(len(response)))

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda function executed successfully!')
    }




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
        time.sleep(1)
        response = client.get_query_results(
            queryId=query_id
        )
    # TO-DO
    # This return response shold be in json format
    return response['results']