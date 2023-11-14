
def projects_extent(map_dir = '/content/cultural-heritage/map-projects/prj-extent/', width=1200, height=700):
	"""
	Plot GeoJSON project extents.

  	:param map_dir: folder with the GeoJSON extents

	:Example: 
	>> projects_extent()
	"""
	import os
	import folium
	import geopandas as gpd

	m = folium.Map(width=width, height=height)
	projects_geojson = [f for f in os.listdir(map_dir) if os.path.isfile(os.path.join(map_dir, f))]
	for prj in projects_geojson:

			def style_function(feature):
				# Extract color information from the GeoJSON feature properties
				color = feature['properties'].get('color', '#ff0000')  # Default to red if color is not present
				return {
            'fillColor': color,
            'color': 'black',
            'weight': 2,
            'fillOpacity': 0.5
			  }
			geojson_data = map_dir + prj
			geojson_layer = folium.GeoJson(
			  geojson_data,
        name='GeoJSON',
        style_function = style_function,
        highlight_function=lambda x: {
          'fillOpacity':1
        },
      )
			folium.features.GeoJsonPopup(fields=['description', 'url', 'logo'], 
                                aliases=['Project Name:', 'Project Website', 'Institution'],
                                labels=True, max_width=500, min_width=10).add_to(geojson_layer)
			geojson_layer.add_to(m)
			m.fit_bounds(m.get_bounds())
	return(m)

# ressource models
def rm_list():
	"""
	Return a dictionary of RMs

	Project names as keys and GitHub URL as values

	:Example: 
	>> remote_source_files = rm_list()
	"""
	remote_source_files = {
		"MAPSS": "https://raw.githubusercontent.com/achp-project/prj-mapss/main/pkg/graphs/Heritage%20Place%20(3).json",
		"MAHS": "https://raw.githubusercontent.com/achp-project/prj-mahs/main/Site.json",
		"MAHSA": "https://raw.githubusercontent.com/achp-project/prj-mahsa/main/resource-models/Heritage%20Location%20Resource%20Model.json",
		"MAEASAM": "https://raw.githubusercontent.com/achp-project/prj-maeasam/main/Site.json",
		"EAMENA": "https://raw.githubusercontent.com/achp-project/prj-eamena-marea/main/resource_models/Heritage%20Place.json",
	}
	return(remote_source_files)

def square_matrix(remote_source_files = None):
	"""
	Create a square matrix from a dictionary of RMs

	:Example: 
	>> remote_source_files = rm_list
	>> square_matrix(remote_source_files)
	"""
	import pandas as pd

	df = pd.DataFrame(0, index=remote_source_files.keys(), columns=remote_source_files.keys())
	for project, url in remote_source_files.items():
		connected_projects = [p for p in remote_source_files.keys() if p != project and p in url]
		df.loc[project, connected_projects] = 1
	print(df)

# check boxes
def generate_checkboxes_from_dict(input_dict):
	import ipywidgets as widgets

	"""
	Generate checkboxes from dict

	Check boxes
		
	:param input_dict: a dictionary of RMs

	:Example: 
	>> checkboxes_dict = generate_checkboxes_from_dict(remote_source_files)
	"""
	checkboxes = {key: widgets.Checkbox(description=key, value=False) for key in input_dict.keys()}
	return checkboxes

def get_and_print_checked_values(**kwargs):
	"""
	Get responses from a checkboxes widget

	Check boxes
     
    :param input_dict: a dictionary of RMs

	:Example: 
	>> checkboxes_dict = generate_checkboxes_from_dict(remote_source_files)
    >> interactive_widget = interactive(get_and_print_checked_values, **checkboxes_dict)
    >> display(interactive_widget)
	"""
	import ipywidgets as widgets

	checked_values = {key: value for key, value in kwargs.items() if isinstance(value, widgets.Checkbox) and value.value}
	return(checked_values)

# remote_source_files = rm_list()
# checkboxes_dict = generate_checkboxes_from_dict(remote_source_files)
# interactive_widget = interactive(get_and_print_checked_values, **checkboxes_dict)
# display(interactive_widget)

