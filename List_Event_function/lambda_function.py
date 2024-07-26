import json
import logging

# Set up the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda function executed successfully!')
    }
