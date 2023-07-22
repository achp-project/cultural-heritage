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
# Plot G1
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
# Plot G2 with the same layout
G2_labels_nodes = nx.get_node_attributes(G2, 'entity')
G2_labels_edges = nx.get_edge_attributes(G2, 'property')
nx.draw(G2, pos=p, labels = G2_labels_nodes, with_labels = True)
nx.draw_networkx_edge_labels(G2, pos=p, edge_labels = G2_labels_edges)

# %%
# store
lg = []
dn = list()
ct = 0
for i in [G1, G2]:
	ct = ct + 1
	df_edges = nx.to_pandas_edgelist(i)
	df_nodes = []
	for a,b in i.nodes(data = True):
		df_nodes.append(
			{
				'node_id': a,
				'entity': b['entity']
			}
		)
	df_nodes=pd.DataFrame(df_nodes)
	# map
	id_to_entity = dict(zip(df_nodes['node_id'], df_nodes['entity']))
	df_subgraph = df_edges
	df_subgraph['source'] = df_edges['source'].map(id_to_entity)
	df_subgraph['target'] = df_edges['target'].map(id_to_entity)
	lg.append(df_subgraph)
	# keep the list of id nodes
	df_nodes['G'] = str(ct)
	dn.append(df_nodes)

df_G1 = lg[0]
df_G2 = lg[1]
dn_all = pd.concat([dn[0], dn[1]])
# clean
dn_all = dn_all.reset_index()
dn_all = dn_all.drop('index', axis = 1)


# %%
# print Markdown tables views

print(df_G1.to_markdown())
print("\n")
print(df_G2.to_markdown())


# %%
# find different and common row(s)

df_G1xG2 = df_G1.merge(df_G2, how='outer', indicator=True)
df_G1_only = df_G1xG2[df_G1xG2['_merge'] == 'left_only']
df_G2_only = df_G1xG2[df_G1xG2['_merge'] == 'right_only']
df_G_both = df_G1xG2[df_G1xG2['_merge'] == 'both']

print(df_G_both)


# %%
# nodes with create 'match' column
dn_all_match = dn_all 
dn_all_match['match'] = dn_all_match["entity"] + '_' + dn_all_match["G"]
# add new node_id for the merge
dn_all_match['id'] = range(len(dn_all_match))
dn_all_match['id'] = dn_all_match['id']+1
dn_all_match = dn_all_match.drop(['entity', 'G'], axis = 1)

print(dn_all_match)

# %%
# edges, assign name of source graph, ids

df_G1_only = df_G1_only.assign(weight=1)
df_G2_only = df_G2_only.assign(weight=1)
df_G_both = df_G_both.assign(weight=2) # weight of two when shared
df_all = pd.concat([df_G1_only, df_G2_only, df_G_both])

df_all_match = df_all

# replace left_only and right_only with graph ids, raname
df_all_match['_merge'] = df_all_match['_merge'].replace(['left_only'], "1")
df_all_match['_merge'] = df_all_match['_merge'].replace(['right_only'], "2")
df_all_match = df_all_match.rename(columns={'_merge': 'G'})

df_all_match['G'] = df_all_match["G"].astype("str")
df_all_match['source_id'] = df_all_match["source"] + '_' + df_all_match["G"]
df_all_match['target_id'] = df_all_match["target"] + '_' + df_all_match["G"]

df_all_match = df_all_match.drop(['G'], axis = 1)


print(df_all_match)

# %%
# split 'both' between 1 and 2

rows_to_duplicate = df_all_match[df_all_match['source_id'].str.contains('_both') | df_all_match['target_id'].str.contains('_both')]

# find indices of 'both' rows 
idx_both = df_all_match.index[df_all_match['source_id'].str.contains('_both') | df_all_match['target_id'].str.contains('_both')].tolist()
df_all_both = df_all_match
# remove rows with 'both'
# df_all_both = df_all_both.drop(idx_both)
for both in idx_both:
	# both = 0
	df_both_1 = df_all_both.loc[[both]]
	# src = df_both_1.iloc[0]['source_id']
	df_both_1['source_id'] = df_both_1.iloc[0]['source_id'].replace('both', '1')
	df_both_1['target_id'] = df_both_1.iloc[0]['target_id'].replace('both', '1')
	# df_both_1['source_id'] = df_both_1['source_id'].replace(['_both'], "_1")
	# df_both_1['target_id'] = df_both_1['target_id'].str.replace(['both'], "1")
	df_both_2 = df_all_both.loc[[both]]
	df_both_2['source_id'] = df_both_2.iloc[0]['source_id'].replace('both', '2')
	df_both_2['target_id'] = df_both_2.iloc[0]['target_id'].replace('both', '2')
	# df_both_2['source_id'] = df_both_2['source_id'].replace(['both'], "2")
	# df_both_2['target_id'] = df_both_2['target_id'].replace(['both'], "2")
	df_all_both = pd.concat([df_all_both, df_both_1], ignore_index=True)
	df_all_both = pd.concat([df_all_both, df_both_2], ignore_index=True)

# remove rows with 'both' patterns
idx_both = df_all_both.index[df_all_both['source_id'].str.contains('_both') | df_all_both['target_id'].str.contains('_both')].tolist()
df_all_both = df_all_both.drop(idx_both)

print(df_all_both)

# duplicated_df = pd.concat([df_all_match, pd.DataFrame([rows_to_duplicate])], ignore_index=True)
# duplicated_df = pd.concat([df_all_match, rows_to_duplicate], ignore_index=True)



# print(rows_to_duplicate)

# duplicates = duplicated_df.duplicated(keep=False)
# duplicated_df.loc[duplicates, 'duplicate_tag'] = duplicated_df.groupby(['source_id', 'target_id']).cumcount() + 1
# duplicated_df['duplicate_tag'].fillna(0, inplace=True)


# print(duplicated_df)


# %%
df_merged_source = df_all_match.merge(dn_all_match, right_on=['match'], left_on=['source_id'])
df_merged_source = df_merged_source.rename(columns={'id': 'id_source'})
df_merged = df_merged_source.merge(dn_all_match, right_on=['match'], left_on=['target_id'])
df_merged = df_merged.rename(columns={'id': 'id_target'})

print(df_merged)

# %%

# load with attributes
G = nx.from_pandas_edgelist(df_merged, 'id_source', 'id_target', True, create_using=nx.DiGraph())
for i in G.nodes():
     G.nodes[i]['entity'] = dn_all[dn_all['id']==i]['entity'].item()

G_labels_nodes = nx.get_node_attributes(G, 'entity')
G_labels_edges = nx.get_edge_attributes(G, 'property')
nx.draw(G, pos=p, labels = G_labels_nodes, with_labels = True)
nx.draw_networkx_edge_labels(G, pos=p, edge_labels = G_labels_edges)

# TODO: add common `df_G_both`