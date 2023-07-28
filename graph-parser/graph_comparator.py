import argparse
import json
import pathlib
import os
import itertools as it
import sys

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


def get_comparison_data(input_graph_urls: list) -> dict:
    # Generate a data dictionary with one entry per file, indexed by their actual name
    file_data_batch = {in_file: process_graph_file(in_file) for in_file in input_graph_urls}

    # Create a structure to store all the results
    results: dict = {}

    # Create a substructure to store the triples
    results['minimal_subgraph_data'] = {}

    # Process the input data to extract the relevant graph data
    for in_file_path, in_file_data in file_data_batch.items():

        root_node_id, nodes, node_dict, edges = extract_graph_structures(in_file_data)

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
        # Add to the global graph index
        results['minimal_subgraph_data'][str(in_file_path.name.replace('.json', ''))] = minimal_subgraphs

    # Create an iterator containing all permutations of graphs to compare
    graph_pair_permutations = it.combinations(list(results['minimal_subgraph_data'].keys()), 2)

    # Create an empty data structure to store the comparisons
    results['graph_comparison_data'] = {}

    # Iterate through the permutations and gather data
    for g1, g2 in graph_pair_permutations:
        comparison_results = compare_graphs(results['minimal_subgraph_data'][g1],
                                            results['minimal_subgraph_data'][g2])
        # Store the results in an indexed structure
        results['graph_comparison_data'][f"{g1}${g2}"] = comparison_results

    return results


def main():
    # TODO Add proper help messages and usage examples
    parser = argparse.ArgumentParser()
    # List of input files, and an optional output file
    parser.add_argument('input_files', nargs='+', type=pathlib.Path, help='local input graph files')
    parser.add_argument('-o', nargs='?', type=argparse.FileType('w'), default=sys.stdout)

    # Parse input to match with specs
    args = parser.parse_args()
    # Validate parameters in terms of remote priority as well as local file and dirtree existence
    args = validate_parameters(args)
    # Get the comparison metrics
    results = get_comparison_data(args.input_files)
    # Output the results
    args.o.write(json.dumps(results, cls=SetEncoder))


if __name__ == "__main__":
    main()