def rm_selected(checkboxes_dict, remote_source_files):
	"""
	Load RMs into the folder 'inputResourceModels/'

	Check boxes
     
    :param checkboxes_dict: checkboxes with answers
	:param remote_source_files: list of the RMs

	:Example: 
	>> rm_selected(checkboxes_dict, remote_source_files)
	"""
	import urllib.request

	selected_keys = []
	for key, checkbox in checkboxes_dict.items():
		if checkbox.value:
			selected_keys.append(key)
	print("Selected projects:", selected_keys)
	if len(selected_keys) < 2:
		print("Please select a minimum of two different JSON files")
	else:
		subset_remote_source_files = {}
		# Iterate through the selected keys and add corresponding key-value pairs to the subset dictionary
		for key in selected_keys:
			if key in remote_source_files:
				subset_remote_source_files[key] = remote_source_files[key]
		print("Selected RMs:", subset_remote_source_files)
	for (project_name, resource_model_url) in subset_remote_source_files.items():
		target_filename = f"{project_name}_{resource_model_url.split('/')[-1]}"
		# print(target_filename)
		urllib.request.urlretrieve(resource_model_url, filename=f"inputResourceModels/{target_filename}")

def rm_one_selected(project_name, remote_source_files):
	"""
	Load one RM into the folder 'inputResourceModels/'

     
  :param project_name: name of the project
	:param remote_source_files: list of the RMs

	:Example: 
	>> rm_one_selected('EAMENA', remote_source_files)
	"""
	import urllib.request

	target_filename = f"{project_name}_{remote_source_files[project_name].split('/')[-1]}"
	urllib.request.urlretrieve(remote_source_files[project_name], filename=f"inputResourceModels/{target_filename}")

def create_rm_graph(subgraph_metrics = 'subgraphMetrics.csv', rm_project = None, highlight_nodes = None, color_default = 'blue', color_highlight='red', color_fields = None):
  """
  Table for one RM. Return a networkx graph. Optional: highlight nodes (fields) listed in a list (UUIDs)
      
  :param subgraph_metrics: a CSV file
  :param rm_project: the name of one RM (ex. EAMENA)
  :param highlight_nodes: optional. A list of UUIDs
  :param color_fields: optional. A dataframe of node UUIDs with their color 

  :Example: 
  >> # create graph
  >> rm_graph = create_rm_graph(rm_project = 'EAMENA')
  >> rm_graph
  >> 
  >> # highlight nodes (fields), EAMENA example
  >> df_erms = erms_template()
  >> df_erms['Enhanced record minimum standard'] = df_erms['Enhanced record minimum standard'].str.contains(r'Yes', case = False, na = False, regex = True).astype(int)
  >> df_erms = df_erms.loc[df_erms['Enhanced record minimum standard'] == 1]
  >> in_erms = df_erms['uuid_sql'].tolist()
  >> rm_graph = create_rm_graph(rm_project = 'EAMENA', highlight_nodes = in_erms)
  >> rm_graph
  """
  import pandas as pd		
  import networkx as nx
  import re

  rm_graph = pd.read_csv(subgraph_metrics)
  rm_graph.rename(columns={'graph_name': 'G', 
                           'source_property': 'source_crm', 
                           'target_property': 'target_crm',
                           'relation_type': 'property'}, inplace=True)
  col_order = ['G', 'source_crm', 'target_crm', 'property', 'source_id', 'target_id', 'source_name', 'target_name']
  rm_graph = rm_graph[col_order]
  rm_graph['G'] = rm_graph['G'].apply(lambda x: x.split('_')[0])
  rm_graph = rm_graph.loc[rm_graph['G'] == rm_project]
  # Create a directed graph from the DataFrame
  G = nx.from_pandas_edgelist(rm_graph, 'source_id', 'target_id', edge_attr=['property'], create_using=nx.DiGraph())
  # Populate node attributes
  for _, row in rm_graph.iterrows():
      source = row['source_id']
      target = row['target_id']
      source_attributes = {key[len('source_'):]: row[key] for key in rm_graph.columns if key.startswith('source_')}
      target_attributes = {key[len('target_'):]: row[key] for key in rm_graph.columns if key.startswith('target_')}
      # Update or add node attributes
      if G.has_node(source):
          G.nodes[source].update(source_attributes)
      if G.has_node(target):
          G.nodes[target].update(target_attributes)
  ## nodes
  for n in G.nodes(data=True):
    n[1]['label'] = n[1]['name'] # will show names
    n[1]['title'] = re.sub(r'_', ' ', n[1]['crm'])
    # TODO: if the has no incoming edges it has a semantic Datatype
    # if G.in_degree(n[1]) == 0:
    #   n[1]['shape'] = 'square'
    #   n[1]['color'] = 'grey'
  ## node colors
  if color_fields is not None:
    for n in G.nodes(data=True):
      color_out = color_fields.loc[color_fields['uuid_sql'] == n[0], 'color']
      if len(color_out) > 0:
        color_out = color_out.iloc[0]
        n[1]['color'] = color_out
      else:
        n[1]['color'] = color_default
    # from highlight
  if type(highlight_nodes) == list:
    node_colors = {node: color_highlight if node in highlight_nodes else color_default for node in G.nodes}
    nx.set_node_attributes(G, values=node_colors, name='color')
  ## edges
  for e in G.edges(data=True):
    e[2]['title'] = re.sub(r'_', ' ', e[2]['property']) # replace _ by spaces
    # e[2]['title'] =  e[2]['label'] # popup labels: complete
    property_label = re.search(r'_(.*)', e[2]['property'])[1] # get text after P53_...
    property_label = re.sub(r'_', ' ', property_label) # replace _ by spaces
    e[2]['label'] = property_label # permanent labels (text)
    # print(e)
  return(G)

