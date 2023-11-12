# %%

import os
from os.path import isfile, join
import pandas as pd
import json
import requests

# map folder
extents = os.getcwd() + '\\prj-extent\\'
# reference list
github_tsv_url = 'https://raw.githubusercontent.com/achp-project/cultural-heritage/main/list.tsv'
df = pd.read_csv(github_tsv_url, sep='\t')
# 
for index, row in df.iterrows():
	name = row['name']
	aFile = extents + row['map']
	print(aFile)
	# add values
	logo = row['inst-logo']
	# map = maps_path + row['map']
	color = row['color']
	response = requests.get(aFile)
	extent = json.loads(response.text)
	extent["features"][0]["properties"]['logo'] = logo
	extent["features"][0]["properties"]['color'] = color
	with open(aFile, "w") as outfile:
		json.dump(extent, outfile)
# %%
