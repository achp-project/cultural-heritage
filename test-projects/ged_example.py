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
# Calculate the number of common edges between G1 and G2
common_edges = set(G1.edges()).intersection(G2.edges())
print(common_edges)
num_common_edges = len(common_edges)
print("Number of common edges:", num_common_edges)
# %%
