import re
import json

input_file_path = 'hodor_request_2.txt'

with open(input_file_path, 'r') as file:
    log_entries = file.read()

entries = log_entries.split('\n')

# Extract information after "query received"
output_entries = []
output_entries.append("[")
for entry in entries:
    if "query received" in entry:
        # Use regular expression to extract relevant information
        match = re.search(r'query received\s+(.*)', entry)
        if match:
            query_data = json.loads(match.group(1))
            #query_data['query']['count'] = 9999
            # try:
            #     #print(query_data['query']['filters']['componentFilters_1']['component_filters'][0]['group'])
            #     query_data['query']['filters']['componentFilters_1']['component_filters'][0]['group'] = 2
            #     del query_data['query']["filters"]["componentFilters_2"]
            # except Exception as e:
            #     pass
            stdata = json.dumps(query_data)
            output_entries.append(stdata+",")

output_entries[-1] = output_entries[-1][:-1]
output_entries.append("]")
# Write output back to the same file
with open('hodor_request_json_2.json', 'w') as file:
    file.write('\n'.join(output_entries))
