
# %%
import os
import requests
import json
import pandas as pd
import numpy as np
import re
import copy

# %%
# needed to export as JSON
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

# %%
# load the PeriodO template
template_periodo_url = "https://gist.githubusercontent.com/rybesh/9f64c127ad8eeb69619896f22064bb0e/raw/5de8010b35512fafec65f2e015f036b2579b42e1/example-dataset.json"
response = requests.get(template_periodo_url)
template_periodo = response.json()
pretty_json = json.dumps(template_periodo, indent=4)
print(pretty_json)

# %%
# Read the cultural periods data

cultural_periods_url = "https://raw.githubusercontent.com/achp-project/cultural-heritage/main/periodo-projects/cultural_periods.tsv"
df_cultural_periods = pd.read_csv(cultural_periods_url, sep='\t')
print(df_cultural_periods.to_markdown())

# %%
# Read the wikidata data

wiki_region_url = "https://raw.githubusercontent.com/achp-project/cultural-heritage/main/periodo-projects/wikidata_period.tsv"
df_wiki_region = pd.read_csv(wiki_region_url, sep='\t')
print(df_wiki_region.to_markdown())

# %%
# create the JSON

# 10 first
for i in range(10):
	print(i)
	json_periodo = copy.deepcopy(template_periodo)
	uuid = df_cultural_periods.iloc[i]['ea.uuid']
	culture_region = df_cultural_periods.iloc[i]['ea.name']
	region = re.findall(r'\((.*?)\)', culture_region)[0]
	print(region)
	culture = re.sub(r'\([^)]*\)', '', culture_region).strip()
	print(culture)
	start = df_cultural_periods.iloc[i]['ea.duration.taq']
	stop = df_cultural_periods.iloc[i]['ea.duration.tpq']

	# replace values
	# change keys
	genid_template = "https://client.perio.do/.well-known/genid/eamena-period-1"
	genid_new = "https://client.perio.do/.well-known/genid/eamena-period-" + str(i)
	wikidata_id = df_wiki_region.loc[df_wiki_region['region'] == region, 'wikidata'].values[0]
	# replace 
	# - genid key
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new] = json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'].pop(genid_template)
	# - genid value
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]["id"] = genid_new
    # - locator
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]["source"]['locator'] = ''
	# - label
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['label'] = culture_region
	# - localizedLabels
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]["localizedLabels"]['en'] = [culture]
	# - spatialCoverageDescription
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['spatialCoverageDescription'] = ''
	# - spatialCoverage - id
	## wikidata id only if it is a single region unit (ie, no "/" in its name)
	if re.search(r"/", region):
		json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['spatialCoverage'][0]['id'] = ''
	else:
		json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['spatialCoverage'][0]['id'] = wikidata_id
	# - spatialCoverage - label
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['spatialCoverage'][0]['label'] = region
	# - start - early
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['start']['in']['earliestYear'] = start
	# - start - early
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['start']['in']['latestYear'] = start
	# - start - label
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['start']['label'] = ''
	# - stop - early
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['stop']['in']['earliestYear'] = stop
	# - stop - early
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['stop']['in']['latestYear'] = stop
	# - stop - label
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['stop']['label'] = ''
	# - note
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['note'] = ''
	# - editorialNote
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['editorialNote'] = ''
	# - citation
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['source']['citation'] = 'University of Oxford, University of Southampton. (2023). EAMENA Database. Retrieved from https://database.eamena.org (Accessed: 2023-10-01).'
	# - title
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['source']['title'] = 'EAMENA Database'
	# - url
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['source']['url'] = 'https://database.eamena.org/'
	# - yearPublished
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['source']['yearPublished'] = '2021'
	# - creators - name
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['source']['creators'][0]['name'] = 'University of Oxford, University of Southampton'
	# - locator
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['source']['locator'] = uuid
	# - editorialNote
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['editorialNote'] = "The locator '%s' is the UUID of the cultural period in EAMENA and can be accessed at 'https://database.eamena.org/concepts/%s' " % (uuid, uuid)
	filename = culture_region.replace('(', ' ').replace(')', '')
	# print(filename)
	filename = filename.replace('/', '_')
	filename = filename.replace(' ', '_')
	filename = filename.replace('__', '_')
	filename = filename.replace(',', '')
	filename = filename.lower()
	# print(filename)
	file_path = os.getcwd() + "\\exports\\eamena_" + filename + ".json"
	json_string = json.dumps(json_periodo, cls=NpEncoder)
	json_string = json.loads(json_string)
	with open(file_path, 'w') as json_file:
		json.dump(json_string, json_file, indent=4)
		print(file_path + " has been exported")
# %%
