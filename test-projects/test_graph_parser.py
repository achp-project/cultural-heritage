# tests on graph_parser.py

import os
import sys
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt

current = os.path.dirname(os.path.realpath(__file__))
graph_parser = os.path.dirname(current)+"\graph-parser"
print(graph_parser)

sys.path.append(graph_parser)

# call of functions
from graph_parser import extract_graph_structures, process_graph_file

# MAPSHA
MAPHSA = "C:/Rprojects/achp-ch/graph-parser/sourceGraphData/MAPHSA/MAPHSA Heritage Item.json"
path_object = Path(MAPHSA)
MA=process_graph_file(MAPHSA)
root_node_id, nodes, node_dict, edges = extract_graph_structures(MA)
for n in nodes:
	cidoc_class_name = n['ontologyclass']
	cidoc_class_name = str(cidoc_class_name).split("/")[-1]
	n['graph_label'] = f"{cidoc_class_name} - {n['name']}"

for e in edges:
	e['graph_label'] = str(e['ontologyproperty']).split("/")[-1]

G = nx.Graph()

for node in nodes:
	G.add_node(node['nodeid'], data=node, label=node['graph_label'])

edge_label_properties = {}
for e in edges:
	G.add_edge(e['domainnode_id'], e['rangenode_id'], label=e['graph_label'])
	edge_label_properties[(e['domainnode_id'], e['rangenode_id'])] = e['graph_label']

node_labels = {n['nodeid']: n['graph_label'] for n in nodes}

p = nx.spring_layout(G)
nx.draw(G, pos=p, labels=node_labels)
nx.draw_networkx_edge_labels(G, pos=p, edge_labels=edge_label_properties)
plt.show()

# EAMENA
EAMENA = "C:/Rprojects/achp-ch/graph-parser/sourceGraphData/EAMENA/Heritage Place.json"
path_object = Path(EAMENA)
EA=process_graph_file(EAMENA)


