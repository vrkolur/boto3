import json
data = {
    "source": "aws.cloudwatch",
    "alarmArn": "arn:aws:cloudwatch:us-east-1:126263378245:alarm:lambda_error_alarm",
    "accountId": "126263378245",
    "time": "2024-07-25T07:22:32.389+0000",
    "region": "us-east-1",
    "alarmData": {
        "alarmName": "lambda_error_alarm",
        "state": {
            "value": "ALARM",
            "reason": "Thresholds Crossed: 1 out of the last 1 datapoints [239.0 (25/07/24 07:21:00)] was greater than the upper thresholds [225.71426732099445] (minimum 1 datapoint for OK -> ALARM transition).",
            "reasonData": "{\"version\":\"1.0\",\"queryDate\":\"2024-07-25T07:22:32.386+0000\",\"startDate\":\"2024-07-25T07:21:00.000+0000\",\"period\":60,\"recentDatapoints\":[239.0],\"recentUpperThresholds\":[225.71426732099445],\"evaluatedDatapoints\":[{\"timestamp\":\"2024-07-25T07:21:00.000+0000\",\"value\":239.0,\"threshold\":225.71426732099445}]}",
            "timestamp": "2024-07-25T07:22:32.389+0000"
        },
        "previousState": {
            "value": "OK",
            "reason": "Thresholds Crossed: 1 out of the last 1 datapoints [209.0 (25/07/24 06:59:00)] was not greater than the upper thresholds [330.3191408914422] (minimum 1 datapoint for ALARM -> OK transition).",
            "reasonData": "{\"version\":\"1.0\",\"queryDate\":\"2024-07-25T07:00:44.734+0000\",\"startDate\":\"2024-07-25T06:59:00.000+0000\",\"period\":60,\"recentDatapoints\":[209.0],\"recentUpperThresholds\":[330.3191408914422],\"evaluatedDatapoints\":[{\"timestamp\":\"2024-07-25T06:59:00.000+0000\",\"value\":209.0,\"threshold\":330.3191408914422}]}",
            "timestamp": "2024-07-25T07:00:44.738+0000"
        },
        "configuration": {
            "description": "Alarm to monitor Lambda errors and invoke a function",
            "metrics": [
                {
                    "id": "m1",
                    "metricStat": {
                        "metric": {
                            "namespace": "filter_demo",
                            "name": "lambda_demo_error_pattern",
                            "dimensions": {}
                        },
                        "period": 60,
                        "stat": "Sum"
                    },
                    "returnData": True
                },
                {
                    "id": "e1",
                    "expression": "ANOMALY_DETECTION_BAND(m1, 0.5)",
                    "label": "Expression1",
                    "returnData": True
                }
            ]
        }
        
    }
}
# import json

# # Assuming 'event' is the variable containing the JSON event data
# event_data = json.loads(data)

# # Access the 'alarmData' dictionary
# alarm_data = event_data.get('alarmData', {})

# # Access the 'previousState' dictionary
# previous_state = alarm_data.get('previousState', {})

# # Extract the 'startDate' value from 'previousState'
# start_date = previous_state.get('startDate')

# if start_date:
#     print(f"Start Date: {start_date}")
# else:
#     print("'startDate' not found in 'previousState'")

import datetime

event_data = data["alarmData"]

alarm_data = event_data["previousState"]
reason_data_str = alarm_data["reasonData"]
reason_json = json.loads(reason_data_str)
res = reason_json['startDate']

print(res)
date_str = '2024-07-25T06:59:00.000+0000'
date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
epoch_time_seconds = date_obj.timestamp()
epoch_time_milliseconds = int(epoch_time_seconds * 1000)

print(f"Epoch time in milliseconds: {epoch_time_milliseconds}")



import time

# Get the current time in seconds since the epoch
current_epoch_time_seconds = time.time()

# Convert seconds to milliseconds
current_epoch_time_milliseconds = int(current_epoch_time_seconds * 1000)

print(f"Current time in milliseconds since the epoch: {current_epoch_time_milliseconds}")

