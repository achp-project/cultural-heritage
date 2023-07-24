# Arches cultural periods to PeriodO temporal gazetteer

The aim is to export Arches cultural periods, and subperiods, as new entries in the temporal gazetteer [PeriodO](https://perio.do/en/) [^4]. In PeriodO, each period is composed of:
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
    <em>EAMENA periods (filtered)</em>
</p>


`@yourvick` mapped the spatial extent of these periods:

<p align="center">
  <img alt="img-name" src="../www/periodo-spatialCoverage-eamena.png" width="1200">
  <br>
    <em>Spatial coverage of EAMENA periods</em>
</p>

* PeriodO (`@rybesh`) sent a [template](https://gist.github.com/rybesh/9f64c127ad8eeb69619896f22064bb0e#file-example-dataset-json) for data entry into PeriodO

  - a duration ([example](https://gist.github.com/rybesh/9f64c127ad8eeb69619896f22064bb0e#file-example-dataset-json-L35-L36))
  - a geographical extension ([example](https://gist.github.com/rybesh/9f64c127ad8eeb69619896f22064bb0e#file-example-dataset-json-L27-L32))
  - an authority ([example](https://gist.github.com/rybesh/9f64c127ad8eeb69619896f22064bb0e#file-example-dataset-json-L7-L8))

* This template has been updated with for the `Chalcolithic (Northern Iran)` cultural period: https://github.com/achp-project/cultural-heritage/blob/main/periodo-projects/template_eamena.json


* **TODO**: this process has to automated to all EAMENA periods and subperiods[^3]


[^1]: This example corresponding to the URL: https://client.perio.do/?page=period-view&backendID=web-https%3A%2F%2Fdata.perio.do%2F&authorityID=p0cp447&periodID=p0cp44786m7
[^3]: PeriodO's `PartOf` is in some ways equivalent to the hierarchical structure of EAMENA
