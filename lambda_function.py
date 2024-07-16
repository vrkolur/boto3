import json


def lambda_handler(event, context):

    num1 = int(event['num1'])
    num2 = int(event['num2'])

    result = num1 + num2
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'result': result
        })
    }
