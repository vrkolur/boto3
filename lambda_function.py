import json
import logging
# from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # logger.info(f"Event payload: {json.dumps(event)}")
    logger.info(f"Previous State is: {event['alarmData']['previousState']['value']}")

    logger.info(f"Alarm Name is: {event['alarmData']['alarmName']}")

    return {
        'statusCode': 200,
        'body': 'Lambda function executed successfully.'
    }
#  event['alarmData']['previousState']['value']