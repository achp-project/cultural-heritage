# Arches periods to PeriodO

Our goal is to export Arches cultural periods, and subperiods, as new entries in [PeriodO](https://github.com/achp-project/cultural-heritage/tree/main/periodo-projects#periodo) in an [automated way](https://github.com/achp-project/cultural-heritage/tree/main/periodo-projects#automated-creation-of-periodo-files). 

## PeriodO

[PeriodO](https://perio.do/en/) is a temporal gazetteer. In PeriodO, each period is composed of:
- a duration (`start` and `stop`)
- a geographical extension (`spatialCoverage`)
- an authority (`authorities`)

An example of the `Predynastic` JSON is here: https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/periodo/periodo-period-cp44786m7.json [^1].

<p align="center">
  <img alt="img-name" src="../www/periodo-json-template-predynastic.png" width="400">
  <br>
    <em>screenshot of the `Predynastic` record in PeriodO</em>
</p>

## Workflow

We start to work on the EAMENA dataset. EAMENA has these periods or subperiods: https://github.com/achp-project/cultural-heritage/blob/main/periodo-projects/cultural_periods.tsv

<p align="center">
  <img alt="img-name" src="../www/periodo-periods-eamena.png" width="700">
  <br>
    <em>EAMENA periods (filtered on 'Pre-Dynastic')</em>
</p>

`@yourvick` mapped these periods with their spatial coverage:

<p align="center">
  <img alt="img-name" src="../www/periodo-spatialCoverage-eamena.png" width="800">
  <img alt="img-name" src="../www/periodo-spatialCoverage-eamena-1.png" width="800">
  <br>
    <em>Correspondances between EAMENA periods' spatial coverage and wikidata URI</em>
</p>

The [list of wikidata links for each period region](https://github.com/achp-project/cultural-heritage/blob/main/periodo-projects/wikidata_period.tsv) and a [polygon file for mapping the wkt regions](https://github.com/achp-project/cultural-heritage/blob/main/periodo-projects/period_regions.tsv) are in tsv format.

* PeriodO (`@rybesh`) sent this [template](https://gist.github.com/rybesh/9f64c127ad8eeb69619896f22064bb0e#file-example-dataset-json) for data entry into PeriodO

  - a duration ([example](https://gist.github.com/rybesh/9f64c127ad8eeb69619896f22064bb0e#file-example-dataset-json-L35-L36))
  - a geographical extension ([example](https://gist.github.com/rybesh/9f64c127ad8eeb69619896f22064bb0e#file-example-dataset-json-L27-L32))
  - an authority ([example](https://gist.github.com/rybesh/9f64c127ad8eeb69619896f22064bb0e#file-example-dataset-json-L7-L8))


* This template has been updated with for the `Chalcolithic (Northern Iran)` cultural period: https://github.com/achp-project/cultural-heritage/blob/main/periodo-projects/template_eamena.json

### Automated creation of PeriodO files

The script [create_periodo_json.py](https://github.com/achp-project/cultural-heritage/blob/main/periodo-projects/create_periodo_json.py) automated the creation of JSON file by:

1. collecting EAMENA `ea.duration.taq` and `ea.duration.tpq` to fill PeriodO (time) `start` and `stop`
2. collecting wikidata URI for spatial coverages 
3. use the file [rdm-bu-period.check.xlsx](https://github.com/achp-project/cultural-heritage/blob/main/periodo-projects/rdm-bu-period-check.xlsx)[^4] to gather:
  - Arabic translation
  - broader periods (ie, parent period)

Results are in: https://github.com/achp-project/cultural-heritage/tree/main/periodo-projects/exports

## TODO

1. add records to the `broader` field
3. ~~use a [temporal annotation / entity recognition tool](https://github.com/historical-time/projects-tools-standards#temporal-annotation--entity-recognition) to add PeriodO (time) `label`[^3] ~~

---

[^1]: This example corresponding to the URL: https://client.perio.do/?page=period-view&backendID=web-https%3A%2F%2Fdata.perio.do%2F&authorityID=p0cp447&periodID=p0cp44786m7
[^2]: in parentesis in the [cultural_periods.tsv](https://github.com/achp-project/cultural-heritage/blob/main/periodo-projects/cultural_periods.tsv)'s `ea.name` field. For example 'Egypt'
[^3]: For example, PeriodO `"earliestYear": "0901"` gives `"label": "late seventh century"`
[^4]: This XLSX file is exported to a TSV using the Python script [convert_xlsx_to_tsv.py](./convert_xlsx_to_tsv.py)