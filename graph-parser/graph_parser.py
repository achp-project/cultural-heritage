import os
import json
import requests
import shutil
import argparse
import pathlib

import bs4
import networkx as nx
from bs4 import BeautifulSoup


def get_children_node_edge_data(node_id: str, edges: list) -> list:
    """
    Get a list of node ids that contains the children of the provided node_id

    :param node_id: id for the parent node.
    :param edges: A list of data for all the edges in the graph.
    :return: A list containing a dict for every children node.
    """
    return [ # Create a list of dicts containing the relevant data to the children nodes
        {
            'id': e['rangenode_id'],
            'cidoc_class': e['ontologyproperty']
        }
        for e in edges if e['domainnode_id'] == node_id
    ]


def get_node_data(node_id: str, node_dict: dict, edges: list) -> dict:
    """
    Get a dict data structure with the relevant data for a specific node.

    :param node_id: The id of the target node.
    :param node_dict: A dict containing all nodes indexed by their ids.
    :param edges: A list of all the edges in the graph.
    :return: A dict containing the target node's relevant data.
    """
    node_data_source = node_dict[node_id]
    linked_instance_data = []
    if node_data_source['datatype'] == 'resource-instance':
        for lid in node_data_source['config']['graphs']:
            linked_instance_data.append({
                'name': lid['name'],
                'cidoc_property': lid['ontologyProperty'] if 'ontologyProperty' in lid.keys() else None
            })

    return {
      'id': node_id,
      'name': node_data_source['name'],
      'data_type': node_data_source['datatype'],
      'cidoc_class': node_data_source['ontologyclass'],
      'children_edge_data': get_children_node_edge_data(node_id, edges),
      'linked_instance_data': linked_instance_data
    }


def print_gexf(nodes: list, edges: list, output_file_path: pathlib.Path, input_file: pathlib.Path):
    """
    Print the .gexf file for the provided graph nodes and edges.

    :param nodes: A list containing all the nodes for the original graph.
    :param edges: A list containing all the edges for the original graph.
    :param output_file_path: pathlib Path for the output folder.
    :param input_file: pathlib Path object for the input file.
    """
    for n in nodes:
        cidoc_class_name = n['ontologyclass']
        cidoc_class_name = str(cidoc_class_name).split("/")[-1]
        n['graph_label'] = f"{cidoc_class_name} - {n['name']}"

    for e in edges:
        e['graph_label'] = str(e['ontologyproperty']).split("/")[-1]

    G = nx.Graph()

    for node in nodes:
        G.add_node(node['nodeid'], data=node, label=node['graph_label'])

    edge_label_properties = {}
    for e in edges:
        G.add_edge(e['domainnode_id'], e['rangenode_id'], label=e['graph_label'])
        edge_label_properties[(e['domainnode_id'], e['rangenode_id'])] = e['graph_label']

    node_labels = {n['nodeid']: n['graph_label'] for n in nodes}

    p = nx.spring_layout(G)
    nx.draw(G, pos=p, labels=node_labels)
    nx.draw_networkx_edge_labels(G, pos=p, edge_labels=edge_label_properties)

    nx.write_gexf(G, pathlib.Path(output_file_path) / input_file.name.replace('.json', '.gexf'))


