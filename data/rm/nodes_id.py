

# %%
# load packages

import os
import requests
import json
import pandas as pd
import re

# %%
url = "https://raw.githubusercontent.com/achp-project/prj-eamena-marea/main/resource_models/Heritage%20Place.json"

# %%
pattern = r'achp-project/(.*?)/main'
project = re.search(pattern, url)
project_name = project.group(1) + "-rm-nodes.tsv"

response = requests.get(url)
graph_data = json.loads(response.text)
root_node_id = graph_data['graph'][0]['root']['nodeid']
# Create an empty DataFrame
df_nodes = pd.DataFrame(columns=['rm_node_name', 'rm_node_uuid'])  


# %%
for i in range(1, len(graph_data['graph'][0]['nodes'])):
    # new_row = {
    #     'rm_node_name': graph_data['graph'][0]['nodes'][i]['name'],
    #     'rm_node_uuid': graph_data['graph'][0]['nodes'][i]['nodeid']
    # }
    new_row = [graph_data['graph'][0]['nodes'][i]['name'], graph_data['graph'][0]['nodes'][i]['nodeid']]
    print(i)
    print(new_row)
    df_nodes.loc[i] = new_row
    # df_nodes = df_nodes.append(new_row, ignore_index=True)

outDir = os.path.dirname(os.path.realpath(__file__))
file_path = outDir + project_name
df_nodes.to_csv(file_path, sep='\t', index=False)

# len(graph_data['graph'][0]['cards'])

# %%
len(graph_data['graph'][0]['nodes'])
graph_data['graph'][0]['nodes'][0]['name']

# %%
url = "https://raw.githubusercontent.com/achp-project/prj-eamena-marea/main/resource_models/Heritage%20Place.json"
# Define a regular expression pattern to match the desired substring




# %%
print(graph_data['graph'][0]['nodes'][1]['nodeid'])

# %%