def plot_net_graph(G = None, show_buttons = False,   filename = "example.html", notebook = True, directed = True, cdn_resources = 'remote'):
	"""
	Load a pyvis netwokx graph in a HML layout that can be downloaded or plotted. Download using: `google.colab.files.download(filename)`, and plot s HTML using: `HTML(filename=filename)`
		
	:param G: a netwokx graph
	:param filename: the HTML output name

	:Example: 
	>> G = gm.create_rm_graph(rm_project= rm_project, color_fields = df_color)
	>> hp_G = gm.plot_net_graph(G, filename = filename)
	"""
	from pyvis import network as net
	from IPython.display import HTML

	g = net.Network(notebook = notebook, directed = directed, cdn_resources = cdn_resources)
	if show_buttons:
		g.show_buttons(filter_=["physics"])
	g.from_nx(G)
	g.save_graph(filename)
#   return HTML(filename=filename)


def subgraph_metrics(subgraph_metrics = 'subgraphMetrics.csv'):
	"""
	Table of subgraph metrics
     
    :param subgraph_metrics: a CSV file

	:Example: 
	>> subgraph_metrics = subgraph_metrics()
	>> subgraph_metrics
	"""
	import pandas as pd		

	subgraph_metrics = pd.read_csv(subgraph_metrics)
	col_order = ['G', 'source', 'target', 'property', 'source_id', 'target_id', 'source_name', 'target_name']
	subgraph_metrics.rename(columns={'graph_name': 'G', 
									'source_property': 'source', 
									'target_property': 'target',
									'relation_type': 'property'}, inplace=True)
	subgraph_metrics['source_id'] = subgraph_metrics['source'] + '_' + subgraph_metrics['G']
	subgraph_metrics['target_id'] = subgraph_metrics['target'] + '_' + subgraph_metrics['G']
	subgraph_metrics = subgraph_metrics[col_order]
	subgraph_metrics['G'] = subgraph_metrics['G'].apply(lambda x: x.split('_')[0])
	return subgraph_metrics

def comparison_metrics(comparison_metrics = 'comparisonMetrics.csv'):
	"""
	Table of comparison metrics
     
    :param comparison_metrics: a CSV file

	:Example: 
	>> comparison_metrics = comparison_metrics()
	>> comparison_metrics
	"""
	import pandas as pd	

	comparison_metrics = pd.read_csv(comparison_metrics)
	col_order = ['G', 'source', 'target', 'property', 'source_id', 'target_id'] # without source_name and target_name
	comparison_metrics.rename(columns={'graph_name': 'G',
									'source_property': 'source',
									'target_property': 'target',
									'relation_type': 'property'}, inplace=True)
	comparison_metrics['G'] = 'both' # comparison_metrics['graph_name_1'] + "_x_" + comparison_metrics['graph_name_2']
	comparison_metrics['source_id'] = comparison_metrics['source'] + '_' + comparison_metrics['G']
	comparison_metrics['target_id'] = comparison_metrics['target'] + '_' + comparison_metrics['G']
	comparison_metrics = comparison_metrics[col_order]
	return comparison_metrics

def all_match(subgraph_metrics, comparison_metrics):
	"""
	Merge subgraph and comparisons
     
    :param subgraph_metrics: Pandas dataframe of subgraphs
	:param comparison_metrics: Pandas dataframe of comparisons

	:Example: 
	>> df_all_match = all_match(subgraph_metrics, comparison_metrics)
	"""
	import pandas as pd

	df_all_match = pd.concat([subgraph_metrics, comparison_metrics])
	df_all_match = df_all_match.drop_duplicates()
	return(df_all_match)


