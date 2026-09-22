---
title: Proteins API
author: 
  - name: MGnify
    url: https://www.ebi.ac.uk/metagenomics
    affiliation: EMBL-EBI
    affiliation-url: https://www.ebi.ac.uk
date: last-modified
citation: true
description: Programmatically accessing MGnify Proteins data via the Proteins Web API
---

# MGnify Proteins API

## Introduction

The MGnify Proteins API provides programmatic access to the data presented on the [MGnify Proteins portal](mgnify-proteins-web.md): the metadata held for each cluster representative in the [MGnify Protein Database](mgnify-proteins.qmd), and a way to search for cluster representatives by [biome](glossary.md#biome) or by [Pfam](https://www.ebi.ac.uk/interpro/entry/pfam/) domain.

This API is **synchronous and read-only**: every request is a single `GET` that returns JSON. No authentication or API key is required.

The API is intended for looking up and exploring *individual* proteins and *small* result sets, if you need to fetch more data bulk downloads are available from the protein database release [FTP server](https://ftp.ebi.ac.uk/pub/databases/metagenomics/peptide_database/current_release/).

::: {.callout-note}
Note that detailed records exist only for **cluster representatives**, not for every protein sequence in the database. See [MGnify Proteins Resource](mgnify-proteins.qmd) for an explanation of the clustering.
:::

## API Overview

### Current version

The current API version is **v1**.

### Base URL

The base address for the API is:

```
https://www.ebi.ac.uk/metagenomics/proteins/api/v1
```

### Interactive documentation

An interactive Swagger UI is served alongside the API, listing every endpoint, parameter and response schema, and allowing requests to be issued from the browser:

* Interactive docs: [`/api/v1/docs`](https://www.ebi.ac.uk/metagenomics/proteins/api/v1/docs)
* OpenAPI schema: [`/api/v1/openapi.json`](https://www.ebi.ac.uk/metagenomics/proteins/api/v1/openapi.json)

The OpenAPI schema can be used to generate a client in your language of choice, with a tool such as [OpenAPI Generator](https://openapi-generator.tech/).

### HTTP methods

The API is read-only: only `GET` is supported.

### Endpoints

There are two endpoints:

| Endpoint | Purpose |
|---|---|
| `GET /protein/{mgyp}` | The record held for one cluster representative — see [Protein detail](#protein-detail) |
| `GET /protein/search` | Find cluster representatives by biome or Pfam domain — see [Protein search](#protein-search) |

### Errors

Errors are returned with a conventional HTTP status code and a JSON body:

| Status | Meaning |
|---|---|
| `302` | The requested MGYP is no longer a cluster representative and has been superseded by another; the `Location` header carries the replacement accession. Pass `curl -L` to follow it automatically. |
| `404` | The MGYP accession is malformed, or no such cluster representative exists |
| `422` | The query parameters are invalid: no filter given, more than one filter given, `limit` out of range, or a `biome_lineage` that matches no biome |

::: {.callout-warning}
The `detail` field has two shapes. Errors raised by the endpoint itself carry a plain string:

```json
{"detail": "No biome matches lineage 'Wastewater'. Provide a full lineage such as 'root:Engineered:Wastewater'."}
```

Errors caught during automatic parameter validation carry a list of objects instead:

```json
{"detail": [{"type": "value_error", "loc": ["query"], "msg": "Provide exactly one of biome_id or pfam_accession or biome_lineage"}]}
```

Client code that displays error messages should handle both.
:::

## Protein detail

```
GET /protein/{mgyp}
```

Returns the full record for a single cluster representative, the same information shown on its [detail page](mgnify-proteins-web.md), **excluding the predicted 3D structure**.

The `{mgyp}` path parameter is an MGYP accession. It is tolerant of formatting: `MGYP000261684433`, `mgyp000261684433` and `261684433` all resolve to the same protein.

### Response fields

* **`mgyp`**: the MGYP accession, e.g. `MGYP000261684433`.
* **`sequence`**: the amino acid sequence of the cluster representative.
* **`full_length`**: whether the sequence is a full-length ORF (`true`) or a fragment (`false`).
* **`cluster_size`**: the number of protein sequences in this cluster.
* **`biomes`**: the [biomes](glossary.md#biome) this protein was observed in, each with an `id`, a `name` (the full lineage) and a `count` of occurrences. The `id` is the value to pass to the search endpoint's `biome_id` parameter.
* **`pfam_annotations`**: Pfam domains matched within the protein — `accession`, `name`, `clan`, `evalue`, `bit_score`, and the `hmm_start`/`hmm_end` and `env_start`/`env_end` coordinates.
* **`study_assembly_contigs`**: where the protein was found — the [study](glossary.md#study) and [assembly](glossary.md#assembly) accessions, the contig accession and name, the `start`/`end` coordinates and the `strand`.

### Example

```bash
curl "https://www.ebi.ac.uk/metagenomics/proteins/api/v1/protein/MGYP000261684433"
```

```json
{
  "mgyp": "MGYP000261684433",
  "sequence": "EESGVTRAVQGAGDEVPGEVFFEKGVVEETLRGGPAGEAAAGDTEAATAET...GDGDVSVERLL",
  "full_length": false,
  "cluster_size": 1,
  "biomes": [
    {"count": 1, "id": 132, "name": "root:Environmental:Aquatic:Marine"}
  ],
  "pfam_annotations": [
    {
      "accession": "PF04659",
      "name": "Archaeal flagella protein",
      "clan": null,
      "evalue": 1.1301790139316117e-22,
      "bit_score": 87.55205535888672,
      "hmm_start": 2,
      "hmm_end": 95,
      "env_start": 325,
      "env_end": 412
    }
  ],
  "study_assembly_contigs": [
    {
      "study_accession": "ERP108403",
      "assembly_accession": "ERZ534239",
      "contig_accession": "MGYC000564781877",
      "contig_name": "ENA-OSOD01046483-OSOD01046483.1-marine-metagenome-genome-assembly--contig:-NODE-46483-length-2198-cov-1.824140",
      "start": 931,
      "end": 2196,
      "strand": "-"
    }
  ]
}
```

The `sequence` value is abbreviated above for readability.

## Protein search

```
GET /protein/search
```

Finds cluster representatives matching a single filter. Provide **exactly one** of `biome_id`, `biome_lineage` or `pfam_accession`; supplying none, or more than one, returns `422`.

### Query parameters

| Parameter | Type | Description |
|---|---|---|
| `biome_id` | integer | Match proteins observed in one specific biome, by its numeric id. Ids come from the `biomes[].id` field of a detail response. |
| `biome_lineage` | string | Match proteins observed in a biome lineage **and all of its sub-biomes**, e.g. `root:Engineered:Wastewater`. |
| `pfam_accession` | string or integer | Match proteins carrying a Pfam domain. Accepts `PF00005` or `5`. |
| `limit` | integer | Maximum number of proteins to return. Defaults to `50`, maximum `1000`. |

Results are returned as a single page ordered by MGYP accession, capped at `limit`. There is no pagination or offset: the search is designed for exploration, and larger result sets should be obtained from the [FTP server](https://ftp.ebi.ac.uk/pub/databases/metagenomics/peptide_database/current_release/).

Each result carries only `mgyp`, `full_length` and `cluster_size`. To obtain sequences and annotations, request each `mgyp` from the detail endpoint — see [Building a FASTA file for a biome](#uc-fasta).

::: {.callout-important}
`biome_lineage` must be a **full lineage**, not a fragment. `root:Engineered` or `root:Engineered:Wastewater` works, but `Wastewater` on its own matches no biome and returns `422` with an explanatory message. A valid lineage that simply has no cluster representatives returns `200` with an empty list.

The full list of biomes can be retrieved from the MGnify API's [biomes endpoint](https://www.ebi.ac.uk/metagenomics/api/v2/biomes/).
:::

### Example

```bash
curl "https://www.ebi.ac.uk/metagenomics/proteins/api/v1/protein/search?biome_lineage=root:Engineered:Wastewater&limit=3"
```

```json
[
  {"mgyp": "MGYP000000000012", "full_length": true, "cluster_size": 1},
  {"mgyp": "MGYP000000000101", "full_length": true, "cluster_size": 1},
  {"mgyp": "MGYP000000000178", "full_length": true, "cluster_size": 1}
]
```

::: {.callout-note}
Biome lineages contain colons, which are safe to send unencoded. Some biome names contain spaces (for example `root:Host-associated:Human:Digestive system`); let `curl` encode those for you:

```bash
curl -G "https://www.ebi.ac.uk/metagenomics/proteins/api/v1/protein/search" \
  --data-urlencode "biome_lineage=root:Host-associated:Human:Digestive system" \
  --data-urlencode "limit=10"
```

`-G` is required here: it tells `curl` to put the `--data-urlencode` values in the query string, which would otherwise turn the request into a `POST`.
:::

## Use cases

The examples below use Python and the [`requests`](https://requests.readthedocs.io/) library. Each one
reuses the `BASE` address defined in the first example.

### Look up a protein and extract its sequence

```python
import requests

BASE = "https://www.ebi.ac.uk/metagenomics/proteins/api/v1"

protein = requests.get(f"{BASE}/protein/MGYP000261684433").json()

print(protein["sequence"])
```

```
EESGVTRAVQGAGDEVPGEVFFEKGVVEETLRGGPAGEAAAGDTEAATAETDDGHLGSVGRNEKTSFAELKAEYESGDLEWVDDEDRETGPDTGESEHSKTSFADLKAEYESGDLEWVDDEGPDEAAARTTGSGDERTAASVETATTEVVPGEEERTAGEADEGEWDEGEWDGGEGDEETGDLADELDELELFEDEIEWDGDDNTPEESLARAGEEAGEREAERAAEDERTVEDERAAEDERGVSRDATGADTATAEEDSSADAPTADQRPDDAAGSRGQEGEAPSPEAASTSAGESPSADREGVEPEAASGGATKRRPPGESGEGKPYLETLPQGHWADLLVMEWLEFLVEEGGTQAATRALEYYERIGWIDGGVTEELERYLAGFEGDGDGALSIDHHRRSLSYVDQLGDGDVSVERLL
```

The same record written out as FASTA:

```python
print(f">{protein['mgyp']}\n{protein['sequence']}")
```

```
>MGYP000261684433
EESGVTRAVQGAGDEVPGEVFFEKGVVEETLRGGPAGEAAAGDTEAATAETDDGHLGSVGRNEKTSFAELKAEYESGDLEWVDDEDRETGPDTGESEHSKTSFADLKAEYESGDLEWVDDEGPDEAAARTTGSGDERTAASVETATTEVVPGEEERTAGEADEGEWDEGEWDGGEGDEETGDLADELDELELFEDEIEWDGDDNTPEESLARAGEEAGEREAERAAEDERTVEDERAAEDERGVSRDATGADTATAEEDSSADAPTADQRPDDAAGSRGQEGEAPSPEAASTSAGESPSADREGVEPEAASGGATKRRPPGESGEGKPYLETLPQGHWADLLVMEWLEFLVEEGGTQAATRALEYYERIGWIDGGVTEELERYLAGFEGDGDGALSIDHHRRSLSYVDQLGDGDVSVERLL
```

### Building a FASTA file for a biome {#uc-fasta}

A common workflow: find the cluster representatives observed in a biome, then retrieve each sequence.
The search endpoint returns the accessions, and the detail endpoint turns each one into a sequence.

```python
import requests

BASE = "https://www.ebi.ac.uk/metagenomics/proteins/api/v1"

# 1. Find cluster representatives from this biome and all of its sub-biomes.
hits = requests.get(
    f"{BASE}/protein/search",
    params={"biome_lineage": "root:Engineered:Wastewater", "limit": 10},
).json()

# 2. Fetch each protein, and write it out as FASTA.
with open("wastewater.fasta", "w") as fasta_file:
    for hit in hits:
        protein = requests.get(f"{BASE}/protein/{hit['mgyp']}").json()
        fasta_file.write(f">{protein['mgyp']}\n{protein['sequence']}\n")

print(f"Wrote {len(hits)} sequences to wastewater.fasta")
```

::: {.callout-note}
`requests` encodes the query parameters, so biome names that contain spaces — for example
`root:Host-associated:Human:Digestive system` — need no special handling.
:::

::: {.callout-tip}
This makes one request per protein, so keep `limit` modest and be considerate of the service. This
service is rate-limited, so queries are going to be throttled. For thousands of sequences, download the
release from the [FTP server](https://ftp.ebi.ac.uk/pub/databases/metagenomics/peptide_database/current_release/)
instead.
:::

### Finding proteins that carry a Pfam domain

Search by Pfam accession to get the matching accessions:

```python
hits = requests.get(
    f"{BASE}/protein/search",
    params={"pfam_accession": "PF00005", "limit": 5},
).json()

for hit in hits:
    print(hit["mgyp"])
```

```
MGYP000000000166
MGYP000000000617
MGYP000000002016
MGYP000000005958
MGYP000000006630
```

Fetching each hit from the detail endpoint adds the sequence length and the domains it carries:

```python
for hit in hits:
    protein = requests.get(f"{BASE}/protein/{hit['mgyp']}").json()
    domains = ", ".join(p["accession"] for p in protein["pfam_annotations"])
    length = "full-length" if protein["full_length"] else "fragment"
    print(f"{protein['mgyp']}\t{length}\t{len(protein['sequence'])} aa\t{domains}")
```

### Exploring outwards from one protein

The biome ids in a detail response are the same ids the search endpoint accepts, so you can start from a
protein of interest and find others sharing its biome:

```python
protein = requests.get(f"{BASE}/protein/MGYP000261684433").json()

for biome in protein["biomes"]:
    print(biome["id"], biome["name"])
```

```
132 root:Environmental:Aquatic:Marine
```

```python
neighbours = requests.get(
    f"{BASE}/protein/search",
    params={"biome_id": protein["biomes"][0]["id"], "limit": 10},
).json()

for hit in neighbours:
    print(hit["mgyp"])
```

```
MGYP000000000012
MGYP000000000101
MGYP000000000348
MGYP000000000812
MGYP000000000829
MGYP000000000853
MGYP000000000871
MGYP000000000872
MGYP000000001138
MGYP000000001467
```


## Related resources

* [MGnify Proteins portal](mgnify-proteins-web.md) — the web interface backed by this API.
* [Sequence Search](mgnify-proteins-sequence-search.md) — search the database *by sequence* using HMMER.
* [BigQuery public dataset](mgnify-proteins-big-query.qmd) — large-scale analytical queries.
* [FTP server](https://ftp.ebi.ac.uk/pub/databases/metagenomics/peptide_database/current_release/) — bulk downloads of complete releases.
* [MGnify RESTful API](api.md) — the main MGnify API, covering studies, samples, runs and analyses.

## License

The data is available for both academic and commercial use under a [CC0 1.0 Universal License](http://creativecommons.org/licenses/by/4.0/legalcode).

If you make use of the MGnify Protein Database, please cite the following paper:

* Richardson, L., Allen, B., Baldi, G., Beracochea, M., Bileschi, M. L., Burdett, T., Burgin, J., Caballero-Pérez, J., Cochrane, G., Colwell, L. J., Curtis, T., Escobar-Zepeda, A., Gurbich, T. A., Kale, V., Korobeynikov, A., Raj, S., Rogers, A. B., Sakharova, E., Sanchez, S., Wilkinson, D. J., Finn, R. D. MGnify: the microbiome sequence data analysis resource in 2023. *Nucleic Acids Research* (2023). [https://doi.org/10.1093/nar/gkac1080](https://doi.org/10.1093/nar/gkac1080)
