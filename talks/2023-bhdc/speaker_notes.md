## "Shared Heritage"

"Shared heritage" is the definition of cultural heritage as first formalized during the post-WWII World Heritage Convention in 1945. In the political world, "shared heritage" means sharing narratives, while in the data world, it only refers to how we make cultural heritage data interoperable. We are seven university projects assessing cultural heritage in the Global South using the same Arches information system. The purpose of our communication is to show how we intend to build shared semantics over Arches reference data.

#### 🖥️ First...

First things first... We chose Python and GitHub to share resources and source code for the management of our reference data. Python is the world's most popular programming language and is at the core of Arches. GitHub is one of the main web platforms for source code management.  We have created the GitHub organization 'Arches Cultural Heritage Partners'. This presentation is a Jupyter notebook hosted on our GitHub organization and mirrored on Google Colab (*share the URL*).

## Context

I will only adress the Where and What question, and not complete the triad of journalism assessimg the question: "When". Indeed our projects are mainly based on the use of remote sensing and seek more for large-geographical scale coverage (mapping) than in-depth chronological research.

### Where

Our projects are mainly located in the Global South, from East to West (the colored polygons represent the projects contributing to ACHP):
* Mongolian Archaeology Project: Surveying the Steppes (**MAPSS**): A Max Planck Institute project on Mongolian steppes.
* Central Asian Archaeological Landscapes (**CAAL**): A University College of London project on Eurasian steppes.
* Mapping Archaeological Heritage in South Asia (**MAHSA**): A University of Cambridge project on the Indus River Basin and the surrounding areas.
* Maldives Heritage Survey (**MAHS**): A Kyoto University project on Indonesia, Vietnam, Thailand, and the Maldives.
* The two projects: Endangered Archaeology in the Middle East & North Africa / Maritime Endangered Archaeology (**EAMENA-MAREA**) on North Africa and the Middle East, sharing the same database, and a project grouping 4 universities: Oxford, Southampton, Durham, and Leicester.
* Mapping Africa's Endangered Sites and Monuments (**MAEASAM**): A University of Cambridge project on sub-Saharan Africa.
* Mapping Pre-Columbian Heritage in South America (**MAPHSA**): A University Pompeu i Fabra project on the Amazon-Andes.

### What

We are primarily mapping built heritage, with a particular focus on endangered built heritage, and to a lesser extent, natural heritage or cultural landscapes. However, there are no conceptual nor technical constraints for Arches-based projects to assess natural areas or landscape features. *Mutatis mutandis*, the workflow we present can be adapted for this kind of data.

## Resource Models

Resource Models (RMs) or graphs are the models of any kind of resources. Like molds, they are not perfect but allow copies to be shared. RMs are CIDOC-CRM-based, with nodes connected to other nodes through directed edges (entities and properties). Within these RMs, a pair of two nodes linked by a directed edge -- or subgraphs -- are the minimum semantized units. To understand differences and similarities in cultural heritage assessment among our projects, subgraphs will be the main metric to do so.

### Basic Example

Here is a basic example: a building with construction material in basalt.

### Available Resource Models

So far, we are sharing the Heritage places Resource Models of our projects. These files are JSON, recording CIDOC CRM-based tables, relations, and thesauri.

## Comparisons

One can select RMs to compare (checkboxes). Here we select two of them:

### Subgraph Metrics

Create subgraph and comparison data frames in CSV files by running `graph-comparator.py`. The overall structure can be considered as a list of edges, with the name of the RM, start node (source), end node (target), and edge property (property).

### Graph Drawing

#### Individual Graphs

We can draw the graph of the two selected RMs in a circular layout. Nodes represent CIDOC-CRM Entities, and edges represent CIDOC-CRM properties. This output represents an overall view of the semantization of the different projects' RM.

#### Combined Graphs

Does the same but putting together the two RMs. Indeed, the layout can be confusing. But eventually, RMs can be analyzed through network analysis.

## Semantic Web

Finally, we can convert these graphs into the semantic web compliant structures.

### RDF

Graphs can be converted into *subject-predicate-object* RDF triples with the same `graph-comparator.py` function and new arguments. Here is the output in a Turtle format.

### Triple Store and SPARQL

Eventually, these RDF triples will be stored in a triple store (like the Ariadne European infrastructure one) to be preserved over the long-term and queried through SPARQL.

## Perspectives


  - Our work builds on standards or iso-standards (CIDOC-CRM, RDF/SPARQL) embedded in Arches. Python and GitHub have so far provided the best framework for collaboration. By pooling our reference data, we facilitate the interoperability of our projects.
  - However, if the semantic web is the desirable future of the web, as quoted by Peter Norvik, semantic web compliancy for cultural heritage management is not the most common approach, especially in the Global South.
* Bringing closer cultural heritage data managers, stakeholders, and researchers:
  - By developping middleware tools, we aim to favor curation of data and help data producers to use our tools for data driven researches. This could directly benefits to the professionals having their fieldwork in the Global South.

* Persistency:
Our work relies on standards such as ISO standards (CIDOC-CRM, RDF/SPARQL) embedded in Arches. Python and GitHub have been the most effective framework for collaboration thus far. By consolidating our reference data, we enhance the interoperability of our projects.
*However, while the semantic web is envisioned as the future of the web, according to Peter Norvik, achieving semantic web compliance for cultural heritage management is not the predominant approach, particularly in the Global South.*
* Bringing Closer Cultural Heritage Data Managers, Stakeholders, and Researchers:
By developing middleware tools, we aim to promote the curation of data and assist data producers in utilizing our tools for data-driven research. This could directly benefit professionals conducting fieldwork in the Global South.