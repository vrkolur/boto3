def lambda_handler(event, context):
    # Your Lambda function code

    # Publish log message to SNS
    log_message = "This is a log message from Lambda"
    response = sns.publish(
        TopicArn='<YOUR_SNS_TOPIC_ARN>',
        Message=log_message
    )
    print(response)

    # Return a response
    return {
        'statusCode': 200,
        'body': 'Lambda function executed successfully'
    }
