

# %%
import requests
import json
import pandas as pd
import re

# %%
url = "https://raw.githubusercontent.com/achp-project/prj-eamena-marea/main/resource_models/Heritage%20Place.json"
response = requests.get(url)
graph_data = json.loads(response.text)
root_node_id = graph_data['graph'][0]['root']['nodeid']
print(root_node_id)

# Create an empty DataFrame
df_nodes = pd.DataFrame(columns=['rm_node_name', 'rm_node_uuid'])  


# %%
for i in range(1, len(graph_data['graph'][0]['nodes'])):
    new_row = {
        'rm_node_name': graph_data['graph'][0]['nodes'][i]['name'],
        'rm_node_uuid': graph_data['graph'][0]['cards'][i]['nodeid']
    }
    df_nodes = df_nodes.append(new_row, ignore_index=True)

file_path = 'your_file.tsv'
df_nodes.to_csv(file_path, sep='\t', index=False)

# len(graph_data['graph'][0]['cards'])

# %%
len(graph_data['graph'][0]['nodes'])
graph_data['graph'][0]['nodes'][0]['name']

# %%
url = "https://raw.githubusercontent.com/achp-project/prj-eamena-marea/main/resource_models/Heritage%20Place.json"
# Define a regular expression pattern to match the desired substring
pattern = r'achp-project/(.*?)/main'

# Use re.search() to find the match
project = re.search(pattern, url)

if project:
    # Extract the captured group (the part between "achp-project/" and "/main")
    result = project.group(1)
    print(result)
else:
    print("Pattern not found in the URL")

# %%
