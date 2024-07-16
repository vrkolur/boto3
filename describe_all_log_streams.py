import boto3

def describe_log_streams(log_group_name):
    client = boto3.client('logs')
    
    try:
        response = client.describe_log_streams(logGroupName=log_group_name)
        
        for stream in response['logStreams']:
            print(stream['arn'])
    except Exception as e:
        print(f"An error occurred: {e}")

describe_log_streams("/aws/elasticbeanstalk/Boost-Prod/var/log/web.stdout.log")
