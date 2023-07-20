# %%

import networkx as nx
import matplotlib.pyplot as plt

# %%
# Create the Directed graphs G1 and G2
G1 = nx.DiGraph()
G2 = nx.DiGraph()

# Add nodes
G1.add_nodes_from([1, 2, 3, 4])
G2.add_nodes_from([1, 2, 3, 4])

# %%
#### Add edges and edges properties
### G1
G1.add_edges_from([(1, 2), (2, 3), (3, 4)])
## attributes
# edges
G1_attrs_edges = {(0, 1): {"property": 'is identified by'}, (1, 2): {"property": 'was influenced by'}, (2, 3): {"property": 'has note'}, (3, 4):{"property": 'has time-span'}}
nx.set_edge_attributes(G1, G1_attrs_edges)
# nodes
G1_attrs_nodes = {1: {"entity": 'E39 Actors'}, 2: {"entity": 'E55 Types'}, 3:{"entity": 'E2 Temporal Entities'}, 4:{"entity": 'E7 Activity'}}
nx.set_node_attributes(G1, G1_attrs_nodes)
# G1.node[1]['entity'] = 'E39 Actors'
# G1.node[2]['entity'] = 'E55 Types'
# G1.node[3]['entity'] = 'E2 Temporal Entities'
# G1.node[4]['entity'] = 'E53 Places'

# %%
p = nx.spring_layout(G1)
G1_labels_nodes = nx.get_node_attributes(G1, 'entity')
G1_labels_edges = nx.get_edge_attributes(G1, 'property')
nx.draw(G1, pos=p, labels = G1_labels_nodes, with_labels = True)
nx.draw_networkx_edge_labels(G1, pos=p, edge_labels = G1_labels_edges)

# %%

### G2
G2.add_edges_from([(1, 2), (2, 3), (4, 3)])
## attributes
# edges
attrs_edges_G2 = {(0, 1): {"property": 'consists of'}, (2, 3): {"property": 'has note'}, (4, 3):{"property": 'has time-span'}}
nx.set_edge_attributes(G1, attrs_edges_G2)
# nodes

attrsG1 = {(0, 1): {"property": 20}, (2, 3): {"property": 3}, (3, 4):{"property": 3}}


# %%
# Calculate the number of common edges between G1 and G2
common_edges = set(G1.edges()).intersection(G2.edges())
print(common_edges)
num_common_edges = len(common_edges)
print("Number of common edges:", num_common_edges)
# %%
