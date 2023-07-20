# %%

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# %%
# Create the Directed graphs G1 and G2
G1 = nx.DiGraph()
G2 = nx.DiGraph()

# Add nodes
G1.add_nodes_from([1, 2, 3, 4])
G2.add_nodes_from([1, 2, 3, 4])

# %%
### G1 ###############################################
G1.add_edges_from([(1, 2), (2, 3), (3, 4)])
G1_attrs_edges = {(1, 2): {"property": 'P3'}, (2, 3): {"property": 'P4'}, (3, 4):{"property": 'P5'}}
nx.set_edge_attributes(G1, G1_attrs_edges)
G1_attrs_nodes = {1: {"entity": 'E39'}, 2: {"entity": 'E55'}, 3:{"entity": 'E2'}, 4:{"entity": 'E7'}}
nx.set_node_attributes(G1, G1_attrs_nodes)

# %%
p = nx.spring_layout(G1)
G1_labels_nodes = nx.get_node_attributes(G1, 'entity')
G1_labels_edges = nx.get_edge_attributes(G1, 'property')
nx.draw(G1, pos=p, labels = G1_labels_nodes, with_labels = True)
nx.draw_networkx_edge_labels(G1, pos=p, edge_labels = G1_labels_edges)

# %%

### G2 ########################################################
G2.add_edges_from([(1, 2), (2, 3), (4, 3)])
G2_attrs_edges = {(1, 2): {"property": 'P3'}, (2, 3): {"property": 'P1'}, (4, 3):{"property": 'P5'}}
nx.set_edge_attributes(G2, G2_attrs_edges)
G2_attrs_nodes = {1: {"entity": 'E39'}, 2: {"entity": 'E55'}, 3:{"entity": 'E2'}, 4:{"entity": 'E7'}}
nx.set_node_attributes(G2, G2_attrs_nodes)

# %%
# p = nx.spring_layout(G2)
G2_labels_nodes = nx.get_node_attributes(G2, 'entity')
G2_labels_edges = nx.get_edge_attributes(G2, 'property')
nx.draw(G2, pos=p, labels = G2_labels_nodes, with_labels = True)
nx.draw_networkx_edge_labels(G2, pos=p, edge_labels = G2_labels_edges)

# %%
# store
lg = []
lg.append(G1)
lg.append(G2)
lg_out = []

for i in lg:
	df_edges = nx.to_pandas_edgelist(i)
	df_nodes = []
	for a,b in i.nodes(data = True):
		df_nodes.append(
			{
				'id': a,
				'entity': b['entity']
			}
		)
	df_nodes=pd.DataFrame(df_nodes)
	# map
	id_to_entity = dict(zip(df_nodes['id'], df_nodes['entity']))
	df_subgraph = df_edges
	df_subgraph['source'] = df_edges['source'].map(id_to_entity)
	df_subgraph['target'] = df_edges['target'].map(id_to_entity)
	lg_out.append(df_subgraph)

# %%
# print Markdown views
df_G1 = lg_out[0]
df_G2 = lg_out[1]

print(df_G1.to_markdown())
print(df_G2.to_markdown())


# %%
# common row(s)

identical_rows = df_G1.merge(df_G2, on=list(df_G1.columns), how='inner', indicator=True)
df_G1xG2 = identical_rows[identical_rows['_merge'] == 'both'].drop(columns=['_merge'])

print(df_G1xG2.to_markdown())