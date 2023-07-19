import networkx as nx
import matplotlib.pyplot as plt

# %%
# Create the graphs G1 and G2
G1 = nx.DiGraph()
G2 = nx.DiGraph()

# Add nodes
G1.add_nodes_from([1, 2, 3, 4])
G2.add_nodes_from([1, 2, 3, 4])

#### Add edges and edges propertyues
### G1
G1.add_edges_from([(1, 2), (2, 3), (3, 4)])
## attributes
# edges
attrs_edges_G1 = {(0, 1): {"property": 'is identified by'}, (2, 3): {"property": 3}, (3, 4):{"property": 3}}
nx.set_edge_attributes(G1, attrs_edges_G1)
# nodes
G1.node[1]['entity'] = 'E39 Actors'
G1.node[2]['entity'] = 'E55 Types'
G1.node[3]['entity'] = 'E2 Temporal Entities'
G1.node[4]['entity'] = 'E53 Places'

### G2
G2.add_edges_from([(1, 2), (2, 3), (4, 3)])
## attributes
# edges
attrs_edges_G2 = {(0, 1): {"property": 5}, (2, 3): {"property": 3}, (4, 3):{"property": 3}}
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
