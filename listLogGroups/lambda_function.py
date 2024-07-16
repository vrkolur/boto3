import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    logs_client = boto3.client('logs')

    try:
        response = logs_client.describe_log_groups()
        log_groups = response['logGroups']

        for log_group in log_groups:
            logger.info(log_group['logGroupName'])

        return {
            'statusCode': 200,
            'body': f"Listed {len(log_groups)} log groups."
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': 'An error occurred while listing log groups.'
        }
