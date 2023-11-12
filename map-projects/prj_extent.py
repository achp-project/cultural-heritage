# append data to the GeoJSON project extents

import json
import requests
import geopandas as gpd


eamena = "https://raw.githubusercontent.com/achp-project/cultural-heritage/main/map-projects/prj-extent/eamena.geojson"

response = requests.get(eamena)

# with open(eamena) as f:
#     d = json.load(f)

gdf = gpd.read_file(response.text)

# Now you can work with the GeoDataFrame (e.g., visualize it)
print(gdf.head())