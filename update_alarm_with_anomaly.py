import boto3
import os

cloudwatch = boto3.client('cloudwatch')

def put_metric_alarm(alarm_name, metric_namespace, metric_name, statistic, dimensions, band_width, evaluation_periods, datapoints_to_alarm, period):
    # Define the metric math expression
    metric_math_expression = f"ANOMALY_DETECTION_BAND(METRICS('{metric_namespace}', '{metric_name}', '{statistic}', {dimensions}), {band_width})"

    # Set the alarm parameters
    alarm_params = {
        'AlarmName': alarm_name,
        'MetricName': metric_math_expression,
        'Namespace': metric_namespace,
        'Statistic': 'Maximum',
        'EvaluationPeriods': evaluation_periods,
        'DatapointsToAlarm': datapoints_to_alarm,
        'TreatMissingData': 'notBreaching',
        'Threshold': 31,
        'ComparisonOperator': 'GreaterThanThreshold',
        'Period': period
    }

    # Create or update the alarm
    try:
        response = cloudwatch.put_metric_alarm(**alarm_params)
        print(f"Alarm '{alarm_name}' created or updated successfully.")
        return response
    except Exception as e:
        print(f"Error creating or updating alarm '{alarm_name}': {e}")
        return None

# Define the alarm parameters
alarm_name = 'lambda-error-alarm'
metric_namespace = 'filter_demo'
metric_name = 'lambda_demo_error_pattern'
statistic = 'Sum'
dimensions = {}
band_width = 1.5  # Updated band width
evaluation_periods = 1
datapoints_to_alarm = 1
period = 120  # 2 minutes

# Create or update the alarm
put_metric_alarm(alarm_name, metric_namespace, metric_name, statistic, dimensions, band_width, evaluation_periods, datapoints_to_alarm, period)
