# list of ready-made SPARQL queries
# queries (q) are stored into a hash dictionary-like object
# alongside with descriptions (d) of the queries
# these SPARQL queries have been tested on 'EAMENA.xml'
# cf: https://github.com/achp-project/prj-eamena-marea

sparq.l <- hash::hash()

# 'nodes' with prefLabels
sparq.l$prefLabel <- list(d = "select all prefLabel for a given XML/RDF file",
                          q = "
                            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

                            SELECT ?label
                            WHERE {
                              ?s rdf:type skos:Concept ;
                                 skos:prefLabel ?label .
                            FILTER (langMatches(lang(?label), 'en-us'))

                          }")

sparq.l$treeLabel <- list(d = "select child concepts and parent concepts (using only narrower)",
                          q = "
                            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

                            SELECT ?parentLabel ?childLabel
                            WHERE {
                              ?parentConcept skos:prefLabel 'Cultural Period'@en-us .
                              ?childConcept skos:narrower* ?parentConcept .
                              ?childConcept skos:prefLabel ?childLabel .
                              FILTER (langMatches(lang(?parentLabel), 'en-us'))
                              FILTER (langMatches(lang(?childLabel), 'en-us'))
                            }")


sparq.l$narrowerLabel <- list(d = "select concept with childs (narrower)",
                          q = "
                            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

                            SELECT ?concept ?prefLabel ?narrower
                            WHERE {
                              ?concept skos:prefLabel ?prefLabel .
                              OPTIONAL {
                                ?concept skos:narrower ?narrowerConcept .
                                ?narrowerConcept skos:prefLabel ?narrower .
                              }
                              FILTER (langMatches(lang(?prefLabel), 'en-us'))
                              FILTER (langMatches(lang(?narrower), 'en-us'))
                            }")

# sparq.l$narrowerLabel2 <- list(d = "select concept with childs (narrower)",
#                               q = "
#                             PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
#
#                             SELECT ?prefLabel ?narrower
#                             WHERE {
#                               skos:prefLabel ?prefLabel .
#                               OPTIONAL {
#                                 ?narrowerConcept skos:prefLabel ?narrower .
#                               }
#                               FILTER (langMatches(lang(?prefLabel), 'en-us'))
#                               FILTER (langMatches(lang(?narrower), 'en-us'))
#                             }")





# sparq.l$prefLabel <- list(d = "select all prefLabel for a given XML/RDF file",
#                           q = "
#                             PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#                             PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
#
#                             SELECT ?label
#                             WHERE {
#                               ?s rdf:type skos:Concept ;
#                                  skos:prefLabel ?label .
#                           }")

# sparq.l$prefLabel2 <- list(d = "select all prefLabel for a given XML/RDF file",
#                           q = "
#                             PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#                             PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
#
#                             SELECT ?narrower
#                             WHERE {
#                               ?concept rdf:type skos:Concept ;
#                               skos:prefLabel "your_prefLabel"@en ;
#                               skos:narrower ?narrower .
#                             }")

