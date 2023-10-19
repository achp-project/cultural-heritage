
# %%
import os
import requests
import json
import pandas as pd
import numpy as np
import re
import copy

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
# recover wikidata spatial regions from EAMENA regions, the smallest wikidata geographical unit is 'country'
# tested on: region = 'Algeria'; region = 'MENA'; region = 'Levant/Arabia/Mesopotamia'
       
def get_wikidata(region):
	# print(region)
	if re.search(r"/", region):
		# If "/" exists, it means the region is a conpound of smaller regions
		region = re.split(r"/", region)
	else:
		region = list([region])
	df_region = pd.DataFrame(columns=['id', 'label'])
	for reg in range(0, len(region)):
		a_reg = region[reg]
		region_id = df_wiki_region.loc[df_wiki_region['region'] == a_reg, 'wikidata'].values
		region_id = region_id.flatten().tolist()
		region_label = df_wiki_region.loc[df_wiki_region['region'] == a_reg, 'country']
		region_label = region_label.tolist()
		unit_id = df_wiki_region.loc[df_wiki_region['unit'] == a_reg, 'wikidata'].values
		unit_id = unit_id.flatten().tolist()
		unit_label = df_wiki_region.loc[df_wiki_region['unit'] == a_reg, 'country']
		unit_label = unit_label.tolist()
		country_id = df_wiki_region.loc[df_wiki_region['country'] == a_reg, 'wikidata'].values    
		country_id = country_id.flatten().tolist()                 
		country_label = df_wiki_region.loc[df_wiki_region['country'] == a_reg, 'country']
		country_label = country_label.tolist()
		df_wiki = pd.DataFrame(
			{'id': region_id + unit_id + country_id,
			'label': region_label + unit_label + country_label
			})
		# print(df_wiki.to_markdown())
		df_region = pd.concat([df_region, df_wiki], axis=0)
	# drop dupliactes
	df_region = df_region.drop_duplicates()
	# convert to dict
	dict_region = df_region.to_dict(orient='records')
	return(dict_region) # return a list of dictionaries
# region = 'Levant/Arabia/Mesopotamia'
# adict = get_wikidata(region)



# %%
# Read the broader and Arabic labels

boader_cultural_periods_url = "https://raw.githubusercontent.com/achp-project/cultural-heritage/main/periodo-projects/rdm-bu-period-levels.tsv"
boader_cultural_periods = pd.read_csv(boader_cultural_periods_url, sep='\t')
# print(boader_cultural_periods.to_markdown())
# get main columns indices
level1_en = boader_cultural_periods.columns.get_loc("level1-en")
level1_ar = boader_cultural_periods.columns.get_loc("level1-ar")
level2_en = boader_cultural_periods.columns.get_loc("level2-en")
level2_ar = boader_cultural_periods.columns.get_loc("level2-ar")
level3_en = boader_cultural_periods.columns.get_loc("level3-en")
level3_ar = boader_cultural_periods.columns.get_loc("level3-ar")
# `boader_cultural_periods` file
# create an accessible structure to retrieve the data by coordinates
d = dict(zip(boader_cultural_periods.columns, range(len(boader_cultural_periods.columns))))
s = boader_cultural_periods.rename(columns=d).stack()

# create the JSON looping over cultural periods
df_broader = pd.DataFrame(columns=['file_pp', 'genid_new_name', 'culture_region'])

# len(df_cultural_periods)
rg = (60,80)
rg = (60,61)
rg = (210,212)
# rg[0], rg[1]

