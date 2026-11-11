---
title: Using MGnify Proteins programmatically
author:
  - name: MGnify
    url: https://www.ebi.ac.uk/metagenomics
    affiliation: EMBL-EBI
    affiliation-url: https://www.ebi.ac.uk
date: last-modified
citation: true
description: Find the right API, combine protein filters, retrieve sequences in bulk, and preserve identifiers and release provenance.
---

Use the [Proteins API](mgnify-proteins-api.md) for individual MGnify90 cluster
representatives and small searches. Use [release files](#bulk) for exhaustive
searches, combinations of filters and large sequence sets. Use
[HMMER](mgnify-proteins-sequence-search.md#programmatic-search) to search by an
amino acid sequence. Agents can discover these interfaces from [llms.txt](../../llms.txt).

## Find the right API

The main MGnify API is at `https://www.ebi.ac.uk/metagenomics/api/v2`.
Protein detail and Pfam/biome search currently use the separate base
`https://www.ebi.ac.uk/metagenomics/proteins/api/v1`. No authentication is required
for these public protein endpoints. There is no need to scrape the portal.

See the [Proteins API reference](mgnify-proteins-api.md) for supported parameters,
response fields and errors, and the [main API guide](api.md) for related studies
and analyses. The examples below use the public interfaces checked on
10 November 2026.

::: {.callout-important}
### Report the scope of a search

The [search endpoint](mgnify-proteins-api.md#protein-search) returns a limited
selection of representatives. Filtering that selection locally, or intersecting
two capped searches, does not produce an exhaustive combined result. Use the
[release query below](#pfam-biome) when you need all proteins matching both a
Pfam and a biome.
:::

## Identifiers and links {#identifiers}

- **MGYP** identifies a non-redundant amino acid sequence, for example
  `MGYP000261684433`. The API serves detailed records for cluster representatives;
  a missing record does not prove that the sequence is absent from release files.
- **MGYC** identifies a contig, for example `MGYC000564781877`.
- **MGYA** identifies a MGnify analysis; **MGYS** identifies a MGnify study.
  Their detail URLs use `/api/v2/analyses/{MGYA}` and `/api/v2/studies/{MGYS}`.
- **ERZ**, such as `ERZ534239`, is an ENA analysis/assembly accession. Its ENA
  record is at `https://www.ebi.ac.uk/ena/browser/view/ERZ534239`.
- **Pfam** accessions, such as `PF04659`, link to
  `https://www.ebi.ac.uk/interpro/entry/pfam/PF04659/`.

Parquet stores MGYP and MGYC identifiers as integers. Convert a protein ID back
with `f"MGYP{protein_id:012d}"`; `MGYP000261684433` becomes `261684433` in a query.
Parquet Pfam accession `5` corresponds to `PF00005`. Preserve prefixes and
zero-padding when writing accession strings.

### Follow a protein to studies and analyses

The current API's `study_assembly_contigs[].study_accession` is an **ENA** study
accession, for example `ERP108403`. Resolve it to MGYS using the main API:

```python
import requests

MAIN = "https://www.ebi.ac.uk/metagenomics/api/v2"
response = requests.get(f"{MAIN}/studies/insdc/ERP108403", timeout=30)
response.raise_for_status()
mgys = response.json()["accession"]
print(f"{MAIN}/studies/{mgys}")
print(f"{MAIN}/studies/{mgys}/samples/")
print(f"{MAIN}/assemblies/ERZ534239/analyses")
```

Follow the assembly's analyses and then their documented relationships to find
samples and studies. These are paginated main API lists; more than one analysis
can belong to an assembly. The current protein occurrence schema and the
documented `2026_07` Parquet schema do **not** supply an MGYA for each occurrence.
Do not infer a unique MGYA from the assembly, pipeline version or a numeric ID.
In particular, Parquet `study_id` is an internal counter, not an MGYS suffix.

## Discover valid biome values

The main API provides a paginated vocabulary of lineages. This bounded example
retrieves the vocabulary, failing explicitly if the page budget is exhausted:

```python
import requests

MAIN = "https://www.ebi.ac.uk/metagenomics/api/v2"
biomes = []
for page in range(1, 101):
    response = requests.get(
        f"{MAIN}/biomes/", params={"page": page, "page_size": 100}, timeout=30
    )
    response.raise_for_status()
    data = response.json()
    biomes.extend(data["items"])
    if len(biomes) >= data["count"]:
        break
    if not data["items"]:
        raise RuntimeError("Empty page before the advertised biome count")
else:
    raise RuntimeError("Biome page budget exhausted; vocabulary is incomplete")

print([b["lineage"] for b in biomes if "Wastewater" in b["lineage"]])
```

Use the returned full lineage as `biome_lineage`. This endpoint does not return
numeric biome IDs; use a protein detail's `biomes[].id` where non-null if you need
`biome_id`. An empty protein search result does not by itself validate an
identifier; see the [search reference](mgnify-proteins-api.md#protein-search) for
no-match and validation behaviour.

## Retrieve a small list of full protein records

There is currently no batch lookup endpoint. For a short list, make serial detail
requests. Keep the requested and returned identifiers because a superseded
representative may redirect to a replacement. HTTP errors stop the example;
missing records are not silently dropped. On `429`, respect `Retry-After` before
retrying. For large lists, use the bulk sequence query below.

```python
import requests

PROTEINS = "https://www.ebi.ac.uk/metagenomics/proteins/api/v1"
accessions = ["MGYP000261684433", "MGYP000000000166"]
records = []
with requests.Session() as session:
    for requested in dict.fromkeys(accessions):
        response = session.get(f"{PROTEINS}/protein/{requested}", timeout=30)
        response.raise_for_status()  # requests follows redirects by default
        protein = response.json()
        records.append({"requested_mgyp": requested, "protein": protein})
        print(requested, "->", protein["mgyp"], len(protein["sequence"]))
```

For existence checks, use `GET` as described under
[HTTP methods](mgnify-proteins-api.md#http-methods). The
[API reference](mgnify-proteins-api.md#response-fields) explains nullable fields
and record contents.

## Choose bulk files and record the release {#bulk}

Pin a dated directory, such as
[`2026_07`](https://ftp.ebi.ac.uk/pub/databases/metagenomics/peptide_database/2026_07/),
and read its
[README and changelog](https://ftp.ebi.ac.uk/pub/databases/metagenomics/peptide_database/2026_07/README.md)
and [checksums](https://ftp.ebi.ac.uk/pub/databases/metagenomics/peptide_database/2026_07/md5sum.txt).
`current_release` can change. Even dated releases can receive corrections, so
retain the checksum file, retrieval date, exact URLs, query and tool versions.
The API version (`v1` or `v2`) is not a protein release label; protein JSON
responses currently omit that label. Do not assign `2026_07` to an API response
simply because a bulk example uses it.

Choose the smallest file that covers the population you need:

- `mgy_clusters.fa.gz`: MGnify90 representative amino acid sequences.
- `mgy_clusters_metadata.parquet`: occurrence metadata for MGnify90
  representatives, sorted by `protein_id`. The release changelog reports this
  extract at about 107 GB, so it is still a substantial download.
- `mgy_protein_sequences.parquet`: all non-redundant sequences and their
  `full_length` values.
- `mgy_proteins_pfam.parquet` and `mgy_biomes.parquet`: Pfam matches and biome
  observations, joined through `protein_id`.
- `mgy_proteins_metadata.parquet`: occurrence metadata for all proteins.
- `mgy30/`: more compact MGnify30 subsets; their README defines the selection rules.

These filenames are relative to the pinned release directory. Consult the
[Parquet guide](mgnify-proteins-parquet-queries.qmd) for the schemas. `md5sum.txt`
does not provide row counts, schemas or partitioning; a complete machine-readable
release manifest is not advertised in the checked release listing. File sizes
can be inspected using `HEAD` on the file server, independently of the Proteins
API's lack of `HEAD` support:

```bash
curl --fail --head 'https://ftp.ebi.ac.uk/pub/databases/metagenomics/peptide_database/2026_07/mgy_clusters.fa.gz'
```

### Get sequences for a list of MGYPs

Run this in DuckDB after loading its `httpfs` extension (`INSTALL httpfs; LOAD
httpfs;`). The result has one row per matching sequence, not full API records.
Compare the returned IDs against your requested IDs before declaring a batch
complete. Missing IDs will not generate placeholder rows.

```sql
SELECT protein_id, full_length, sequence
FROM read_parquet('https://ftp.ebi.ac.uk/pub/databases/metagenomics/peptide_database/2026_07/mgy_protein_sequences.parquet')
WHERE protein_id IN (1, 2, 3)
ORDER BY protein_id;
```

### Find full-length proteins for a Pfam in a biome {#pfam-biome}

This query exports **all non-redundant sequences** matching `PF00005`, full-length
status, and the Wastewater lineage or its descendants, for the pinned release.
`EXISTS` avoids duplicating a protein with multiple domain hits or biome
observations. The colon in the descendant test keeps similarly named sibling
biomes out of the result. It tests the biomes of the sequence itself, not all
members of a cluster.

::: {.callout-warning}
This is a large-data example for your own DuckDB environment, not an automatically
executed browser cell. A remote join may still scan substantial data. Inspect
[file metadata and row groups](mgnify-proteins-parquet-queries.qmd#plan-remote-query)
first; use local copies when appropriate. `LIMIT` limits output rows, not network
traffic. `COPY` writes the result directly to a local Parquet file without
collecting it into a Python list or dataframe; it is not a server-side export job.
:::

```sql
COPY (
    SELECT s.protein_id, s.full_length, s.sequence
    FROM read_parquet('https://ftp.ebi.ac.uk/pub/databases/metagenomics/peptide_database/2026_07/mgy_protein_sequences.parquet') AS s
    WHERE s.full_length IS TRUE
      AND EXISTS (
          SELECT 1
          FROM read_parquet('https://ftp.ebi.ac.uk/pub/databases/metagenomics/peptide_database/2026_07/mgy_proteins_pfam.parquet') AS p
          WHERE p.protein_id = s.protein_id AND p.pfam_accession = 5
      )
      AND EXISTS (
          SELECT 1
          FROM read_parquet('https://ftp.ebi.ac.uk/pub/databases/metagenomics/peptide_database/2026_07/mgy_biomes.parquet') AS b
          WHERE b.protein_id = s.protein_id
            AND (b.biome = 'root:Engineered:Wastewater'
                 OR starts_with(b.biome, 'root:Engineered:Wastewater:'))
      )
) TO 'pfam-biome-sequences.parquet' (FORMAT PARQUET);
```

The export has no guaranteed row order. For **MGnify90 representatives only**,
add this predicate inside the `WHERE` clause before the closing `) TO`:

```sql
AND EXISTS (
    SELECT 1
    FROM read_parquet('https://ftp.ebi.ac.uk/pub/databases/metagenomics/peptide_database/2026_07/mgy_clusters.parquet') AS c
    WHERE c.cluster_rep = s.protein_id
)
```

To write the resulting local sequence subset as FASTA with bounded Python memory:

```python
import duckdb

with duckdb.connect() as con, open("pfam-biome-sequences.fasta", "w") as fasta:
    result = con.execute(
        "SELECT protein_id, sequence FROM read_parquet('pfam-biome-sequences.parquet')"
    )
    while rows := result.fetchmany(1000):
        for protein_id, sequence in rows:
            fasta.write(f">MGYP{protein_id:012d}\n{sequence}\n")
```

## Compare releases carefully

Biome assignments are metadata and may change without a sequence changing its
MGYP. Keep the protein release, Pfam version, clustering definition and biome
lineage with each result. Differences can reflect reassignment or reclustering,
as well as additional sequences. For occurrence comparisons, retain assembly,
contig and coordinates; do not assume an internal numeric occurrence ID is
stable across releases.

Consult each release's changelog or contact
[MGnify support](https://www.ebi.ac.uk/support/metagenomics) for documented biome
changes. Count differences alone do not establish which assignments changed.
