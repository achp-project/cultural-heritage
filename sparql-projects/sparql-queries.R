# list of ready-made SPARQL queries
# queries (q) are stored into a hash dictionary-like object
# alongside with descriptions (d) of the queries

sparq.l <- hash::hash()

# prefLabels
sparq.l$prefLabel <- list(d = "select all prefLabel for a given XML/RDF file",
                          q = "
                            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

                            SELECT ?label
                            WHERE {
                              ?s rdf:type skos:Concept ;
                                 skos:prefLabel ?label .
                          }")

sparq.l$prefLabel2 <- list(d = "select all prefLabel for a given XML/RDF file",
                          q = "
                            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

                            SELECT ?narrower
                            WHERE {
                              ?concept rdf:type skos:Concept ;
                              skos:prefLabel "your_prefLabel"@en ;
                              skos:narrower ?narrower .
                            }")

