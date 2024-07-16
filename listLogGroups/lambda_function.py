import boto3

def lambda_handler(event, context):
    client = boto3.client('logs')
    
    try:
        response = client.describe_log_groups()
        log_groups = response['logGroups']
        
        log_groups_str = '\n'.join([f"{group['logGroupName']}"] for group in log_groups)
        
        return {
            'statusCode': 200,
            'body': f"Found {len(log_groups)} log groups:\n{log_groups_str}"
        }
    except Exception as e:
        print(e)