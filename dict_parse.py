# dict = [[{'field': 'id', 'value': '2157239302'}, {'field': '@ptr', 'value': 'CpkBClgKRDM1NjU1OTg3MzY5MTovYXdzL2VsYXN0aWNiZWFuc3RhbGsvQm9vc3QtUHJvZC92YXIvbG9nL3dlYi5zdGRvdXQubG9nEAAiDgiAwPjpgzIQmPCRk4QyEjkaGAIGY2AkbQAAAAUheFItAAZnc0swAAAF0iABKN2sl42EMjDY3JuNhDI48ARAieI5SPPGAVCXwwEYACABENsEGAE='}], [{'field': 'id', 'value': '2157234182'}, {'field': '@ptr', 'value': 'CpkBClgKRDM1NjU1OTg3MzY5MTovYXdzL2VsYXN0aWNiZWFuc3RhbGsvQm9vc3QtUHJvZC92YXIvbG9nL3dlYi5zdGRvdXQubG9nEAAiDgiAwPjpgzIQmPCRk4QyEjkaGAIGY2AkbQAAAAUheFItAAZnc0swAAAF0iABKN2sl42EMjDY3JuNhDI48ARAieI5SPPGAVCXwwEYACABEKkEGAE='}]]

# print(dict[1][0]['value'])

# from prettytable import PrettyTable


# dict = [[{'field': 'id', 'value': '2157239302'}, {'field': 'count(*)', 'value': '6'}], [{'field': 'id', 'value': '2157234182'}, {'field': 'count(*)', 'value': '6'}], [{'field': 'id', 'value': '2157228038'}, {'field': 'count(*)', 'value': '6'}], [{'field': 'id', 'value': '2157220870'}, {'field': 'count(*)', 'value': '6'}], [{'field': 'id', 'value': '2157215238'}, {'field': 'count(*)', 'value': '6'}]]

# # print(f"guid: {dict[0][0]['value']}")

# table = PrettyTable()
# table.field_names = ['guid','count']

# for i in range(0,len(dict)):
#     table.add_row([dict[i][0]['value'],dict[i][1]['value']])

# print(table)


# sha = [[{'field': 'guid', 'value': '2157424646","transmission_status_code":"transmission_failed","status_message":"Error while invoking benefits admin api","error_details":"403 Forbidden - Different HttpStatusCodeException","ldex_transmission_response":""}}'}, {'field': 'count(*)', 'value': '3'}]]

# test_data = sha[0][0]['value']
# # print(test_data[:10])
# if (int)(sha[0][1]['value']) >=2:
#     print(sha[0][1]['value'])


# from datetime import datetime

# now = datetime.now()

# formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

# print(formatted_time)

# str = "adedae3"

# print(str[-2])

# import json

# def lambda_handler(event, context):
#     # Assuming the response from the function is stored in the variable 'response'
#     # and it contains a list of alarm names
#     response = [
#         'alarm_name_1',
#         'alarm_name_2',
#         'alarm_name_3',
#         # Add more alarm names here
#     ]

#     # Create a dictionary with a single key 'alarmNames' and the list of alarm names as the value
#     alarm_names_dict = {'alarmNames': response}

#     # Convert the dictionary to a JSON string
#     alarm_names_json = json.dumps(alarm_names_dict)

#     # Print the JSON string
#     print(alarm_names_json)

#     return {
#         'statusCode': 200,
#         'body': alarm_names_json
#     }

data = {
    "source": "aws.cloudwatch",
    "alarmArn": "arn:aws:cloudwatch:us-east-1:126263378245:alarm:lambda_error_alarm",
    "accountId": "126263378245",
    "time": "2024-07-16T13:14:42.817+0000",
    "region": "us-east-1",
    "alarmData": {
        "alarmName": "lambda_error_alarm",
        "state": {
            "value": "ALARM",
            "reason": "Threshold Crossed: 1 out of the last 1 datapoints [1051.0 (16/07/24 13:13:00)] was greater than the threshold (12.0) (minimum 1 datapoint for OK -> ALARM transition).",
            "reasonData": "{\"version\":\"1.0\",\"queryDate\":\"2024-07-16T13:14:42.817+0000\",\"startDate\":\"2024-07-16T13:13:00.000+0000\",\"statistic\":\"Sum\",\"period\":60,\"recentDatapoints\":[1051.0],\"threshold\":12.0,\"evaluatedDatapoints\":[{\"timestamp\":\"2024-07-16T13:13:00.000+0000\",\"sampleCount\":1051.0,\"value\":1051.0}]}",
            "timestamp": "2024-07-16T13:14:42.817+0000"
        },
        "previousState": {
            "value": "OK",
            "reason": "Threshold Crossed: 1 out of the last 1 datapoints [132.0 (16/07/24 13:10:00)] was not greater than the threshold (40000.0) (minimum 1 datapoint for ALARM -> OK transition).",
            "reasonData": "{\"version\":\"1.0\",\"queryDate\":\"2024-07-16T13:11:18.715+0000\",\"startDate\":\"2024-07-16T13:10:00.000+0000\",\"statistic\":\"Sum\",\"period\":60,\"recentDatapoints\":[132.0],\"threshold\":40000.0,\"evaluatedDatapoints\":[{\"timestamp\":\"2024-07-16T13:10:00.000+0000\",\"sampleCount\":132.0,\"value\":132.0}]}",
            "timestamp": "2024-07-16T13:11:18.717+0000"
        },
        "configuration": {
            "metrics": [
                {
                    "id": "24c85dd6-abfa-5881-7a0a-ab671e64deb8",
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
                }
            ]
        }
    }
}

# print(data["alarmData"]["state"]["reasonData"])

import json

            
event_data = data["alarmData"]

reason_data_str = event_data["state"]["reasonData"]

reason_data = json.loads(reason_data_str)

recent_datapoints = reason_data["recentDatapoints"]
# print(reason_data)


# print(recent_datapoints[0])  