def get_interactive_tree_graph_node(node_data: dict, soup_parser: BeautifulSoup, node_dict: dict, edges: list,
                                    edge_class: str = "") -> bs4.Tag:
    """
    Recursive method to generate an HTML list representation of the graph.

    :param node_data: The data of the current root of the tree.
    :param soup_parser: The parser being used to build the HTML partial tree.
    :param node_dict: Dictionary containing the nodes to be rendered indexed by id.
    :param edges: A list containing all the relevant edges and their data.
    :param edge_class: The class of the relationship of the parent node of this partial tree, whose data is contained in
    node_data.
    :return: A BeautifulSoup tag class belonging to the root of this partial HTML tree.
    """
    cidoc_class_name = node_data['cidoc_class']
    cidoc_class_name = str(cidoc_class_name).split("/")[-1]
    cidoc_edge_class = str(edge_class).split("/")[-1] if edge_class else None

    attributes = {'class': 'leaf'} if len(node_data['children_edge_data']) == 0 else {'class': 'node'}
    tag: bs4.Tag = soup_parser.new_tag(name='li', attrs=attributes)

    if edge_class != "":
        cidoc_edge_class_label = soup_parser.new_tag(name='a',
                                                     attrs={
                                                         'class': 'outlink',
                                                         'outlink': edge_class,
                                                         'onclick': f"openOutlink(this);"
                                                     })
        cidoc_edge_class_label.string = cidoc_edge_class
        tag.append(cidoc_edge_class_label)

    tag_label = soup_parser.new_tag(name='a', attrs={'class': 'name'})
    tag_label.string = f"{node_data['name']} ({node_data['data_type']})"
    tag.append(tag_label)

    cidoc_class_label = soup_parser.new_tag(name='a',
                                            attrs={
                                                'class': 'outlink',
                                                'outlink': node_data['cidoc_class'],
                                                'onclick': f"openOutlink(this);"
                                            }
                                            )

    cidoc_class_label.string = f"{cidoc_class_name}"
    tag.append(cidoc_class_label)

    if node_data['data_type'] == 'resource-instance':

        for lid in node_data['linked_instance_data']:
            lid_property = lid['cidoc_property']
            linked_instance_label = soup_parser.new_tag(name='a', attrs={'class': 'instancelink',
                                                                         'outlink': lid_property if lid_property else "",
                                                                         'onclick': f"openOutlink(this);"})
            lid_property = lid_property.split('/')[-1] if lid_property else "[untyped]"
            linked_instance_string = f"{lid_property} "
            linked_instance_label.string = linked_instance_string
            tag.append(linked_instance_label)

            lid_label = soup_parser.new_tag(name='a', attrs={'class': 'name'})
            lid_label.string = f"{lid['name']}"
            tag.append(lid_label)

    if len(node_data['children_edge_data']) > 0:
        children_tag_list = soup_parser.new_tag(name='ul')

        # Create a list of tuples containing each of the child node's CIDOC relationship and associated data
        children_node_data = [(cnd['cidoc_class'],
                              get_node_data(cnd['id'], node_dict, edges)) for cnd in node_data['children_edge_data']]
        # Sort child noes by name
        children_node_data = sorted(children_node_data, key=lambda d: d[1]['name'])

        for cnd in children_node_data:
            children_tag_list.append(get_interactive_tree_graph_node(
                cnd[1], # Child node data
                soup_parser,
                node_dict,
                edges,
                cnd[0] # Child node CIDOC relationship
            ))

        tag.append(children_tag_list)

    return tag


def generate_force_tree_data(node_dict: dict, edges: list) -> dict:
    """
    Recursive function to generate the intermediate data necessary to build the force tree representation.

    :param node_dict: A dictionary containing the source nodes with all of their data to be simplified.
    :param edges: A list containing the source edges with all of their data to be simplified
    :return: A dict containing the simplified data for the nodes and edges.
    """

    node_list = []

    for node_key, node in node_dict.items():
        node_list.append(
            {
                'id': node['nodeid'],
                'type': node['name'],
                'properties': {}
            }
        )

    edge_list = []

    for edge in edges:
        edge_list.append(
            {
                'id': edge['edgeid'],
                'type': edge['name'],
                'from': edge['domainnode_id'],
                'to': edge['rangenode_id'],
            }
        )

    force_tree_data = {'nodes': node_list, 'edges': edge_list}

    return force_tree_data


def print_force_tree(node_dict: dict, edges: list, tree_template: str, output_file_path: pathlib.Path,
                     input_file: pathlib.Path):
    """
    Print the HTML interactive force tree node JSON data inside the template HTML file.

    :param node_dict: A dict containing all the node relevant data indexed by their id.
    :param edges: A list of all the edges and their relevant data.
    :param tree_template: The HTML file where the resulting data will get injected.
    :param output_file_path: pathlib Path for the output file.
    :param input_file: pathlib Path object for the input file.
    """

    with open(tree_template, 'r') as in_file:
        tree_source_text = in_file.read()
        soup_parser = BeautifulSoup(tree_source_text, 'html.parser')

        script_node = soup_parser.find("script", {"id": "datasetScript"})
        script_node_parent = script_node.parent

        output_file_url = pathlib.Path(output_file_path) / input_file.name.replace('.json', '_forceTree.html')

        force_tree_data = generate_force_tree_data(node_dict, edges)

        # TODO This is ugly and should be done through proper JS JSON resource loading
        # Inject the JSON representation of the tree into the Javascript
        force_tree_data_string = f"var dataset = {json.dumps(force_tree_data)}"

        script_node.extract()
        new_script = soup_parser.new_tag("script", attrs={'id': "datasetScript"})
        new_script.string = force_tree_data_string
        script_node_parent.insert(0, new_script)

        with open(output_file_url, "w") as out_file:
            out_file.write(str(soup_parser.prettify()))


