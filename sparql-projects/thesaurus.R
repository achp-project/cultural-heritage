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
#' @param export.plot if TRUE will export into outDir. Default: FALSE
#' @param outDir the output directory.
#'
#' @verbose if TRUE, print messages
#'
#' @return an interactive plot
#'
#' @examples
#'
#' ## plot "EAMENA.xml" concepts as a collapsibleTree layout
#' thesaurus()
#'
#' thesaurus(height = 1400, fontSize = 7, nodeSize = 10)
#'
#' ## export "EAMENA.xml" concepts as a collapsibleTree layout
#' thesaurus(outPlot = "collapsibleTree",
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
                      # nodeSize = NA,
                      fontSize = 10,
                      width = 1400,
                      height = 800,
                      outPlot = "collapsibleTree",
                      export.plot = FALSE,
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
  if(verbose){print(paste0("Parse the XML file with the SPARQL query (..it takes time..)"))}
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
                                            # nodeSize = nodeSize,
                                            fontSize = fontSize,
                                            width = width,
                                            height = height) # could take a long time
    if(verbose){print(paste0("  done")) }
    # gph <- collapsibleTree::collapsibleTree(tree.Node,
    #                                         c("from", "to"),
    #                                         collapsed = T)
    if(export.plot){
      if(verbose){print(paste0("Export to collapsibleTree"))}
      dir.create(outDir, showWarnings = FALSE)
      if(is.na(outFile)){outFile <- root}
      outName <- paste0(outDir, outFile, "_tree.html")
      htmlwidgets::saveWidget(gph, outName)
      if(verbose){print(paste0("  done")) }
      if(verbose){print(paste0("Exported to '", outName, "'"))}
    } else {
      gph
    }
  }
  if(outPlot == "visNetwork"){
    # adapt for visNetwork
    nodes.igraph <- igraph::as_data_frame(g, what = "vertices")
    colnames(nodes.igraph)[which(names(nodes.igraph) == "name")] <- "id"
    nodes.igraph$label <- nodes.igraph$title <- nodes.igraph$id
    edges.igraph <- igraph::as_data_frame(g, what = "edges")
    gph <- visNetwork::visNetwork(nodes.igraph, edges.igraph) %>%
      visNetwork::visEdges(arrows = "to") %>%
      visNetwork::visHierarchicalLayout() # same as   visLayout(hierarchical = TRUE)
    if(export.plot){
      if(verbose){print(paste0("Export to visNetwork"))}
      dir.create(outDir, showWarnings = FALSE)
      if(is.na(outFile)){outFile <- root}
      outName <- paste0(outDir, outFile, "_viz.html")
      htmlwidgets::saveWidget(gph, outName, selfcontained = T)
      if(verbose){print(paste0("  done")) }
      if(verbose){print(paste0("Exported to '", outName, "'"))}
    } else {
      gph
    }

  }
}

# thesaurus(height = 1400, fontSize = 7)
