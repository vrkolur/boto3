import json
import logging
from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Event payload: {json.dumps(event)}")

    if event.get('source') == 'aws.cloudwatch':
        alarm_name = event['detail']['alarmName']
        alarm_state = event['detail']['state']['value']
        logger.info(f"CloudWatch alarm '{alarm_name}' is in state '{alarm_state}'")
        print()

        try:
            previous_state_time = event['detail']['stateUpdatedTimestamp'] - timedelta(hours=4)
            previous_state = event['detail']['oldStateValue']
            logger.info(f"CloudWatch alarm '{alarm_name}' was in state '{previous_state}' at {previous_state_time.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            logger.error(f"Error retrieving previous state: {str(e)}")

    return {
        'statusCode': 200,
        'body': 'Lambda function executed successfully.'
    }