def subgraph_comparison_merge(subgraph_metrics, comparison_metrics):
	"""
	Concatenation of subgraphs and comparison metrics and drops duplicates.Get subgraphs in both RM, and remove duplicated subgraphs
     
    :param subgraph_metrics: Pandas dataframe of subgraphs
	:param comparison_metrics: Pandas dataframe of comparisonss

	:Example: 
	>> df_all_complete = subgraph_comparison_merge(subgraph_metrics, comparison_metrics)
	"""
	import pandas as pd

	df_all_match = all_match(subgraph_metrics, comparison_metrics)
	df_all_match_copy = df_all_match.copy() # deep copy
	df_all_match_copy['uniq'] = df_all_match_copy['source'] + "_" + df_all_match_copy['property'] + df_all_match_copy['target'] # field with unique id
	# get 'both' rows in a separated df
	df_both = df_all_match_copy.loc[df_all_match_copy['G'] == 'both'] # both dataframe
	both_uniq = list(set(df_both['uniq'])) # get uniq ID in the 'both' dataframe
	df_all_match_copy = df_all_match_copy[~df_all_match_copy['uniq'].isin(both_uniq)] # drop both from the main dataframe
	df_all_complete = pd.concat([df_both, df_all_match_copy])
	return df_all_complete

def create_graph(rm, subgraph_metrics, comparison_metrics, edge_width = .2):
	"""
	Concatenation of subgraphs and comparison metrics and drops duplicates.Get subgraphs in both RM, and remove duplicated subgraphs
     
	:param rm: name of a RM
    :param subgraph_metrics: Pandas dataframe of subgraphs
	:param comparison_metrics: Pandas dataframe of comparisons
	:param edge_width: edge width for subgraphs (default: .2). The comparison edges will be the double.

	:return: A directed networkx graph

	:Example: 
	>> G = create_graph(rm, subgraph_metrics, comparison_metrics)
	"""
	import networkx as nx
	import re

	# filter on graph label
	# condition = df_all_match['G'] == rm
	# condition = df_all_match['G'] in rm
	# df_G = df_all_match[condition]
	subgraph_metrics['weight'] = edge_width
	comparison_metrics['weight'] = edge_width * 2
	# df_all_match = pd.concat([subgraph_metrics, comparison_metrics])
	df_all_match = all_match(subgraph_metrics, comparison_metrics)
	df_G = df_all_match[df_all_match.G.isin([rm])]
	G = nx.from_pandas_edgelist(df_G, 'source_id', 'target_id', True, create_using=nx.DiGraph())
	G_attrs_nodes = {}
	# clean
	rm_ = '_' + rm
	for i, node in enumerate(G.nodes()):
		a = re.sub(rm_, '', node)
		G_attrs_nodes[node] = {'entity': a, 'G': rm}
		nx.set_node_attributes(G, G_attrs_nodes)
	return G

def edges_labels(dict):
	import re

	newdict = {}
	for ed, value in dict.items():
		# short the name
		val = re.sub(r'_.*', '',  value)
		newdict[ed] = val
	return newdict

def nodes_labels(dict):
	import re

	newdict = {}
	for node, value in dict.items():
		# short the name
		val = re.sub(r'_.*', '',  value)
		newdict[node] = val
	return newdict

def plot_G(digraph, node_size = 200, node_color = "#add8e6", font_size = 10, edge_width = .2, fig_dim = 10):
	"""
	Plot a graph
		
	:param digraph: A directed networkx graph
	:param node_size: Node size
	:param node_color: Node color
	:param font_size: Node font size
	:param edge_width: Edge width for subgraphs (default: .2). The comparison edges will be the double.
	:param fig_dim: Figure dimensions

	:return: Plot a networkx graph

	:Example: 
	>> plot_G(G)
	"""
	import networkx as nx
	import matplotlib.pyplot as plt

	p = nx.circular_layout(digraph)
	labels_nodes = nx.get_node_attributes(digraph, 'entity')
	labels_nodes = nodes_labels(labels_nodes)
	labels_edges = nx.get_edge_attributes(digraph, 'property')
	labels_edges = edges_labels(labels_edges)
	plt.figure(figsize = (fig_dim + 6, fig_dim - 1))
	nx.draw(digraph, pos = p, labels = labels_nodes, with_labels = True, node_size = node_size, node_color = node_color, font_size = font_size, width = edge_width)
	nx.draw_networkx_edge_labels(digraph, pos = p, edge_labels = labels_edges, font_size = font_size)
	plt.show()

