import boto3 
import json 
from datetime import datetime
import datetime 
import time
from prettytable import PrettyTable
# import logging

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
    # duration_in_seconds = convert_into_seconds(time_duration)
    duration_in_seconds = 300
    trailing_time = now - datetime.timedelta(seconds=duration_in_seconds)
    return trailing_time.strftime("%Y-%m-%d %H:%M:%S")



def send_email_via_sns(topic_arn, subject, message, source_email):
    sns = boto3.client('sns')

    # Create the email message
    email_message = f"From: {source_email}\nSubject: {subject}\n\n{message}"

    # Publish the message to the SNS topic
    response = sns.publish(
        TopicArn=topic_arn,
        Message=email_message,
        Subject=subject,
        MessageStructure='string'
    )

    return response

# Example usage


# log_group_name = "/aws/elasticbeanstalk/Boost-Prod/var/log/web.stdout.log"
log_group_name = "/aws/containerinsights/aws-dev-eks-cluster/application"
# filter_pattern = ("filter @message like /401 Unauthorized/ and @message like /guid/ | parse @message '\"orgID\":*,' as orgId | stats count(*) by orgId")
filter_pattern = "fields @timestamp, @message, @logStream, @log| sort @timestamp desc| limit 10"


now = datetime.datetime.now()
end_time = now.strftime("%Y-%m-%d %H:%M:%S")
epoc_end_time = get_epoc_time(end_time)

start_time = calculate_duration_from_now('1w')
epoc_start_time = get_epoc_time(start_time)

response = filter_events(log_group_name, epoc_start_time, epoc_end_time, filter_pattern)


table = PrettyTable()
table.field_names = ['orgID','count']
# count=0
for i in range(0,len(response)):
    try:
        # if (int)(response[i][1]['value']):
        # count+=1
        # table.add_row([response[i][0]['value'][:10],response[i][1]['value']])
        table.add_row([i+1,i+3])
    except IndexError:
        pass



topic_arn = 'arn:aws:sns:us-east-1:126263378245:Alarm_status'
subject = 'Test Email'
message = f'This is a test email sent via Amazon SNS.\nLog group Name: {log_group_name}\nDate: {datetime.datetime.now()} \n {table}'
source_email = 'varun.ravikolur@plansource.com'

response = send_email_via_sns(topic_arn, subject, message, source_email)
print(response)