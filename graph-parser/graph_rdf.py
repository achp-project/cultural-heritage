def to_rdf(	infile = 'https://raw.githubusercontent.com/achp-project/prj-maeasam/main/Site.json', outfile = "C:/Rprojects/achp-ch/graph-parser/temp.ttl"):
	import requests
	from rdflib import Graph, URIRef, Literal, Namespace
	from rdflib.namespace import RDF, RDFS, DC

	response = requests.get(infile)
	data = response.json()
	nodes = data['graph'][0]['nodes'] # Replace this with the actual nodes data
	g = Graph()

	MAEASAM = Namespace("http://maeasam#")
	g.bind("dc", DC)
	g.bind("rdfs", RDFS)
	cidoc_crm_ns = "http://www.cidoc-crm.org/cidoc-crm/"
	g.bind("cidoccrm", Namespace(cidoc_crm_ns))

	for node in nodes:
		node_uri = MAEASAM[node['nodeid']]
		g.add((node_uri, RDF.type, RDFS.Class))
		g.add((node_uri, DC.title, Literal(node['name'])))
		g.add((node_uri, RDFS.subClassOf, URIRef(node['ontologyclass'])))

	# g.serialize(destination=outfile, format='turtle')
	return str(g.serialize(format='turtle'))

# # to_rdf(outfile = "C:/Rprojects/achp-ch/graph-parser/temp_1.ttl")
# print(to_rdf())