def print_interactive_tree_graph(root_node: dict, node_dict: dict, edges: list,
                                 tree_template: str, output_file_path: pathlib.Path, input_file: pathlib.Path):
    """
    Print the HTML interactive list containing the information fom a specific graph JSON file.

    :param root_node: Root node data of the tree graph in a dict structure.
    :param node_dict: A dict containing all the node relevant data indexed by their id.
    :param edges: A list of all the edges and their relevant data.
    :param tree_template: The HTML file where the resulting data will get injected.
    :param output_file_path: pathlib Path for the output file.
    :param input_file: pathlib Path object for the input file.
    """

    with open(tree_template, 'r') as in_file:
        tree_source_text = in_file.read()

    soup_parser = BeautifulSoup(tree_source_text, 'html.parser')

    out_tree_root = soup_parser.find("ul", {"class": "tree"})

    out_tree_root.append(get_interactive_tree_graph_node(root_node, soup_parser, node_dict, edges))

    output_file_url = pathlib.Path(output_file_path) / input_file.name.replace('.json', '.html')

    with open(output_file_url, "w") as out_file:
        out_file.write(str(soup_parser.prettify()))


def process_graph_file(input_file: pathlib.Path) -> dict:
    """ Read the structured JSON data for a specific exported Arches resource model.

    :param input_file: The Path for an input JSON graph file.
    :return: A dict structure containing the hierarchical source representation of the Arches graph for a resource.
    """
    with open(input_file, 'r') as f:
        contents = f.read()

    file_data = json.loads(contents)

    return file_data


def extract_graph_structures(graph_data: dict) -> (str, list, dict, list):
    """
    Get a new nested data structured with the essential data for graph rendering.
    This includes names and CIDOC classes.

    :param graph_data: The original Arches JSON tree structure containing the nodes and edges of the desired resource.
    :return: The simplified data structure containing relevant essential data for tree rendering.
    """
    root_node_id = graph_data['graph'][0]['root']['nodeid']
    nodes = graph_data['graph'][0]['nodes']
    node_dict = {n['nodeid']: n for n in nodes}
    edges = graph_data['graph'][0]['edges']

    return root_node_id, nodes, node_dict, edges


def process_graph_data(graph_data: dict, input_file: pathlib.Path, output_file_path: pathlib.Path):
    """
    Process the provided file containing an Arches resource graph and generate the Gephy and HTML visual
    representations.

    :param graph_data: Dict data structure containing the original Arches graph resource model.
    :param output_file_path: pathlib Path object to the target output folder.
    :param input_file: pathlib Path object with the input Graph json data.
    """

    # Extract the essential relevant data into intermediate structures
    root_node_id, nodes, node_dict, edges = extract_graph_structures(graph_data)

    # Find and build the root node
    root_node = get_node_data(root_node_id, node_dict, edges)

    # Print the .gexf file for Gephy usage (no metadata for ordering, use Gephy to sort and color)
    print_gexf(nodes=nodes, edges=edges, output_file_path=output_file_path, input_file=input_file)

    # Print the HTML interactive list containing the hierarchical CIDOC graph
    print_interactive_tree_graph(
        root_node=root_node, node_dict=node_dict, edges=edges,
        tree_template=f"{TREE_TEMPLATE_SOURCE}/tree_back.html", output_file_path=output_file_path, input_file=input_file
    )

    #  Print the HTML force tree depicting the hierarchical CIDOC graph
    print_force_tree(
        node_dict=node_dict, edges=edges,
        tree_template=f"{TREE_TEMPLATE_SOURCE}/forceTree_back.html", output_file_path=output_file_path,
        input_file=input_file
    )


# TODO Make this gather some useful stats, consider population and usage metrics (missing data)
def gather_statistics(overall_graph_data):
    """
    A simple method to gather some essential surface informative statistics, such as the amount of datatypes contained
    in an Arches resource graph.

    :param overall_graph_data: A dict structure containing the hierarchical source representation of the Arches graph
    for a resource.
    """

    statistics_block = {}
    for graph_name, graph_data in overall_graph_data.items():
        root_node_id, nodes, node_dict, edges = extract_graph_structures(graph_data)

        data_types = {}

        for n in nodes:
            if 'datatype' not in n.keys():
                continue
            data_type = n['datatype']
            if data_type not in data_types.keys():
                data_types[data_type] = 1
            else:
                data_types[data_type] += 1

        statistics_block[graph_name] = data_types

    return statistics_block


