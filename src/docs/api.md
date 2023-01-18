# RESTful API

With the rapid expansion in the number of datasets deposited in MGnify, it has become increasingly important to provide programmatic
access to the data for cross-database complex queries.

## API Overview

### Current version

Current API version is **v1**

### Base URL

The base address to the API is [https://www.ebi.ac.uk/metagenomics/api/latest/](https://www.ebi.ac.uk/metagenomics/api/latest/).

A GET request can be issued to the root endpoint to get all categories that the API supports.

```bash
curl -X GET "https://www.ebi.ac.uk/metagenomics/api/latest/"
```

There are several easy-to-use top-levels resources, such as
[studies](glossary.md#term-Study), [samples](glossary.md#term-Sample), [runs](glossary.md#term-Run),
experiment-types, [biomes](glossary.md#term-Biome), and annotations. For example
[https://www.ebi.ac.uk/metagenomics/api/latest/studies](https://www.ebi.ac.uk/metagenomics/api/latest/studies) retrieves a list
of all studies, while [https://www.ebi.ac.uk/metagenomics/api/latest/studies/ERP009004](https://www.ebi.ac.uk/metagenomics/api/latest/studies/ERP009004)
retrieves a single study, with the accession ERP009004. The samples contained
within this study can be retrieved using the relationship URL:
[https://www.ebi.ac.uk/metagenomics/api/latest/studies/ERP009004/samples](https://www.ebi.ac.uk/metagenomics/api/latest/studies/ERP009004/samples).

### The Browsable API

The easiest way to discover the API’s capabilities is to open the interactive
[“Browsable API” in your web browser](https://www.ebi.ac.uk/metagenomics/api/latest/).

This interace is created automatically when you open an API endpoint from a program
that supports HTML (i.e. your browser).
If you were to request the same URL using e.g. `curl`, plain JSON would be returned.
This means you can find the URL pattern for data you’re interested in interactively,
then copy the URL into your scripts.

### HTTP methods

API provides read-only access to all resources, that means only HTTP GET
method can be used with exception of authentication endpoint.

### Response

Links to a resource return a JSON object formatted data structure that
contains the resource type (in this example [biomes](glossary.md#term-Biome)), associated
object identifier (*id*) and *attributes*. Where appropriate, *relationships*
and links are provided to other resources, allowing complex queries to be
constructed.

```json
{
  "data": {
      "type": "studies",
      "id": "MGYS00002008",
      "attributes": {
          "bioproject": "PRJEB22493",
          "samples-count": 136,
          "accession": "MGYS00002008",
          "secondary-accession": "ERP104174",
          "centre-name": "EMBL-EBI",
          "is-public": true,
          "public-release-date": null,
          "study-abstract": "The APY Third Party Annotation (TPA) assembly was derived from the primary whole genome shotgun (WGS) data set PRJEB1787. This project includes samples from the following biomes : Marine.",
          "study-name": "EMG produced TPA metagenomics assembly of the Shotgun Sequencing of Tara Oceans DNA samples corresponding to size fractions for  prokaryotes. (APY) data set",
          "data-origination": "SUBMITTED",
          "last-update": "2022-01-16T11:17:46"
      },
      "relationships": {
          "downloads": {
              "links": {
                  "related": "https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00002008/downloads"
              }
          },
          "biomes": {
              "links": {
                  "related": "https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00002008/biomes"
              },
              "data": [
                  {
                      "type": "biomes",
                      "id": "root:Environmental:Aquatic:Marine:Oceanic",
                      "links": {
                          "self": "https://www.ebi.ac.uk/metagenomics/api/v1/biomes/root:Environmental:Aquatic:Marine:Oceanic"
                      }
                  }
              ]
          },
          "studies": {
              "links": {
                  "related": "https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00002008/studies"
              },
              "data": [
                  {
                      "type": "studies",
                      "id": "MGYS00000410",
                      "links": {
                          "self": "https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00000410"
                      }
                  },
                  {
                      "type": "studies",
                      "id": "MGYS00000492",
                      "links": {
                          "self": "https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00000492"
                      }
                  },
                  {
                      "type": "studies",
                      "id": "MGYS00001482",
                      "links": {
                          "self": "https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00001482"
                      }
                  }
              ]
          },
          "samples": {
              "links": {
                  "related": "https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00002008/samples"
              }
          },
          "geocoordinates": {
              "links": {
                  "related": "https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00002008/geocoordinates"
              }
          },
          "publications": {
              "links": {
                  "related": "https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00002008/publications"
              },
          },
          "analyses": {
              "links": {
                  "related": "https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00002008/analyses"
              },
          }
      },
      "links": {
          "self": "https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00002008"
      }
  }
}
```

### Hypermedia

All resources may have one or more **links** properties referencing to other
resources, to provide explicit URLs so that proper API clients don’t need to
construct URLs on their own.

**NOTE**: It is highly recommended for API clients to use links for future upgrades
of the API.

### Pagination

As some queries can result in a large response, the API supports pagination,
using a page number and size of results per page as query parameters. Request
that return multiple items is paginated to 20 items by default, and can be
increased up to 100:

```bash
curl -X GET "https://www.ebi.ac.uk/metagenomics/api/latest/studies?page_size=100"
```

Navigation through pages:

```json
{
  "links": {
    "first": "https://www.ebi.ac.uk/metagenomics/api/latest/studies?page=1",
    "last": "https://www.ebi.ac.uk/metagenomics/api/latest/studies?page=63",
    "next": "https://www.ebi.ac.uk/metagenomics/api/latest/studies?page=26",
    "prev": "https://www.ebi.ac.uk/metagenomics/api/latest/studies?page=24"
  },
  "data": [ ],
  "meta": {
    "pagination": {
      "page": 25,
      "pages": 63,
      "count": 1255
    }
  }
}
```

**NOTE**: Some API endpoint use *cursor-based pagination*, because they come from a document database.
The `links` object in responses provided the necesary cursors to fetch

For example, fetching Contigs for an [analysis](glossary.md#term-Analysis-result).

```bash
curl -X GET "https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00585528/contigs"
```

Gives:

```json
{
  "links": {
      "next": "https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00585528/contigs?cursor=cD02MTUyMDU0Yzg5YTUzNWM2ZDQzYTY5MGI%3D",
      "prev": null
  },
  "data": [
      {
          "type": "analysis-job-contigs",
          "id": "6152054c89a535c6d43a68f3",
          "attributes": {
              "contig-id": "ERZ2310312.1-contig-1",
              "length": 20832,
              "coverage": 0.0,
              "analysis-id": "585528",
              "accession": "MGYA00585528",
              "pipeline-version": "5.0",
              "job-id": 585528,
              "has-cog": true,
              "has-kegg": true,
              "has-go": true,
              "has-pfam": true,
              "has-interpro": true,
              "has-antismash": false,
              "has-kegg-module": false
          }
      },
      "..."
  ],
  "meta": {
      "pagination": {
          "count": 105
      }
  }
}
```

### Parameters

Lists of resources can be filtered and sorted by selected parameters, allowing
the construction of more complex queries. For instance, in order to retrieve
oceanographic [samples](glossary.md#term-Sample) from [metagenomic](glossary.md#term-Metagenomic)
[studies](glossary.md#term-Study) taken at temperature less than 10C, the following query
could be constructed [https://www.ebi.ac.uk/metagenomics/api/latest/biomes/root:Environmental:Aquatic:Marine/samples?experiment_type=metagenomic&metadata_key=temperature&metadata_value_lte=10&ordering=accession](https://www.ebi.ac.uk/metagenomics/api/latest/biomes/root:Environmental:Aquatic:Marine/samples?experiment_type=metagenomic&metadata_key=temperature&metadata_value_lte=10&ordering=accession):

```bash
curl -X GET "https://www.ebi.ac.uk/metagenomics/api/latest/biomes/root:Environmental:Aquatic:Marine/samples?experiment_type=metagenomic&metadata_key=temperature&metadata_value_lte=10&ordering=accession"
```

The provision of such complex queries allows metadata to be combined with
annotation for powerful data analysis and visualisation.

### Customising queries: compound documents

The API response distinguishes between attributes and relationships,
allowing customisation of the response by passing fields or including
relations as parameters in the initial query.

Some relationship fields render the related data automatically,
in cases where the count of related objects is known to always be small,
and where this is an extremely common requirement.

For other relationships, adding `?include=<relationship field>`
to a query will result in the
`relationships` response including a `<relationship field>.data` object,
with a list of IDs of the related object.
Provided these data arrays are non-empty,
the response will also include a top-level `included` array,
with the corresponding IDs and fully rendered data for the related objects.
This format is known as a
[“Compound Document”](https://jsonapi.org/format/#document-compound-documents).

**NOTE**: Note that the list of related objects is *not* paginated,
and can be very expensive to query.
Only a subset of relationships are available for inclusion in compound documents:
these are based on common use cases and on queries that can be optimised
so are less likely to run slowly or time out.

The supported `?include=` relationships are discoverable using the
[“Browsable API” in your web browser](https://www.ebi.ac.uk/metagenomics/api/latest/).

For example:

```bash
curl -X GET "https://www.ebi.ac.uk/metagenomics/api/latest/studies/MGYS00002008?include=samples,biomes"
```

```json
{
  "data": {
      "type": "studies",
      "id": "MGYS00002008",
      "attributes": {
          "..."
      },
      "relationships": {
          "samples": {
              "links": {
                  "related": "https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00002008/samples"
              },
              "data": [
                  {
                      "type": "samples",
                      "id": "6173"
                  }
              ]
          },
          "..."
          "biomes": {
              "links": {
                  "related": "https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00002008/biomes"
              },
              "data": [
                  {
                      "type": "biomes",
                      "id": "root:Environmental:Aquatic:Marine",
                      "links": {
                          "self": "https://www.ebi.ac.uk/metagenomics/api/v1/biomes/root:Environmental:Aquatic:Marine"
                      }
                  }
              ]
          },
          "..."
      },
      "links": {
          "self": "https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00002008"
      }
  },
  "included": [
      {
          "type": "biomes",
          "id": "root:Environmental:Aquatic:Marine",
          "attributes": {
              "samples-count": 183,
              "biome-name": "Marine",
              "lineage": "root:Environmental:Aquatic:Marine"
          },
          "relationships": {
              "samples": {
                  "links": {
                      "related": "https://www.ebi.ac.uk/metagenomics/api/v1/biomes/root:Environmental:Aquatic:Marine/samples"
                  }
              },
              "children": {
                  "links": {
                      "related": "https://www.ebi.ac.uk/metagenomics/api/v1/biomes/root:Environmental:Aquatic:Marine/children"
                  }
              },
              "genomes": {
                  "links": {
                      "related": "https://www.ebi.ac.uk/metagenomics/api/v1/biomes/root:Environmental:Aquatic:Marine/genomes"
                  }
              },
              "studies": {
                  "links": {
                      "related": "https://www.ebi.ac.uk/metagenomics/api/v1/biomes/root:Environmental:Aquatic:Marine/studies"
                  }
              }
          },
          "links": {
              "self": "https://www.ebi.ac.uk/metagenomics/api/v1/biomes/root:Environmental:Aquatic:Marine"
          }
      },
      {
          "type": "samples",
          "id": "ERS487899",
          "attributes": {
              "sample-metadata": [],
              "longitude": -6.5669,
              "biosample": "SAMEA2619376",
              "latitude": 36.5533,
              "accession": "ERS487899",
              "analysis-completed": "2015-03-17",
              "collection-date": "2009-09-15",
              "geo-loc-name": null,
              "sample-desc": "&quot;This sample (TARA_X000000263) was collected during the Tara Oceans expedition (2009-2013) at station TARA_004 (latitudeN=36.5533, longitudeE=-6.5669) on date/time=2009-09-15T11:30, using a PUMP (High Volume Peristaltic Pump).  The sample material (saline water (ENVO:00002010), including plankton (ENVO:xxxxxxxx)) was collected at a depth of 3-7 m, targeting a surface water layer (ENVO:00002042) in the marine biome (ENVO:00000447). The sample was size-fractionated (0.22-1.6 micrometres), and stored in liquid nitrogen for later detection of prokaryote nucleic acid sequences by pyrosequencing methods, and for later metagenomics analysis. This sample has replicate sample(s): TARA_X000000264.&quot;",
              "environment-biome": "marine biome (ENVO:00000447)",
              "environment-feature": "surface water layer (ENVO:00002042)",
              "environment-material": "&quot;saline water (ENVO:00002010), including plankton (ENVO:xxxxxxxx)&quot;",
              "sample-name": "TARA_X000000263",
              "sample-alias": "TARA_X000000263",
              "host-tax-id": null,
              "species": null,
              "last-update": "2019-09-25T16:24:35"
          },
          "relationships": {
              "runs": {
                  "links": {
                      "related": "https://www.ebi.ac.uk/metagenomics/api/v1/samples/ERS487899/runs"
                  }
              },
              "biome": {
                  "data": {
                      "type": "biomes",
                      "id": "root:Environmental:Aquatic:Marine"
                  },
                  "links": {
                      "related": "https://www.ebi.ac.uk/metagenomics/api/v1/biomes/root:Environmental:Aquatic:Marine"
                  }
              },
              "studies": {
                  "links": {
                      "related": "https://www.ebi.ac.uk/metagenomics/api/v1/samples/ERS487899/studies"
                  },
                  "data": [
                      {
                          "type": "studies",
                          "id": "MGYS00002008",
                          "links": {
                              "self": "https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00002008"
                          }
                      }
                  ]
              }
          },
          "links": {
              "self": "https://www.ebi.ac.uk/metagenomics/api/v1/samples/ERS487899"
          }
      }
  ]
}
```

Datasets that cannot be made using a single Compound Document
should be built up by making several requests to the API,
using the URIs provided in the `relationships.<related field>.links.related`
attributes.

### Errors

There are three possible types of client errors on API calls:


* 400 Bad requests.


* 404 Not found.


* 403 Authentication failed.

### Cross Origin Resource Sharing

The API supports Cross Origin Resource Sharing (CORS) for AJAX requests from any origin.

## Examples


* Examples of using the API are provided in our [MGnify Notebooks Server](notebooks.md), which is available at [notebooks.mgnify.org](http://notebooks.mgnify.org). See the [dedicated documentation](notebooks.md) for that resource for more information.


* You can also find our [example notebooks and scripts on GitHub](https://github.com/EBI-Metagenomics/notebooks/tree/main/notebooks-src/notebooks).


* We also have short examples of [how to fetch paginated data from the API into one big CSV/TSV file](https://gist.github.com/SandyRogers/5d9eff7f1f7b08cfa40265f5e2adf9cd).

## Interactive documentation

We have utilised an interactive documentation framework (Swagger UI) to visualise and simplify interaction with the API’s resources via an HTML interface. Detailed explanations of the purpose of all resources, along with many examples, are provided to guide end-users.

Documentation on how to use the endpoints is available at [https://www.ebi.ac.uk/metagenomics/api/docs/](https://www.ebi.ac.uk/metagenomics/api/docs/).
