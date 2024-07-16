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


sha = [[{'field': 'guid', 'value': '2157424646","transmission_status_code":"transmission_failed","status_message":"Error while invoking benefits admin api","error_details":"403 Forbidden - Different HttpStatusCodeException","ldex_transmission_response":""}}'}, {'field': 'count(*)', 'value': '3'}]]

test_data = sha[0][0]['value']
# print(test_data[:10])
if (int)(sha[0][1]['value']) >=2:
    print(sha[0][1]['value'])


# from datetime import datetime

# now = datetime.now()

# formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

# print(formatted_time)

# str = "adedae3"

# print(str[-2])