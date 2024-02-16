#%%

import requests
import json
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, DC

infile = 'https://raw.githubusercontent.com/achp-project/prj-maeasam/main/Site.json'
outdir = "C:/Rprojects/achp-ch/graph-parser/temp.ttl"

#%%

# with open('/mnt/data/Site.json', 'r') as file:
#     json_data = json.load(file)

response = requests.get(infile)
data = response.json()

#%%
# Initialize an RDF graph
g = Graph()

# Define a namespace for our resources
NS = Namespace("http://www.cidoc-crm.org/cidoc-crm/")

# Function to add cards to the graph
def add_card_to_graph(g, card):
    card_uri = URIRef(NS[card["cardid"]])
    g.add((card_uri, RDF.type, NS.Card))
    g.add((card_uri, NS.active, Literal(card["active"])))
    g.add((card_uri, NS.component_id, Literal(card["component_id"])))
    # Add other properties as needed

    # Add constraints if present
    for constraint in card.get("constraints", []):
        constraint_uri = URIRef(NS[constraint["constraintid"]])
        g.add((constraint_uri, RDF.type, NS.Constraint))
        # Add constraint properties
        g.add((constraint_uri, NS.card_id, card_uri))
        # Add other properties as needed

# Iterate through the JSON data and add each card to the graph
for item in data["graph"]:
    for card in item.get("cards", []):
        add_card_to_graph(g, card)

# Serialize the graph to a Turtle file
g.serialize(destination=outdir, format="turtle")

# %%



# Assuming `nodes` is a list of dictionaries extracted from your JSON's "graph" key
nodes = data['graph'][0]['nodes'] # Replace this with the actual nodes data

# Initialize your graph
g = Graph()

# Define Namespaces
CIDOC_CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
MAEASAM = Namespace("http://maeasam#")
g.bind("cidoccrm", CIDOC_CRM)
g.bind("dc", DC)
g.bind("rdfs", RDFS)

for node in nodes:
    node_uri = MAEASAM[node['nodeid']]
    g.add((node_uri, RDF.type, RDFS.Class))
    g.add((node_uri, DC.title, Literal(node['name'])))
    g.add((node_uri, RDFS.subClassOf, CIDOC_CRM[node['ontologyclass']]))

# Serialize the graph to a file
g.serialize(destination=outdir, format='turtle')


# %%
