#' Show the extension of the different Global South projects based in Arches in an interactive leaflet map.
#'
#' @name prj_arches_gs
#'
#' @description Creates a leaflet map (HTML widget) showing the extension of different Arches-powered projects
#'
#' @param verbose if TRUE (by default): verbose
#'
#' @return Leaflet map
#'
#' @examples
#'
#' prj_arches_gs()
#'
#'
#' @export
prj_arches_gs <- function(root.project = "https://raw.githubusercontent.com/achp-project/cultural-heritage/main/map-projects/",
                          list.projects = "list-projects.txt",
                          bck = paste0(root.project, "bckgrd/global-south.geojson"),
                          map.title = "<a href='https://www.archesproject.org/'>Arches</a> projects in the Global South",
                          col.ramp = "Set1",
                          export.map = TRUE,
                          dirOut = paste0(getwd(),"/map-projects/"),
                          fileOut = "arches-global-south.html",
                          verbose = TRUE){
  `%>%` <- dplyr::`%>%` # used to not load dplyr
  if(verbose){
    print(paste0("Creates a leaflet map (HTML widget) showing the extension of different Arches-powered projects"))
  }
  l.projects <- read.csv(paste0(root.project, list.projects), header = F)
  l.projects <- l.projects[ , 1]
  projects.colors <- RColorBrewer::brewer.pal(length(l.projects), col.ramp)
  gs <- geojsonsf::geojson_sf(bck)
  gs.globalsouth <- gs[!is.na(gs$globalsout), ] # could be long
  # leaflet map
  if(verbose){
    print(paste0("Load the map background"))
  }
  ggs <- leaflet::leaflet(gs.globalsouth,
                          width = "100%",
                          height = "100vh") %>%
    leaflet::addProviderTiles(leaflet::providers$Stamen.Toner,
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
    print(paste0("loop over '", list.projects, "' to add the project layers"))
  }
  for(i in seq(1, length(l.projects))){
    if(verbose){
      print(paste0(" - read: ", l.projects[i]))
    }
    arches.projects <- readLines(paste0(root.project, "prj-extent/", l.projects[i], ".geojson")) %>%
      paste(collapse = "\n") %>%
      jsonlite::fromJSON(simplifyVector = FALSE)
    ggs <- ggs %>%
      leaflet.extras::addGeoJSONv2(geojson = arches.projects,
                                   labelProperty = "project",
                                   popupProperty = "description",
                                   weight = 1,
                                   color = projects.colors[i],
                                   opacity = 1,
                                   fillOpacity = 0)
  }
  ggs <- ggs %>%
    leaflet::addControl(map.title,
                        position = "topright")
  if(export.map){
    dir.create(file.path(dirOut), showWarnings = F)
    mapOut <- paste0(dirOut, fileOut)
    htmlwidgets::saveWidget(ggs, mapOut)
    if(verbose){
      print(paste0(fileOut, " has been saved into: ", dirOut))
    }
  } else {
    print(ggs)
  }
}

prj_arches_gs()

