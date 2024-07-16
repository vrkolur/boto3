import boto3

cloudwatch = boto3.client('cloudwatch')
lambda_client = boto3.client('lambda')

# get the ARN of the lambda function
lambda_function_name = 'list-log-group-names'
lambda_response = lambda_client.get_function(FunctionName=lambda_function_name)
lambda_arn = lambda_response['Configuration']['FunctionArn']

# Put your arn here
notification_arn = 'arn:aws:sns:us-east-1:126263378245:Alarm_status'

alarm_name = 'lambda_error_alarm'
metric_name = 'lambda_demo_error_pattern'
namespace = 'filter_demo'
statistic = 'Sum'
threshold = 14
period = 60
evaluation_periods = 1
comparison_operator = 'GreaterThanThreshold'

response = cloudwatch.put_metric_alarm(
    AlarmName=alarm_name,
    MetricName=metric_name,
    Namespace=namespace,
    Statistic=statistic,
    Period=period,
    EvaluationPeriods=evaluation_periods,
    Threshold=threshold,
    ComparisonOperator=comparison_operator,
    TreatMissingData='notBreaching',
    AlarmActions=[lambda_arn, notification_arn],
    AlarmDescription='Alarm to monitor Lambda errors and invoke a function',
    OKActions=[notification_arn]
)

print(response)

