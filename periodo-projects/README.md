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
    <em>EAMENA periods (filtered on 'Pre-Dynastic')</em>
</p>


`@yourvick` mapped the spatial extent of these periods:

<p align="center">
  <img alt="img-name" src="../www/periodo-spatialCoverage-eamena-1.png" width="900">
  <br>
    <em>Spatial coverage of EAMENA periods</em>
</p>

* PeriodO (`@rybesh`) sent this [template](https://gist.github.com/rybesh/9f64c127ad8eeb69619896f22064bb0e#file-example-dataset-json) for data entry into PeriodO

  - a duration ([example](https://gist.github.com/rybesh/9f64c127ad8eeb69619896f22064bb0e#file-example-dataset-json-L35-L36))
  - a geographical extension ([example](https://gist.github.com/rybesh/9f64c127ad8eeb69619896f22064bb0e#file-example-dataset-json-L27-L32))
  - an authority ([example](https://gist.github.com/rybesh/9f64c127ad8eeb69619896f22064bb0e#file-example-dataset-json-L7-L8))

```json
{
  "type": "rdf:Bag",
  "id": "https://client.perio.do/.well-known/genid/eamena-dataset",
  "@context": "http://n2t.net/ark:/99152/p0c",
  "authorities": {
    "https://client.perio.do/.well-known/genid/eamena-authority": {
      "id": "https://client.perio.do/.well-known/genid/eamena-authority",
      "type": "Authority",
      "periods": {
        "https://client.perio.do/.well-known/genid/eamena-period-1": {
          "id": "https://client.perio.do/.well-known/genid/eamena-period-1",
          "type": "Period",
          "source": {
            "locator": "page 13"
          },
          "label": "Transitional Period",
          "language": "http://lexvo.org/id/iso639-1/en",
          "languageTag": "en",
          "localizedLabels": {
            "en": [
              "age of Iconoclasm",
              "Byzantine Dark Ages",
              "Transitional Period"
            ]
          },
          "spatialCoverageDescription": "The name Cappadocia refers to a historical region of central Anatolia.",
          "spatialCoverage": [
            {
              "id": "http://www.wikidata.org/entity/Q51614",
              "label": "Anatolia"
            }
          ],
          "start": {
            "in": {
              "earliestYear": "0667",
              "latestYear": "0700"
            },
            "label": "late seventh century"
          },
          "stop": {
            "in": {
              "earliestYear": "0901",
              "latestYear": "0934"
            },
            "label": "early tenth century"
          },
          "note": "\"Sometimes called the 'age of Iconoclasm' or simply the \"dark ages,\" I prefer the more neutral nomenclature and thus refer to the late seventh through the early tenth centuries as the transitional period.\" (Ousterhout, 13). ",
          "editorialNote": "I agree with Ousterhout's reasoning that the label \"transitional period\" is preferable to the Iconoclastic period (which may not represent Cappadocian experience) or dark age (which is perceived as derogatory, even when it refers to the dearth of extant sources from the seventh to ninth centuries in Anatolia). "
        }
      },
      "source": {
        "citation": "Ousterhout Robert G. 2017. Visualizing Community: Art Material Culture and Settlement in Byzantine Cappadocia. Washington D.C: Dumbarton Oaks Research Library and Collection.",
        "title": "Visualizing Community: Art, Material Culture, and Settlement in Byzantine Cappadocia",
        "url": "https://worldcat.org/en/title/934100132",
        "yearPublished": "2017",
        "creators": [
          {
            "name": "Robert G. Ousterhout"
          }
        ],
        "locator": "13"
      },
      "editorialNote": "This book was written by a scholar of Byzantine architecture, and is the most up to date and comprehensive study of Cappadocian architecture during the Byzantine period. "
    }
  }
}
```

* This template has been updated with for the `Chalcolithic (Northern Iran)` cultural period: https://github.com/achp-project/cultural-heritage/blob/main/periodo-projects/template_eamena.json

### Automated creation of PeriodO files

1. match EAMENA geographical entities[^2] with `@yourvick` table to fill PeriodO `spatialCoverage` id and label
2. collect EAMENA `ea.duration.taq` and `ea.duration.tpq` to fill PeriodO (time) `start` and `stop`
3. use a [temporal annotation / entity recognition tool](https://github.com/historical-time/projects-tools-standards#temporal-annotation--entity-recognition) to add PeriodO (time) `label`[^4] 


[^1]: This example corresponding to the URL: https://client.perio.do/?page=period-view&backendID=web-https%3A%2F%2Fdata.perio.do%2F&authorityID=p0cp447&periodID=p0cp44786m7
[^2]: in parentesis in the [cultural_periods.tsv](https://github.com/achp-project/cultural-heritage/blob/main/periodo-projects/cultural_periods.tsv)'s `ea.name` field. For example 'Egypt'
[^4]: For example, PeriodO `"earliestYear": "0901"` gives `"label": "late seventh century"`