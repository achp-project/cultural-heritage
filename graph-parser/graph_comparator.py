import argparse
import json
import csv
import pathlib
import os
import itertools as it
import sys

import pandas as pd

# Import required methods from the original Arches graph parser
from graph_parser import process_graph_file, extract_graph_structures


# This is a simple serializer that encodes sets as lists
# By jterrace and Akaisteph7 from https://stackoverflow.com/questions/8230315/how-to-json-serialize-sets
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def compare_graphs(g1_data: dict, g2_data: dict) -> dict:
    # Create new structure to store comparison data
    comparison_results = {}

    # If cms is present in both graphs, create an entry and join the instances
    for cms_key in g1_data.keys():
        if cms_key in g2_data.keys():
            cms_comparison_data: dict = {
                'instances': g1_data[cms_key]['instances'] + g2_data[cms_key]['instances']
            }
            comparison_results[cms_key] = cms_comparison_data

    return comparison_results


def validate_parameters(parameters: argparse.Namespace) -> argparse.Namespace:
    """
    Validate the input CLI parameters, discriminate data source and generate necessary output dir tree.

    :param parameters: argparse Namespace containing the parsed parameters.
    :return: Namespace with validated parameters
    """

    # Check input files
    for in_file in parameters.input_files:
        if not os.path.isfile(in_file) or in_file.suffix != '.json':
            raise Exception(f"Invalid input Graph file provided with value {in_file}")

    return parameters


def get_comparison_data(input_graph_urls: list) -> (dict, dict):
    # Generate a data dictionary with one entry per file, indexed by their actual name
    file_data_batch = {in_file: process_graph_file(in_file) for in_file in input_graph_urls}

    # Create a structure to store all the results and the relevant metadata
    results: dict = {}
    graph_metadata = {}

    # Create a substructure to store the triples
    results['minimal_subgraph_data'] = {}

    # Process the input data to extract the relevant graph data
    for in_file_path, in_file_data in file_data_batch.items():

        root_node_id, nodes, node_dict, edges, graph_id = extract_graph_structures(in_file_data)

        indexed_nodes = {n['nodeid']: n for n in nodes}

        minimal_subgraphs = {}

        for e in edges:
            # Store the CIDOC parent class
            domain_node = indexed_nodes[e['domainnode_id']]['ontologyclass'].split('/')[-1:][0]
            # Store the CIDOC relation class
            ontology_property = e['ontologyproperty'].split('/')[-1:][0]
            # Store the CIDOC child class
            range_node = indexed_nodes[e['rangenode_id']]['ontologyclass'].split('/')[-1:][0]
            # Generate a unique hash for this CMS
            key_string = f"{domain_node}${ontology_property}${range_node}"

            # If CMD is present, increase instances amount, storing the node and graph ids
            if key_string in minimal_subgraphs.keys():
                minimal_subgraphs[key_string]['instances'].append((e['domainnode_id'], e['rangenode_id'], e['graph_id']))

            # If CMN is not present, create new entry with relevant data
            else:

                minimal_subgraph_metrics = {
                    # Store the cms type (redundant with key)
                    'cms': (domain_node, ontology_property, range_node),
                    # Store the ids of the participating nodes and graph
                    'instances': [(e['domainnode_id'], e['rangenode_id'], e['graph_id'])]
                }
                # Add to the cms index
                minimal_subgraphs[key_string] = minimal_subgraph_metrics
        # Get the graph name
        graph_name = str(in_file_path.name.replace('.json', ''))
        # Add to the global graph index
        results['minimal_subgraph_data'][graph_name] = minimal_subgraphs
        # Add relevant graph_metadata
        graph_metadata[graph_name] = {
            'graph_id': graph_id,
            'indexed_nodes': indexed_nodes
        }

    # Create an iterator containing all permutations of graphs to compare
    graph_pair_permutations = it.combinations(list(results['minimal_subgraph_data'].keys()), 2)

    # Create an empty data structure to store the comparisons
    comparison_results = {}

    # Iterate through the permutations and gather data
    for g1, g2 in graph_pair_permutations:
        partial_comparison_results = compare_graphs(results['minimal_subgraph_data'][g1],
                                            results['minimal_subgraph_data'][g2])
        # Store the results in an indexed structure
        comparison_results[f"{g1}${g2}"] = partial_comparison_results

    return comparison_results, graph_metadata


def get_comparison_results_dataframe(comparison_results: dict, graph_metadata) -> str:
    data_source = []
    for (graph_name, gcd) in comparison_results.items():
        (g1_name, g2_name) = graph_name.split('$')

        g1_uuid = graph_metadata[g1_name]['graph_id']
        g2_uuid = graph_metadata[g2_name]['graph_id']

        for (comparison_item_name, comparison_item) in gcd.items():
            (source_property, target_proerty, relation_type) = comparison_item_name.split('$')

            for instance in comparison_item['instances']:
                graph_name = g1_name if instance[2] == g1_uuid else g2_name
                indexed_nodes = graph_metadata[graph_name]['indexed_nodes']

                data_source.append({
                    'source_property': source_property,
                    'target_property': target_proerty,
                    'relation_type': relation_type,
                    'graph_id': instance[2],
                    'source_id': instance[0],
                    'target_id': instance[1],
                    'graph_name': graph_name,
                    'source_name': indexed_nodes[instance[0]],
                    'target_name': indexed_nodes[instance[1]]
                })

    df = pd.read_json(json.dumps(data_source))
    return df.to_csv()


def main():
    # TODO Add proper help messages and usage examples
    parser = argparse.ArgumentParser()
    # List of input files, and an optional output file
    parser.add_argument('input_files', nargs='+', type=pathlib.Path, help='local input graph files')
    parser.add_argument('-d', action='store_true')
    parser.add_argument('-o', nargs='?', type=argparse.FileType('w'), default=sys.stdout)


    # Parse input to match with specs
    args = parser.parse_args()
    # Validate parameters in terms of remote priority as well as local file and dirtree existence
    args = validate_parameters(args)
    # Get the comparison metrics
    comparison_results, graph_metadata = get_comparison_data(args.input_files)
    # Check if the output is a dataframe
    if args.d:
        out_data = get_comparison_results_dataframe(comparison_results, graph_metadata)
    else:
        out_data = json.dumps(comparison_results, cls=SetEncoder, indent=2)
    # Output the results as JSON
    args.o.write(out_data)


if __name__ == "__main__":
    main()
