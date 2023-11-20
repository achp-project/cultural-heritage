## "Shared heritage"

"Shared heritage" is the definition of the cultural heritage when it comes to its first formalization, during the post-WWII World Heritage Convention in 1945. 
- In the real world ... 
- In the digital world "Shared" means only: how we made cultural heritage interoperable?
We are several university projects assessing cultural heritage in the Global South using the same Arches information system. We have created the GitHub organisation 'Arches Cultural Heritage Partners' to share reference data. 
The purpose of this communication iis to show how we attent to build shared semantics over Arches.

#### 🖥️ first..

We chose Python and GitHub to share ressources and source code for the management of our reference data. Python is the world most popular programming language and GitHub one of the main web-platform for source code management. 

## Context

### Where

In the Global South mainly, over large continuous geographical areas. From East to the West (the colored polygons are the projects contributing to ACHP):
*   Mongolian Archaeology Project: Surveying the Steppes (**MAPSS**): A Max Planck Institute project on Mongolian steppes
*   Central Asian Archaeological Landscapes (**CAAL**): A University College of London project on Eurasian steppes
*   Mapping Archaeological Heritage in South Asia (**MAHSA**): A University of Cambridge project on the Indus River Basin and the surrounding areas
*   Maldives Heritage Survey (**MAHS**): A Kyoto University "Maldives", "Indonesia", "Vietnam", "Thailand"
*   Endangered Archaeology in the Middle East & North Africa / Maritime Endangered Archaeology (**EAMENA-MAREA**): A consortium of Universities project, with Oxford, Southampton, Durham and Leicester, on North Africa and the Middle East
*   Mapping Africa's Endangered Sites and Monuments (**MAEASAM**): A University of Cambridge project on sub-Saharan Africa
*   Mapping Pre-Columbian Heritage in South America (**MAPHSA**): A University Pompeu i Fabra project on Amazon-Andes

### What

We are mostly mapping built heritage, and moreover endangered built heritage, so far not so much natural heritage or cultural landscape. For example EAMENA and MAESAM. But our main funder, Arcadia, is now 

## Resource Models

Resource Models (RMs), or graphs, are the models of any kind of resources. Like molds, they are not perfect. However, they allow copies to be shared. RM in Arches works the same way as a schema in a relational database. Subgraphs are the minimum semantised elements: having two nodes linked by a directed edge.

### Basic example

Here is a basic example

### Available Resource Models

So far we sharing 6 Resource Models. These files are JSON. Record CIDOC CRM based tables, relations and thesauru. We usualy hsoted them on GitHub

## Comparisons

One can select RMs to compare (checkboxes). Here we select two of them:

### Subgraph metrics

Create subgraph and comparison dataframe in CSV files by running [graph-comparator.py](https://github.com/achp-project/cultural-heritage/blob/main/graph-parser/graph_comparator.py)

### Graph drawing

#### Individual graphs

We can draw the graph of the two selected RM in a circular layout. Nodes represent the CIDOC-CRM Entities, and edges represent CIDOC-CRM properties. This output represents an overall view of the semantisation of the different projects' RM.

#### Combined graphs

Does the same but putting together the two RM. Indeed, the layout can be confusing

#### Interactive graphs

Use of interactive tools better the rendering

## RDF

the graphs can be converted into *subject-predicate-object* RDF triples. This last step allows the RM to be queried with SPARQL

### Triple store and SPARQL

Eventually, these RDF triples can be stored in a triple store (like the Ariadne european infrastructure one) to be preserved over the long-term and making queriable through SPARQL. Here 

## Perspectives

* Persistancy:
	- Our work builds over the standards, or isostandards (CIDOC-CRM, RDF/SPARQL), embeded in Arches. Python and GitHub offered so far the best framework for collaboration. By pooling our reference data, we facilitate the interoperability of our projects
* Bring closer cultural heritage data managers, stakeholders and researchers:
	- Our work aims to narrow the digital gap between cultural heritage data managers and researchers. By delivering IT tools and workflow, we think it will make easier our colleagues from different countries of the Global South, to have their data work published and aknowledged.

we coordinate to share cultural heritage data