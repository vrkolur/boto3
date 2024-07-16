import boto3

cloudwatch = boto3.client('cloudwatch')

alarm_name = 'lambda_error_alarm'
metric_name = 'lambda_demo_error_pattern'  
namespace = 'filter_demo'  
statistic = 'Sum'  
threshold = 10000
period = 1800 
evaluation_periods = 1  
comparison_operator = 'GreaterThanThreshold'
state_value = 'OK'

response = cloudwatch.put_metric_alarm(
    AlarmName=alarm_name,
    MetricName=metric_name,
    Namespace=namespace,
    Statistic=statistic,
    StateValue = state_value,
    Period=period,
    EvaluationPeriods=evaluation_periods,
    Threshold=threshold,
    ComparisonOperator=comparison_operator,
    TreatMissingData='notBreaching'
)

# get the response
print(response)

