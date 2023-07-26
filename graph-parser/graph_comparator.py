import argparse
import pathlib
import os
import itertools as it
from pprint import pprint

from graph_parser import process_graph_file, extract_graph_structures


def validate_parameters(parameters: argparse.Namespace) -> argparse.Namespace:
    """
    Validate the input CLI parameters, discriminate data source and generate necessary output dir tree.

    :param parameters: argparse Namespace containing the parsed parameters.
    :return: Namespace updated for potential alternate data sources
    """

    # Check input files
    for in_file in parameters.input_files:
        if not os.path.isfile(in_file) or in_file.suffix != '.json':
            raise Exception(f"Invalid input Graph file provided with value {in_file}")

    return parameters


# TODO Add proper help messages and usage examples
parser = argparse.ArgumentParser()
# List of input files, will be ignored if remote URL is provided in the following parameter
parser.add_argument('input_files', nargs='+', type=pathlib.Path, help='local input graph files')

# Parse input to match with specs
args = parser.parse_args()
# Validate parameters in terms of remote priority as well as local file and dirtree existence
args = validate_parameters(args)

# Generate a data dictionary with one entry per file, indexed by their actual name
file_data_batch = {in_file: process_graph_file(in_file) for in_file in args.input_files}

minimal_subgraph_batch = {}

# Process the input data to extract the relevant graph data
for in_file_path, in_file_data in file_data_batch.items():

    print(f"\n\n{in_file_path}\n")

    minimal_subgraphs = []

    root_node_id, nodes, node_dict, edges = extract_graph_structures(in_file_data)

    indexed_nodes = {n['nodeid']: n for n in nodes}

    for e in edges:
        domain_node = indexed_nodes[e['domainnode_id']]['ontologyclass'].split('/')[-1:][0]
        ontology_property = e['ontologyproperty'].split('/')[-1:][0]
        range_node = indexed_nodes[e['rangenode_id']]['ontologyclass'].split('/')[-1:][0]

        minimal_subgraphs.append((domain_node, ontology_property, range_node))

    pprint(minimal_subgraphs)

    minimal_subgraph_batch[str(in_file_path)] = minimal_subgraphs

    for g1, g2 in it.combinations(list(minimal_subgraph_batch.keys()), 2):
        print(f"\n\n{g1} in common with {g2}\n")
        g1_edge_set = set(minimal_subgraph_batch[g1])
        g2_edge_set = set(minimal_subgraph_batch[g2])
        common_edge_set = set.intersection(g1_edge_set, g2_edge_set)
        pprint(common_edge_set)
exit(0)