def plot_all_G(subgraph_metrics, comparison_metrics, node_size = 200, node_color = "#add8e6", font_size = 10, fig_dim = 10):
	"""
	Plot all the graphs separately
		
    :param subgraph_metrics: Pandas dataframe of subgraphs
	:param comparison_metrics: Pandas dataframe of comparisons
	:param node_size: Node size
	:param node_color: Node color
	:param font_size: Font size
	:param fig_dim: Figure dimensions

	:return: Plot several networkx graphs

	:Example: 
	>> plot_all_G(subgraph_metrics, comparison_metrics)
	"""
	df_all_match = all_match(subgraph_metrics, comparison_metrics)
	rms = df_all_match['G'].unique()
	rms = rms.tolist()
	for rm in rms:
		print(rm)
		G = create_graph(rm, subgraph_metrics, comparison_metrics)
		# graph_list.append(G)
		plot_G(G, node_size = node_size, node_color = node_color, font_size = font_size, fig_dim = fig_dim)

def all_nx_G(subgraph_metrics, comparison_metrics, colors = ['green', 'blue', 'red', 'yellow', 'purple']):
	"""
	Plot all the graphs separately 	# assign colors
		
    :param subgraph_metrics: Pandas dataframe of subgraphs
	:param comparison_metrics: Pandas dataframe of comparisons
	:param colors: List of colors. Only the first ones will be used.

	:return: A networkx graph

	:Example: 
	>> G = all_nx_G(subgraph_metrics, comparison_metrics)
	"""
	import pandas as pd
	import networkx as nx
	import re

	df_all_complete = subgraph_comparison_merge(subgraph_metrics, comparison_metrics)
	boths = df_all_complete['G'].unique().tolist()
	boths.remove('both') #?
	boths.append('both') #?
	# colors = ['green', 'blue', 'red', 'yellow', 'purple']
	# subset on number of graphs
	colors = colors[0:len(boths)-1]
	colors.append('black')
	df = pd.DataFrame(list(zip(boths, colors)),
				columns =['G', 'color'])
	df_all_complete = df_all_complete.merge(df, left_on='G', right_on='G')
	# load with attributes
	G = nx.from_pandas_edgelist(df_all_complete, 'source', 'target', True, create_using=nx.DiGraph())
	for i in G.nodes():
		G.nodes[i]['entity'] = re.sub(r'_.*', '',  i)
	return G

def plot_all_nx_G(G, node_size = 200, node_color = "#add8e6", font_size = 10, fig_dim = 10):
	"""
	Plot all the graphs separately 	# assign colors
		
    :param subgraph_metrics: Pandas dataframe of subgraphs
	:param comparison_metrics: Pandas dataframe of comparisons
	:param node_size: Node size
	:param node_color: Node color
	:param font_size: Font size
	:param fig_dim: Figure dimensions

	:return: Plot one networkx graph merging all graphs

	:Example: 
	>> G = all_nx_G(subgraph_metrics, comparison_metrics)
	>> plot_all_nx_G(G)
	"""
	import networkx as nx
	import matplotlib.pyplot as plt

	edges = G.edges()
	colors = list(nx.get_edge_attributes(G,'color').values())
	weights = list(nx.get_edge_attributes(G,'weight').values())
	p = nx.circular_layout(G)
	labels_nodes = nx.get_node_attributes(G, 'entity')
	labels_nodes = nodes_labels(labels_nodes)
	labels_edges = nx.get_edge_attributes(G, 'property')
	labels_edges = edges_labels(labels_edges)
	plt.figure(figsize = (fig_dim + 12, fig_dim + 2))
	nx.draw(G, pos=p, labels = labels_nodes, with_labels = True, node_size = node_size, node_color = node_color, font_size = font_size, edge_color=colors, width=weights)
	nx.draw_networkx_edge_labels(G, pos=p, edge_labels = labels_edges)
	plt.show()


# TODO: short node labels, node labels inside node shapes, label edges
def plot_all_pyvis_G(G, name = "pyvis-example", directed =True, notebook = True, cdn_resources='remote'):
	"""
	Plot an interactive pyvis graph
		
    :param G: Netwokx graph
	:param directed: If directed or not (default: True)
	:param notebook: If run in Jupyter Notebook (default: True)
	:param cdn_resources: If the upyter Notebook is hosted on a remote serevr (default: True)

	:return: Plot one pyvis graph merging all graphs

	:Example: 
	>> plot_all_pyvis_G(G, "pyvis-example")
	"""
	from pyvis import network as net
	from IPython.display import HTML

	g = net.Network(notebook = notebook, directed = directed, cdn_resources = cdn_resources)
	g.show_buttons(filter_=["physics"])
	g.from_nx(G)
	filename = f"{name}.html"
	g.save_graph(filename)
	return HTML(filename=filename)   
