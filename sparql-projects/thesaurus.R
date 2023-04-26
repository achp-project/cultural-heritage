#' Read thesauri
#'
#' @name thesaurus
#'
#' @description Read the multi-linguism thesaurus with SPARQL and replot it as an interactive graph.
#'
#' @param path.thes the path to the thesaurus file.
#' @param mod the way the thesaurus in handled. Default, "read".
#' @param prefix,suffix the prefix and suffix to remove.
#' @param root the node under which the subgraph will be filtered
#' @param outPlot the type of interactive plot.
#' @param export.plot if TRUE will export into outDir.
#' @param outDir the output directory.
#'
#' @verbose if TRUE, print messages
#'
#' @return an interactive plot
#'
#' @examples
#'
#' ## export the subgraph of 'artefact' in a collapsibleTree layout
#' thesaurus(root = "artefact",
#'           outPlot = "collapsibleTree",
#'           export.plot = T,
#'           outDir = "C:/Rprojects/itineRis/results/")
#'
#'
#' @export
thesaurus <- function(rootGH =  "https://raw.githubusercontent.com/achp-project/",
                      inDir = "prj-eamena/main/reference_data/concepts/",
                      inFile = "EAMENA.xml",
                      inSPARQL = paste0(getwd(), "/sparql-projects/sparql-queries.R"),
                      mod = "read",
                      root = "artefact",
                      # prefix = "https://thesaurus.mom.fr:443/opentheso/?idc=",
                      # suffix = "&idt=th101",
                      outPlot = "collapsibleTree",
                      export.plot = FALSE,
                      outFile = NA,
                      outDir = system.file(package = 'itineRis'),
                      verbose = FALSE){
  if(is.na(outFile)){outFile <- root}
  source(inSPARQL)
  thesaurus_path <- paste0(rootGH, inDir, inFile)
  rdf <- rdflib::rdf_parse(thesaurus_path, format = "rdfxml")
  if(verbose){
    print(paste0("Will read the file'", thesaurus_path,"'"))
  }

  # sparql <-"
  #           PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  #           PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
  #
  #           SELECT ?label
  #           WHERE {
  #             ?s rdf:type skos:Concept ;
  #                skos:prefLabel ?label .
  #         }"


  sparql <-"
            select ?broader
            where {
            ?concept skos:prefLabel ?broader .
          }"
  relations <- rdflib::rdf_query(rdf, sparql)
  relations <- rdflib::rdf_query(rdf, sparq.l$prefLabel$q)
  # iris2 <- head(iris2, 10)
  # gsub(prefix, "", head(iris2$broader), fixed = T)
  relations <- relations %>%
    mutate(across(c(broader, narrower), ~gsub(prefix, "", .x, fixed = T))) %>%
    mutate(across(c(broader, narrower), ~gsub(suffix, "", .x, fixed = T)))

  sparql <- "
            prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix skos:  <http://www.w3.org/2004/02/skos/core#>
            prefix dcterms: <http://purl.org/dc/terms/>

            select ?id ?name
            where {
            ?concept skos:prefLabel ?name ;
                     dcterms:identifier ?id .
            FILTER (lang(?name) = 'en-us')
          }"

  # sparql <- "
  #           prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  #           prefix skos:  <http://www.w3.org/2004/02/skos/core#>
  #           prefix dcterms: <http://purl.org/dc/terms/>
  #
  #           select ?id ?name
  #           where {
  #           ?concept skos:prefLabel ?name ;
  #                    dcterms:identifier ?id .
  #           FILTER (lang(?name) = 'fr')
  #         }"
  nodes <- rdflib::rdf_query(rdf, sparql)
  nodes$id <- as.character(nodes$id)
  df <- merge(relations, nodes, by.x = "broader", by.y = "id", all.x = T)
  names(df)[names(df) == 'name'] <- 'from'
  df <- merge(df, nodes, by.x = "narrower", by.y = "id", all.x = T)
  names(df)[names(df) == 'name'] <- 'to'
  df <- df[ , c("from", "to")]
  g <- igraph::graph_from_data_frame(df, directed = TRUE, vertices = NULL)
  # filter on nodes
  nodes.subg <- igraph::subcomponent(g, root, mode = "out")
  subg <- igraph::subgraph(g, nodes.subg)
  if(outPlot == "visNetwork"){
    # adapt for visNetwork
    nodes <- igraph::as_data_frame(subg, what = "vertices")
    colnames(nodes)[which(names(nodes) == "name")] <- "id"
    nodes$label <- nodes$title <- nodes$id
    edges <- igraph::as_data_frame(subg, what = "edges")
    gph <- visNetwork::visNetwork(nodes, edges) %>%
      visNetwork::visEdges(arrows ="to") %>%
      visNetwork::visOptions(highlightNearest = T)
    if(export.plot){
      dir.create(outDir, showWarnings = FALSE)
      outName <- paste0(outDir, "/", outFile, ".html")
      htmlwidgets::saveWidget(gph, outName)
    } else {
      gph
    }

  }
  if(outPlot == "collapsibleTree"){
    g.df <- as_data_frame(subg, what = "edges")
    gph <- collapsibleTree::collapsibleTree(g.df,
                                            c("from", "to"),
                                            collapsed = T)
    if(export.plot){
      dir.create(outDir, showWarnings = FALSE)
      outName <- paste0(outDir, "/", outFile, ".html")
      htmlwidgets::saveWidget(gph, outName)
    } else {
      gph
    }
  }
}
