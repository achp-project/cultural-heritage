#' Show the extension of the different Global South projects based in Arches in an interactive leaflet map.
#'
#' @name prj_map
#'
#' @description Creates a leaflet map (HTML widget) showing the extension of different Arches-powered projects
#'
#' @param verbose if TRUE (by default): verbose
#'
#' @return Leaflet map
#'
#' @examples
#'
#' # export the map
#' prj_map()
#'
#' # plot without saving the map
#' prj_map(export.map = F)
#'
#' # highlight 'EAMENA' project
#' prj_map(export.map = F, prj.highlight = 'eamena')
#'
#' @export
prj_map <- function(root.project = "https://raw.githubusercontent.com/achp-project/cultural-heritage/main/map-projects/",
                    list.projects = "list-projects.tsv",
                    bck = paste0(root.project, "bckgrd/globalsouth-1.geojson"),
                    basemap = "Terrain",
                    map.title = "<a href='https://www.archesproject.org/'>Arches-based</a> projects in the Global South",
                    col.ramp = "Set1",
                    prj.weight = 1,
                    prj.highlight = "",
                    export.map = TRUE,
                    dirOut = paste0(getwd(),"/map-projects/"),
                    fileOut = "arches-global-south.html",
                    verbose = TRUE){
  `%>%` <- dplyr::`%>%` # used to not load dplyr
  if(verbose){
    print(paste0("Creates a leaflet map (HTML widget) showing the extension of different Arches-powered projects"))
  }
  l.projects <- read.table(paste0(root.project, list.projects))
  # l.projects <- read.csv(paste0(root.project, list.projects), header = F)
  # l.projects <- l.projects[ , 1]
  # projects.colors <- RColorBrewer::brewer.pal(nrow(l.projects), col.ramp)

  projects.colors <- RColorBrewer::brewer.pal(nrow(l.projects), col.ramp)
  projects.colors <- colorRampPalette(projects.colors)(nrow(l.projects))

  gs <- geojsonsf::geojson_sf(bck)
  gs.globalsouth <- gs[!is.na(gs$globalsout), ] # could be long
  if(basemap == "Terrain"){
    bmap.leaflet <- leaflet::providers$Stamen.TerrainBackground
  } else {
    bmap.leaflet <- leaflet::providers$Stamen.Toner
  }
  # leaflet map
  if(verbose){
    print(paste0("Load the map background"))
  }
  ggs <- leaflet::leaflet(gs.globalsouth,
                          width = "100%",
                          height = "100vh") %>%
    leaflet::addProviderTiles(bmap.leaflet,
                              options = leaflet::providerTileOptions(noWrap = TRUE)
    ) %>%
    leaflet::setView(lng = 53,
                     lat = 25,
                     zoom = 3) %>%
    leaflet::addPolygons(color = "red",
                         weight = 0,
                         opacity = .5,
                         fillOpacity = .5)
  if(verbose){
    print(paste0("loop over '", list.projects, "' (",  nrow(l.projects),
                 "projects) to add the ROI layers"))
  }
  #
  for(i in seq(1, nrow(l.projects))){
    # i <- 1
    prj.name <- l.projects[i, 1]
    prj.url <- l.projects[i, 2]
    if(verbose){
      print(paste0(" - read: ", prj.name))
    }
    if(prj.name == prj.highlight){
      weight <- prj.weight + 1.5
    } else {
      weight <- prj.weight
    }
    arches.project <- paste0(root.project, "prj-extent/", prj.name, ".geojson") %>%
    # arches.project <- readLines(paste0(root.project, "prj-extent/", l.projects[i], ".geojson")) %>%
      paste(collapse = "\n") %>%
      jsonlite::fromJSON(simplifyVector = FALSE)
    # TODO
    # hlink <- HTML(paste0('<a href=', shQuote(prj.url),
    #                      "\ target=\"_blank\"",
    #                      '>', prj.name,'</a>'))
    hlink <- paste0('<a href=', shQuote(prj.url),
                         "\ target=\"_blank\"",
                         '>', prj.name,'</a>')
    arches.project$features.properties.description <- hlink

    ggs <- ggs %>%
      leaflet.extras::addGeoJSONv2(geojson = arches.project,
                                   labelProperty = "project",
                                   # popupProperty = "description",
                                   popupProperty = "description",
                                   weight = weight,
                                   color = projects.colors[i],
                                   opacity = 1,
                                   fillOpacity = 0)
  }

  # lbl <- HTML(paste0('<a href=', shQuote(prj.url), "\ target=\"_blank\"",
  #                           '>', prj.name,'</a>'))
  ggs <- ggs %>%
    leaflet::addControl(map.title,
                        position = "topright")
  if(export.map){
    dir.create(file.path(dirOut), showWarnings = F)
    mapOut <- paste0(dirOut, "/", fileOut)
    htmlwidgets::saveWidget(ggs, mapOut)
    if(verbose){
      print(paste0(fileOut, " has been saved into: ", dirOut))
    }
  } else {
    print(ggs)
  }
}

prj_map(export.map = F)