# TODO Consider proper template usage such as Jinja2
def copy_html_dependencies(output_directory: pathlib.Path):
    """
    Copy any required HTML/CSS/JS sources to render and be injected with dynamic inline data if necessary.

    :param output_directory:
    :return:
    """
    # Append the dependency path
    html_dependency_path = output_directory / 'treeHTML'
    html_dependency_path.mkdir(parents=True, exist_ok=True)

    # Copy HTML dependencies
    for hd in HTML_DEPENDENCIES:
        shutil.copyfile(TREE_TEMPLATE_SOURCE / hd, html_dependency_path / hd)


def validate_parameters(parameters: argparse.Namespace) -> argparse.Namespace:
    """
    Validate the input CLI parameters, discriminate data source and generate necessary output dir tree.

    :param parameters: argparse Namespace containing the parsed parameters.
    :return: Namespace updated for potential alternate data sources
    """

    # Check for remote input
    if getattr(parameters, 'w') is not None:
        parameters.remote_data = getattr(parameters, 'w')

    # Check local input
    else:
        # Check input files
        for in_file in parameters.input_files:
            if not os.path.isfile(in_file) or in_file.suffix != '.json':
                exit(f"Invalid input Graph file provided with value {in_file}"
                     f"{'Perhaps consider -w for remote URL.' if 'http' in str(in_file) else ''}")

    # Check output folder
    if not os.path.isdir(parameters.o):
        print(f"Creating folder {parameters.o}")
        parameters.o.mkdir(parents=True)

    # Copy HTML dependencies
    copy_html_dependencies(parameters.o)

    return parameters


# Location for the HTML tree templates
TREE_TEMPLATE_SOURCE = pathlib.Path("templates/treeHTML/")
# Names of the HTML dependencies that need to be moved
HTML_DEPENDENCIES = ['tree.js', 'tree.css', 'forceTree.js', 'forceTree.css']
# Folder to store temporary remote data
REMOTE_TEMPORARY_FOLDER = 'remoteTempData'

# TODO Add proper help messages and usage examples
parser = argparse.ArgumentParser()
# List of input files, will be ignored if remote URL is provided in the following parameter
parser.add_argument('input_files', nargs='*', type=pathlib.Path, help='local input graph files')
# A remote URL to be fetched, does not support multiple values
parser.add_argument('-w', nargs='?', type=str, help='remote input graph files')
# A path to place the output files, will make a new one if needed
parser.add_argument('-o', nargs='?', type=pathlib.Path, default=os.getcwd(), help='output folder')

# Parse input to match with specs
args = parser.parse_args()
# Validate parameters in terms of remote priority as well as local file and dirtree existence
args = validate_parameters(args)

# Fetch any required remote content
if args.w:
    # Load actual JSON
    remote_data = json.loads(requests.get(args.w).text)
    # Create temporary folder if not present
    if not os.path.exists(REMOTE_TEMPORARY_FOLDER):
        os.mkdir(REMOTE_TEMPORARY_FOLDER)

    # Create the remote JSON file path for the local replica (will be deleted)
    remote_file_path = f"{REMOTE_TEMPORARY_FOLDER}/{args.w.split('/')[-1]}"
    # Dump remote data into a local intermediate JSON file
    with open(remote_file_path, 'w', encoding='utf8') as json_file:
        json.dump(remote_data, json_file, ensure_ascii=False)

    # Overwrite CLI arg local input with the intermediate JSON file created TODO consider proper multiplex refactor
    args.input_files = [pathlib.Path(remote_file_path)]

# Generate a data dictionary with one entry per file, indexed by their actual name
file_data_batch = {in_file: process_graph_file(in_file) for in_file in args.input_files}

# If no input has been found to process, exit gracefully
if len(file_data_batch) == 0:
    exit("Missing input parameter")

# Process the input data to generate the files for every Graph
for in_file_path, in_file_data in file_data_batch.items():
    process_graph_data(in_file_data, in_file_path, args.o)

# Clean any existing remote file fetched, comment to keep remote data
if os.path.exists(REMOTE_TEMPORARY_FOLDER):
    shutil.rmtree(REMOTE_TEMPORARY_FOLDER)

# TODO Add capabilities to load from project metadata file for remote batch generation, and stat gathering
