# %%

import os
from os.path import isfile, join
import pandas as pd
import json
import requests

## Read a TSV, use the style to update GeoJSON file. For example, embed a logo in a popup for the function projects_extent()

# map folder
outDir = os.getcwd() + '\\prj-extent\\'
inDir = 'https://raw.githubusercontent.com/achp-project/cultural-heritage/main/map-projects/prj-extent/'
# reference list
github_tsv_url = 'https://raw.githubusercontent.com/achp-project/cultural-heritage/main/list.tsv'
df = pd.read_csv(github_tsv_url, sep='\t')
# 
for index, row in df.iterrows():
	name = row['name']
	inFile = inDir + row['map']
	outFile = outDir + row['map']
	print(inFile)
	# add values
	logo = "<img src='" + row['inst-logo'] + "' style='height:50px;'>"
	# logo = row['inst-logo']
	# map = maps_path + row['map']
	color = row['color']
	response = requests.get(inFile)
	extent = json.loads(response.text)
	# extent = json.loads(aFile)
	extent["features"][0]["properties"]['logo'] = logo
	extent["features"][0]["properties"]['color'] = color
	with open(outFile, "w") as outfile:
		json.dump(extent, outfile)
# %%
