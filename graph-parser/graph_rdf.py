def to_rdf(infile = 'https://raw.githubusercontent.com/achp-project/prj-maeasam/main/Site.json'):
	# TODO: OWL
	# inspired from graph_comparator.py
	import requests
	from rdflib import Graph, URIRef, Literal, Namespace
	from rdflib.namespace import RDF, RDFS, DC

	prj = infile.replace("https://raw.githubusercontent.com/achp-project/", "")
	prj = prj.split('/')[0]

	response = requests.get(infile)
	data = response.json()
	nodes = data['graph'][0]['nodes'] # Replace this with the actual nodes data
	g = Graph()

	arches_prj = Namespace("http://" + prj + "#")
	g.bind("dc", DC)
	g.bind("rdfs", RDFS)
	cidoc_crm_ns = "http://www.cidoc-crm.org/cidoc-crm/"
	g.bind("cidoccrm", Namespace(cidoc_crm_ns))

	for node in nodes:
		node_uri = arches_prj[node['nodeid']]
		g.add((node_uri, RDF.type, RDFS.Class))
		g.add((node_uri, DC.title, Literal(node['name'])))
		g.add((node_uri, RDFS.subClassOf, URIRef(node['ontologyclass'])))

	# g.serialize(destination=outfile, format='turtle')
	return str(g.serialize(format='turtle'))

# # to_rdf(outfile = "C:/Rprojects/achp-ch/graph-parser/temp_1.ttl")
print(to_rdf('https://raw.githubusercontent.com/achp-project/prj-eamena-marea/main/resource_models/Heritage%20Place.json'))