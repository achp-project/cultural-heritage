#%%

# this chunk is a direct copy from 'graph_comparator.py'

import os
import sys
import json
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

current = os.path.dirname(os.path.realpath(__file__))
graph_parser = os.path.dirname(current)+"/graph-parser"
sys.path.append(graph_parser)

from graph_parser import extract_graph_structures, process_graph_file
from graph_comparator import get_comparison_data

resource_models = [
	graph_parser + "/sourceGraphData/MAPHSA/MAPHSA Heritage Item.json",
	graph_parser + "/sourceGraphData/EAMENA/EAMENA Heritage Place.json",
]

input_files: list = [Path(r) for r in resource_models]
result_data = get_comparison_data(input_files)

#%% Gather input file URLs

from test_graph_comparator import print_individual_minimal_subgraph_metrics

print_individual_minimal_subgraph_metrics(result_data)

# print(result_data['minimal_subgraph_data']['MAPHSA Heritage Item']['E53_Place$P140i_was_attributed_by$E16_Measurement']['cms'])

# print(len(result_data['minimal_subgraph_data']['MAPHSA Heritage Item']))

# print(result_data['minimal_subgraph_data']['MAPHSA Heritage Item'].keys())

# print(len(result_data['minimal_subgraph_data']['MAPHSA Heritage Item']['E53_Place$P140i_was_attributed_by$E16_Measurement']['instances']))

#%% 

df_both = pd.DataFrame(columns=['G', 'source', 'target', 'property', 'id_source', 'id_target', 'id_property'])

for k,v in result_data['minimal_subgraph_data']['MAPHSA Heritage Item'].items(): 
	# collect litterals
	s, p, o = k.split('$')
	for i in range(len(result_data['minimal_subgraph_data']['MAPHSA Heritage Item'][k]['instances'])):
        # print(result_data['minimal_subgraph_data']['MAPHSA Heritage Item'][k]['instances'][i][0] + result_data['minimal_subgraph_data']['MAPHSA Heritage Item'][k]['instances'][i][1] + result_data['minimal_subgraph_data']['MAPHSA Heritage Item'][k]['instances'][i][2])
		# collect UUIDs
		s1 = result_data['minimal_subgraph_data']['MAPHSA Heritage Item'][k]['instances'][i][0]
		p1 = result_data['minimal_subgraph_data']['MAPHSA Heritage Item'][k]['instances'][i][1]
		o1 = result_data['minimal_subgraph_data']['MAPHSA Heritage Item'][k]['instances'][i][2]
		# idx = len(df.index)+1
		df_both.loc[len(df_both.index)+1] = ['both', s, o, p, s1, o1, p1]

# print(df)

# colors
conditions = [
    (df_both['G'] == '1'),
    (df_both['G'] == '2')]
choices = ['red', 'green']
df_both['color'] = np.select(conditions, choices, default='black')

# weight
conditions = [
    (df_both['G'] == '1'),
    (df_both['G'] == '2')]
choices = [1, 1]
df_both['weight'] = np.select(conditions, choices, default=2)

# load with attributes
G = nx.from_pandas_edgelist(df_both, 'id_source', 'id_target', True, create_using=nx.DiGraph())

# nodes
df_node_source = pd.DataFrame({'entity':df_both['source'],
			       'id':df_both['id_source']})
df_node_target = pd.DataFrame({'entity':df_both['target'],
			       'id':df_both['id_target']})
dn_all = pd.concat([df_node_source, df_node_target])
dn_all = dn_all.drop_duplicates()
# dn_all
for i in G.nodes():
     G.nodes[i]['entity'] = dn_all[dn_all['id']==i]['entity']

edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]
weights = [G[u][v]['weight'] for u,v in edges]

nodes = G.nodes()

p = nx.spring_layout(G)
G_labels_nodes = nx.get_node_attributes(G, 'entity')
G_labels_edges = nx.get_edge_attributes(G, 'property')
nx.draw(G, pos=p, labels = G_labels_nodes, with_labels = True, edge_color=colors, width=weights)
nx.draw_networkx_edge_labels(G, pos=p, edge_labels = G_labels_edges)
plt.show()



     
# %%
