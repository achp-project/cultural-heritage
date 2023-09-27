# tests on graph_comparator.py and graph_parser.py

import os
import sys
import json
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt

current = os.path.dirname(os.path.realpath(__file__))
graph_parser = os.path.dirname(current)+"/graph-parser"
sys.path.append(graph_parser)

# call of functions
from graph_parser import extract_graph_structures, process_graph_file
from graph_comparator import get_comparison_data


# Check individual graph ms metrics
def print_individual_minimal_subgraph_metrics(results: dict):


	for graph_name, graph_ms_metrics in results['minimal_subgraph_data'].items():

		# Sketchy way to get url for data, will fail with graphs that share name
		graph_url = [url for url in resource_models if graph_name in url][0]

		# Generate a data dictionary with one entry per file, indexed by their actual name
		in_file_data = process_graph_file(graph_url)
		root_node_id, nodes, node_dict, edges = extract_graph_structures(in_file_data)
		indexed_nodes = {n['nodeid']: n for n in nodes}

		print(f"Minimal Sugraph Stats for {graph_name}\n\n")

		# print the minimal subgraphs, crossing the data from the graph_comparator and graph_parser
		for ms_label, ms_metrics in graph_ms_metrics.items():
			(domain_node_class, relation_class, range_node_class) = ms_metrics['cms']
			print(f"\t[{len(ms_metrics['instances'])}] instance(s) of Minimal Subgraph for {domain_node_class} => {relation_class} => {range_node_class}\n")
			for (domain_node_id, range_node_id, graph_id) in ms_metrics['instances']:
				domain_node = indexed_nodes[domain_node_id]
				range_node = indexed_nodes[range_node_id]
				print(f"\t({domain_node_class}) {domain_node['name']} => {relation_class} => ({range_node_class}) {range_node['name']}")
			print()


# print the comparison of cms
def print_comparison_common_minimal_subgraph_metrics(results: dict):

	for comparison_label, comparison_data in results['graph_comparison_data'].items():
		# Another sketchy hack to get the graph names, using names with a slash will break things
		[graph_name1, graph_name2] = comparison_label.split('$')

		# Sketchy way to get url for data, will fail with graphs that share name
		graph_url1 = [url for url in resource_models if graph_name1 in url][0]
		graph_url2 = [url for url in resource_models if graph_name2 in url][0]

		# Get node data for both graphs being compared
		in_file_data_graph1 = process_graph_file(graph_url1)
		root_node_id_graph1, nodes_graph1, node_dict_graph1, edges_graph1 = extract_graph_structures(in_file_data_graph1)
		indexed_nodes_graph1 = {n['nodeid']: n for n in nodes_graph1}

		in_file_data_graph2 = process_graph_file(graph_url2)
		root_node_id_graph2, nodes_graph2, node_dict_graph2, edges_graph2 = extract_graph_structures(in_file_data_graph2)
		indexed_nodes_graph2 = {n['nodeid']: n for n in nodes_graph2}

		print(f"Common Minimal Sugraph Stats for {graph_name1} and {graph_name2}\n\n")

		# print the common minimal subgraphs, crossing the data from the graph_comparator and graph_parser
		for cms_label, cms_metrics in comparison_data.items():
			[domain_node_class, relation_class, range_node_class] = cms_label.split('$')
			print(
				f"\t[{len(cms_metrics['instances'])}] common instance(s) of Minimal Subgraph for {domain_node_class} => {relation_class} => {range_node_class}\n")
			for (domain_node_id, range_node_id, graph_id) in cms_metrics['instances']:

				# Determine if the instace of cms belongs to the first or second graph
				if domain_node_id in indexed_nodes_graph1:
					source_nodes = indexed_nodes_graph1
					graph_name = graph_name1
				else:
					source_nodes = indexed_nodes_graph2
					graph_name = graph_name2

				# Feth the node data from the graph_parser results
				domain_node = source_nodes[domain_node_id]
				range_node = source_nodes[range_node_id]
				# Verify all is good, and no Graphs with the same name are present
				assert domain_node['graph_id'] == graph_id
				assert range_node['graph_id'] == graph_id
				print(f"\t\t[{graph_name}]\t({domain_node_class}) {domain_node['name']} => {relation_class} => ({range_node_class}) {range_node['name']}")
			print()

# Resource model graphs to be loaded, the program supports as many as desired, although the output gets tricky to read
resource_models = [
	graph_parser + "/sourceGraphData/MAPHSA/MAPHSA Heritage Item.json",
	graph_parser + "/sourceGraphData/EAMENA/Heritage Place.json",
]

# Gather input file URLs
input_files: list = [Path(r) for r in resource_models]

# Run the graph comparator
result_data = get_comparison_data(input_files)

# Print individual graph metrics for ms
# print_individual_minimal_subgraph_metrics(result_data)

# Print the comparison of common minimal subgraphs
print_comparison_common_minimal_subgraph_metrics(result_data)