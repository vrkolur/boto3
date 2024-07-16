import boto3

client = boto3.client('cloudwatch')

alarm_name = 'lambda_error_alarm'
alarm_type = 'MetricAlarm'

response = client.describe_alarms(
    AlarmNames=[alarm_name],
    AlarmTypes=[alarm_type]
)


if response['MetricAlarms']:
    alarm = response['MetricAlarms'][0]
    print(f"Alarm Name: {alarm['AlarmName']}")
    print(f"Metric Name: {alarm['MetricName']}")
    print(f"Namespace: {alarm['Namespace']}")
    print(f"Statistic: {alarm['Statistic']}")
    print(f"Period: {alarm['Period']} seconds")
    print(f"Evaluation Periods: {alarm['EvaluationPeriods']}")
    print(f"Threshold: {alarm['Threshold']}")
    print(f"Comparison Operator: {alarm['ComparisonOperator']}")
    print(f"Alarm State: {alarm['StateValue']}")
else:
    print(f"No alarm found with name '{alarm_name}' and type '{alarm_type}'")