for i in range(len(df_cultural_periods)):
	# one copy each loop, to create 1 file
	# i = 1
	json_periodo = copy.deepcopy(template_periodo)
	uuid = df_cultural_periods.iloc[i]['ea.uuid']
	culture_region = df_cultural_periods.iloc[i]['ea.name']
	print(" - " + str(i) + " '" + culture_region + "'")
	region = re.findall(r'\((.*?)\)', culture_region)[0]
	# print(region)
	culture = re.sub(r'\([^)]*\)', '', culture_region).strip()
	# print(culture)
	start = df_cultural_periods.iloc[i]['ea.duration.taq']
	stop = df_cultural_periods.iloc[i]['ea.duration.tpq']
	# replace values
	# change keys
	genid_template = "https://client.perio.do/.well-known/genid/eamena-period-1"
	genid_new_name = "eamena-period-" + str(i)
	genid_new = "https://client.perio.do/.well-known/genid/" + genid_new_name
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
	# - localizedLabels - en
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]["localizedLabels"]['en'] = [culture]
	# - localizedLabels - ar
	cell_loc = (s == culture_region).idxmax() # the opposite: boader_cultural_periods.iloc[cell_loc[0]][cell_loc[1]]
	# print(cell_loc)
	if cell_loc == (0,0):
		print("/!\ The period '%s' hasn't be found in 'rdm-bu-period-levels.tsv'" % culture_region)
	if cell_loc[1] == level3_en:
		# same row, different column
		arabicPeriod = boader_cultural_periods.iloc[cell_loc[0]][level3_ar]
		arabicPeriod = re.sub(r'\([^)]*\)', '', arabicPeriod).strip()
		# arabicPeriod = arabicPeriod.encode("utf-8").decode("utf-8")
		# print(arabicPeriod)
		# arabicPeriod = arabicPeriod.encode(encoding = 'UTF-8')
		# lang_ar = {"ar": [arabicPeriod]}
		json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]["localizedLabels"]['ar'] = [arabicPeriod]
	if cell_loc[1] == level2_en:
		# same row, different column
		arabicPeriod = boader_cultural_periods.iloc[cell_loc[0]][level2_ar]
		arabicPeriod = re.sub(r'\([^)]*\)', '', arabicPeriod).strip()
		# arabicPeriod = arabicPeriod.encode("utf-8").decode("utf-8")
		# print(arabicPeriod)
		# arabicPeriod = arabicPeriod.encode(encoding = 'UTF-8')
		json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]["localizedLabels"]['ar'] = [arabicPeriod]
		# skip broader category which is too generic
	# print(arabicPeriod)
	# - spatialCoverageDescription
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['spatialCoverageDescription'] = region
	# - spatialCoverage
	# call get_wikidata()
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['spatialCoverage'][0] = get_wikidata(region)
	# - start - early
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['start']['in']['earliestYear'] = start
	# - start - early
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['start']['in']['latestYear'] = start
	# - start - label
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['start']['label'] = str(start)
	# - stop - early
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['stop']['in']['earliestYear'] = stop
	# - stop - early
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['stop']['in']['latestYear'] = stop
	# - stop - label
	json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['stop']['label'] = str(stop)
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
	filename = filename.replace('[', ' ').replace(']', '')
	filename = filename.replace(',', '')
	filename = filename.replace('/', '_')
	filename = filename.replace(' ', '_')
	filename = filename.replace('__', '_')
	filename = filename.replace('-', '_')
	# for c in ["/", " ", "_", "-", "__"]:
	# 	filename = filename.replace(c, "_" + c)
	filename = filename.lower()
	file_pp = "eamena_" + filename + ".json"
	file_path = os.getcwd() + "\\exports\\" + file_pp
	# save
	json_string = json.dumps(json_periodo, cls=NpEncoder)
	json_string = json.loads(json_string)
	# create the JSON file
	with open(file_path, 'w', encoding='utf8') as json_file:
		# beware of the encoding, see: https://stackoverflow.com/questions/18337407/saving-utf-8-texts-with-json-dumps-as-utf-8-not-as-a-u-escape-sequence
		json.dump(json_string, json_file, indent=4, ensure_ascii=False)
		print(file_pp + " has been exported")
	# store the 'genid_new' and 'culture_region' in a dataframe for broader addition
	df_broader.loc[i] = [file_pp, genid_new_name, culture_region]

# %%

