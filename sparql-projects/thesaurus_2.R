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
                      inSPARQL = paste0(getwd(), "/sparql-projects/"),
                      SPARQLfile = "sparql-queries.R",
                      # mod = "read",
                      # prefix = "https://thesaurus.mom.fr:443/opentheso/?idc=",
                      # suffix = "&idt=th101",
                      outPlot = "collapsibleTree",
                      export.plot = TRUE,
                      outDir = paste0(getwd(), "/sparql-projects/"),
                      outFile = NA,
                      verbose = TRUE){
  `%>%` <- dplyr::`%>%` # used to not load dplyr
  thesaurus_path <- paste0(rootGH, inDir, inFile)
  if(verbose){print(paste0("Read the XML file '", thesaurus_path,"'"))}
  rdf <- rdflib::rdf_parse(thesaurus_path, format = "rdfxml")
  if(verbose){print(paste0("  done"))}
  if(verbose){print(paste0("Load the R file listing the SPARQL queries '",
                           inSPARQL,"'"))}
  source(paste0(inSPARQL, SPARQLfile))
  if(verbose){print(paste0("  done"))}
  if(verbose){print(paste0("Parse the XML file with the SPARQL query"))}
  # nodes <- rdflib::rdf_query(rdf, sparq.l$prefLabel$q) # WORKS
  nodes <- rdflib::rdf_query(rdf, sparq.l$narrowerLabel$q) # WORKS but very long
  if(verbose){print(paste0("  done")) }

  if(verbose){print(paste0("Convert the data to a dataframe"))}
  # prefLabel
  nodes.prefLabel <- purrr::map(nodes$prefLabel, jsonlite::fromJSON)
  nodes.prefLabel.df <- do.call(rbind.data.frame, nodes.prefLabel)
  if(verbose){print(paste0("  'prefLabel' done"))}
  # narrower
  nodes.narrower <- purrr::map(nodes$narrower, jsonlite::fromJSON)
  nodes.narrower.df <- do.call(rbind.data.frame, nodes.narrower)
  if(verbose){print(paste0("  'narrower' done"))}
  # prefLabel + narrower
  df <- cbind(nodes.prefLabel.df, nodes.narrower.df)
  names(df) <- c("uuid.from", "from", "uuid.to", "to")
  df <- subset(df, from != to) # rm rows
  # work with igraphs
  g <- igraph::graph_from_data_frame(df[ , c("from", "to")], directed = TRUE)
  # add the root. Nodes with ingoing edges = 0 are the top nodes, just below the root
  ingoing <- igraph::degree(g, mode = 'in')
  ingoing <- ingoing[ingoing == 0]
  root <- tools::file_path_sans_ext(inFile)
  roots <- rep(root, length(ingoing))
  df.root <- data.frame(from = roots,
                        to = names(ingoing))
  # there's a misuse in the SPARQL query, or maybe the RDF/XML structure itself is bad. Indeed, a leaf is linked to its direct parents but also to its previous ancestors. It is neceserary to 'clean' the 'from', 'to' list, by retrieving only the direct parents, i.e. those having the lower (min) number of outgoing edges.
  outgoing <- igraph::degree(g, mode = 'out')
  outgoing.df <- data.frame(node = names(outgoing),
                            outgoing = as.numeric(outgoing))
  df <- merge(df, outgoing.df, all.x = TRUE, by.x = "from", by.y = "node")
  names(df)[names(df) == 'outgoing'] <- 'outgoing.from'
  df <- merge(df, outgoing.df, all.x = TRUE, by.x = "to", by.y = "node")
  names(df)[names(df) == 'outgoing'] <- 'outgoing.to'
  # loop through vertics names and collect the min outgoing edges
  selected.rownames <- c()
  for(a.node in igraph::V(g)$name){
    # a.node <- "Epipalaeolithic (North Africa)"
    df.sub <- df[df$to == a.node, ]
    df.sub <- df.sub[df.sub$outgoing.from == min(df.sub$outgoing.from), ]
    selected.rownames <- c(selected.rownames, rownames(df.sub))
  }
  # select
  df <- df[row.names(df) %in% selected.rownames, ]
  # get rid of uuids, etc.
  df <- df[ , c("from", "to")]
  # add root
  df.all <- rbind(df.root, df)
  # df.all <- df.all[c(1:1000), ]
  if(verbose){print(paste0("Convert dataframe to Node (data.tree), etc."))}
  tree <- data.tree::FromDataFrameNetwork(as.data.frame(df.all))
  tree.df <- data.tree::ToDataFrameTree(tree, "pathString")
  tree.dt <- data.table::as.data.table(tree.df)
  tree.Node <- data.tree::as.Node(tree.dt)
  if(verbose){print(paste0("  done")) }
  if(outPlot == "collapsibleTree"){
    # g.df <- as_data_frame(subg, what = "edges")
    if(verbose){print(paste0("Convert tree to collapsibleTree (could take a while)"))}
    gph <- collapsibleTree::collapsibleTree(tree.Node,
                           width = 1400,
                           height = 800) # could take a long time
    if(verbose){print(paste0("  done")) }
    # gph <- collapsibleTree::collapsibleTree(tree.Node,
    #                                         c("from", "to"),
    #                                         collapsed = T)
    if(export.plot){
      if(verbose){print(paste0("Export to collapsibleTree"))}
      dir.create(outDir, showWarnings = FALSE)
      if(is.na(outFile)){outFile <- root}
      outName <- paste0(outDir, outFile, ".html")
      htmlwidgets::saveWidget(gph, outName)
      if(verbose){print(paste0("  done")) }
      if(verbose){print(paste0("Exported to '", outName, "'"))}
    } else {
      gph
    }
  }

  # collapsible tree
  collapsibleTree(tree.Node, fill = "color")

  URL <- paste0(
    "https://cdn.rawgit.com/christophergandrud/networkD3/",
    "master/JSONdata//flare.json")

  ## Convert to list format
  Flare <- jsonlite::fromJSON(URL, simplifyDataFrame = FALSE)

  # Use subset of data for more readable diagram
  Flare$children = Flare$children[1:3]

  networkD3::diagonalNetwork(List = Flare, fontSize = 10, opacity = 0.9)

  df.1 <- data.frame(from = c(1, 1, 1, 2, 3, 3, 4),
                     to = c(5, 6, 7, 4, 8, 9, 10))

  dat <- read.table(text="ID      Car Bus Train   Feedback_Car    Feedback_Bus    Feedback_Train
23433   Yes Yes Yes     Toyota          GreyHound       Amtrak", header=TRUE)

  ## Make an edgelist from your data
  edges <- rbind(cbind(dat$ID, names(dat)[2:4]),
                 cbind(names(dat)[2:4], as.vector(t(dat[5:7]))))

  library(data.tree)
  tree <- data.tree::FromDataFrameNetwork(as.data.frame(df.1))

  tree


  df.1$pathString <- paste("world",
                           df.1$from,
                           df.1$to,
                           sep = "/")
  population <- data.tree::as.Node(df.1)
  print(population, "iso3", "population", "GNI", limit = 20)

  library(treemap)
  data(GNI2014)
  head(GNI2014)
  GNI2014$pathString <- paste("world",
                              GNI2014$continent,
                              GNI2014$country,
                              sep = "/")
  population <- data.tree::as.Node(GNI2014)
  print(population, "iso3", "population", "GNI", limit = 20)
  # g_list <- igraph::as_adj_list(g)

  wc <- igraph::cluster_walktrap(g)
  members <- igraph::membership(wc)
  karate_d3 <- networkD3::igraph_to_networkD3(g, members, what = "both")
  # see: https://christophergandrud.github.io/networkD3/#radial
  diagonalNetwork(List = karate_d3, fontSize = 10, opacity = 0.9)

  gD3 <- forceNetwork(Links = karate_d3$links, Nodes = karate_d3$nodes,
                      Source = 'source', Target = 'target', NodeID = 'name',
                      Group = 'group')
  fileName <- tools::file_path_sans_ext(inFile)
  if(verbose){print(paste0("Export to a HTML widget"))}
  fileNameOut <- paste0(outDir, fileName, ".html")
  saveNetwork(gD3, fileNameOut, selfcontained = TRUE)
  # htmlwidgets::saveWidget(gD3, )
  if(verbose){print(paste0("  done"))}

  radialNetwork(as.radialNetwork(g))



  URL <- paste0(
    "https://cdn.rawgit.com/christophergandrud/networkD3/",
    "master/JSONdata//flare.json")

  ## Convert to list format
  Flare <- jsonlite::fromJSON(URL, simplifyDataFrame = FALSE)

  # df <- df[ , c(1,3,2,4)]

  View(df[ df[ , "to"] == 'Early Bronze Age (Northern Mesopotamia)', ])

  head(as.numeric(outgoing))
  head(outgoing.df)

  g.df <- igraph::as_data_frame(g, what = "edges")
  collapsed = FALSE)


collapsibleTree::collapsibleTree(df[c(1:1000), ],
                                 c("from", "to"),
                                 collapsed = FALSE)

df$root <- tools::file_path_sans_ext(inFile)
collapsibleTree(df, c("root", "from", "to"))

roots <- sapply(decompose(g), function(x) {
  V(x)$id[ topo_sort(x)[1]+1 ] })

unfold_tree(g, roots)

View(df[ df[ , "to"] == 'Epipalaeolithic (North Africa)', ])

View(df[ df[ , "to"] == 'Early Bronze Age (Northern Mesopotamia)', ])
df[ df[ , "to"] == 'Chalcolithic (Northern Iran)', ]
df[ df[ , "to"] == 'Chalcolithic', ]
df[ df[ , "from"] == 'EAMENA', ]

unfold_tree(graph,
            mode = c("all", "out", "in", "total"),
            roots)


library(collapsibleTree)
library(igraph)

View(warpbreaks)
# nodes <- rdflib::rdf_query(rdf, sparq.l$treeLabel$q)


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
}
