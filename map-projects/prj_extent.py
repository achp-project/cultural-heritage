# %%

import os
from os.path import isfile, join
import pandas as pd
import json
import requests

## Read the TSV: https://github.com/achp-project/cultural-heritage/blob/main/list.tsv. Use the style to update GeoJSON file. For example, embed a logo in a popup for the function projects_extent()

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
	logo = "<img src='" + row['inst-logo'] + "' style='height:30px;'>"
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

# Try to create a GeoJSON file for MAHS project: https://maritimeasiaheritage.cseas.kyoto-u.ac.jp/country/indonesia/
import geopandas as gpd
from wikitables import import_tables

def get_wikidata_id(country_name):
    # Retrieve Wikidata ID for a given country
    tables = import_tables(f"List of administrative divisions of {country_name}")
    wikidata_id = None
    for table in tables:
        for row in table.rows:
            if "wikidata" in row.values():
                wikidata_id = row["wikidata"].value.strip()
                break
    return wikidata_id

def get_country_boundary(wikidata_id):
    # Retrieve country boundary from Wikidata
    query = f"""
    SELECT ?geometry WHERE {{
      wd:{wikidata_id} wdt:P3896 ?geometry.
    }}
    """
    url = f"https://query.wikidata.org/sparql?query={query}&format=geojson"
    gdf = gpd.read_file(url)
    return gdf

# List of countries
countries = ["Maldives", "Indonesia", "Vietnam"]

# Create GeoJSON file
for country in countries:
    wikidata_id = get_wikidata_id(country)
    if wikidata_id:
        boundary_gdf = get_country_boundary(wikidata_id)
        boundary_gdf.to_file(f"{country}_boundary.geojson", driver="GeoJSON")
        print(f"{country} boundary GeoJSON file created.")
    else:
        print(f"Could not retrieve Wikidata ID for {country}.")

# Export the combined GeoDataFrame to a GeoJSON file
import os
print(os.getcwd())
combined_gdf.to_file("combined_boundaries.geojson", driver="GeoJSON")
print("Combined GeoJSON file created.")
# %%