df_broader
# broaderPeriod = 'Chalcolithic (Mesopotamia)'
# genid_new_name_broader = df_broader['genid_new_name'][df_broader.index[df_broader['culture_region']== broaderPeriod].tolist()[0]]

# %%
# TODO: add broader periods using `df_broader`

# loop through `df_broader` rows to re-open JSON files one by one
# for index, row in df_broader.iterrows():
for index in range(len(df_cultural_periods)):
	# index = 0 ; culture_region = "Chalcolithic (Levant)"
	# index = 60 ; culture_region = "Chalcolithic, Late 4 (Northern Mesopotamia)"
	culture_region = df_broader.loc[index]['culture_region']
	genid_new_name = df_broader.loc[index]['genid_new_name']
	file_pp = df_broader.loc[index]['file_pp']
	# df_broader.loc[index]['file_pp']
	file_path = os.getcwd() + "\\exports\\" + file_pp
	print(str(index) + " read: " + file_path)
	# student_details = json.loads(file_path)[0]
	# file_path = os.getcwd() + "\\exports\\" + "eamena_classical_pre-islamic_levant_mesopotamia_iran_northern_arabia.json"
	with open(file_path) as f:
		periodo_period = json.load(f)
	# print(periodo_period)
	# get the location of the value in x,y (row, column)
	cell_loc = (s == culture_region).idxmax() # the opposite: boader_cultural_periods.iloc[cell_loc[0]][cell_loc[1]]
	# print(cell_loc)
	# will only consider the broader of level3 periods (that is to say level2), indeed level2 broader periods are level1 and are too much generic (Chalcolithic, Palaelithic, etc.) and do not exist in cultural_periods.tsv, so only existing in EAMENA has place holders
	if cell_loc == (0,0):
		print("level1")
		print("The period %s hasn't be found in 'rdm-bu-period-levels.tsv'" % culture_region)
	if cell_loc[1] == level2_en:
		print("level2")
	if cell_loc[1] == level3_en:
		print("level3")
		# same row, different column
		broaderPeriod = boader_cultural_periods.iloc[cell_loc[0]][level2_en]
		genid_broader = df_broader['genid_new_name'][df_broader.index[df_broader['culture_region']== broaderPeriod].tolist()[0]]
		genid_broader = "https://client.perio.do/.well-known/genid/" + genid_broader
		genid_new_name = "https://client.perio.do/.well-known/genid/" + genid_new_name
		# - broader
		# will add the new record at the correct place
		# subset the dict
		mykeys = list(periodo_period['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new_name].keys())
		mydict = periodo_period['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new_name]
		# insert a key and a value
		pos = list(mydict.keys()).index('languageTag')
		items = list(mydict.items())
		items.insert(pos + 1, ('broader', genid_broader))
		mydict = dict(items)
		# print(mydict)
		# mykeys.insert(mykeys.index('languageTag')+1, 'broader')
		# mydict['broader'] = genid_broader
		# add the updated dict to the main record
		periodo_period['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new_name] = mydict
		# json_periodo['authorities']['https://client.perio.do/.well-known/genid/eamena-authority']['periods'][genid_new]['broader'] = genid_broader
		print("'" + culture_region + "' broader period '", broaderPeriod, "' has been added")
	# TODO: overwrite the JSON
	# pretty_json = json.dumps(json_periodo, indent=4)
	# print(pretty_json)
	json_string = json.dumps(json_periodo, cls=NpEncoder)
	json_string = json.loads(json_string)
	# create the JSON file
	with open(file_path, 'w', encoding='utf8') as json_file:
		# beware of the encoding, see: https://stackoverflow.com/questions/18337407/saving-utf-8-texts-with-json-dumps-as-utf-8-not-as-a-u-escape-sequence
		json.dump(json_string, json_file, indent=4, ensure_ascii=False)
		print(file_pp + " has been exported")

# %%
mydict = {"ar": ""}
ar = "العصر الحجري القديم"
mydict["ar"] = ar
mydict

# %%
