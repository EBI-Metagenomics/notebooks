---
title: Sequence search
author:
  - name: MGnify
    url: https://www.ebi.ac.uk/metagenomics
    affiliation: EMBL-EBI
    affiliation-url: https://www.ebi.ac.uk
date: last-modified
citation: true
description: Guide to searching the MGnify protein databases with HMMER
---

MGnify protein sequence searches are provided by the EMBL-EBI HMMER web [HMMER web](https://www.ebi.ac.uk/Tools/hmmer/search/phmmer?database=mgnify30_c2){.vf-link .external target="_blank" rel="noopener noreferrer"}
service. Use `phmmer` to search a protein query sequence in the MGnify Proteins Database.

[Open HMMER](https://www.ebi.ac.uk/Tools/hmmer/search/phmmer?database=mgnify30_c2){.btn .btn-primary target="_blank" rel="noopener noreferrer"}

![The HMMER phmmer search page for submitting a protein sequence.](images/sequence_search/hmmer-mgnify30-search.png){#fig-hmmer-mgnify30-search}

## Running a search

1. Paste a FASTA-formatted amino acid sequence into the **Protein sequence**
   field, or upload a sequence file.
2. Under **Sequence database**, choose one of the MGnify30 databases described
   below. The link above preselects **MGnify30-C2**.
3. Optionally adjust the cut-offs and other advanced settings.
4. Select **Submit** to start the search.

`phmmer` returns sequences with statistically significant similarity to the
query. Results are ordered by significance and include the target protein
accessions, alignments, scores and E-values.

Note: With the increasing size of MGnify Proteins, downstream tools like [HMMER Web](https://www.ebi.ac.uk/Tools/hmmer/search/phmmer?database=mgnify30_c2) require subsets which are significantly reduced in size. To that end, the "MGnify30" clustering set was created.


![Example MGnify30-C2 results, showing MGnify protein accessions, associated studies and assemblies, Pfam matches and E-values.](images/sequence_search/hmmer-mgnify30-results.png){#fig-hmmer-mgnify30-results}

## Choosing a MGnify30 database

MGnify30 contains representative sequences from MGnify protein clusters formed
at 30% sequence identity. HMMER provides three subsets for different search
goals:

![MGnify30-C2 selected as the HMMER sequence database, with the default search cut-offs.](images/sequence_search/hmmer-mgnify30-database.png){#fig-hmmer-mgnify30-database}

### Non-singletons (MGnify30-C2)
The non-singletons subset was created by extracting clusters that have **at least two members**, thereby excluding a majority of the representatives. This subset contains **128,674,267 cluster representatives**.

### Larger non-singletons (MGnify30-C5-FL)
The larger non-singletons subset was created by extracting clusters that have **at least five members, including at least one member that is predicted to be a full-length sequence**. This subset therefore reduces the space even further, and guarantees at least one full-length sequence for increased confidence. This subset contains **20,911,652  cluster representatives**.

### Pfam-poor non-singletons (MGnify30-C5-PPfam)
The Pfam-poor non-singletons subset was created by extracting clusters that have **at least five members, and where at least 90% of the cluster members do not have a Pfam accession**. This subset similarly reduces the space significantly, and contains clusters for which function is relatively unknown. This subset contains **18,155,509  cluster representatives**.

See the HMMER documentation for the current list and definitions of
[target databases](https://hmmer-web-docs.readthedocs.io/en/development/databases.html).

## Recording and interpreting results

The target databases are updated periodically. Open **Search Details** above the
HMMER results table to find the target database name, release date and other
search settings. Record these details with the query sequence when a search
needs to be reproduced or reported.

![The Search Details panel records the phmmer command, MGnify30 database release and query sequence.](images/sequence_search/hmmer-mgnify30-search-details.png){#fig-hmmer-mgnify30-search-details}

HMMER's [results documentation](https://hmmer-web-docs.readthedocs.io/en/latest/result.html)
explains the results table, domain graphics, alignments, scores and E-values.

## Search programmatically {#programmatic-search}

HMMER has a separate asynchronous API, described by its
[OpenAPI schema](https://www.ebi.ac.uk/Tools/hmmer/api/v1/openapi.json) and
[API documentation](https://hmmer-web-docs.readthedocs.io/en/latest/api.html).
This sequence-similarity search is different from the synchronous Proteins API's
Pfam/biome search. Run the following Python examples in your own environment
with `requests` installed.

First discover the available targets. Save the selected database's `id`,
`version` and `release_date` with your query; a MGnify30 subset is not the entire
MGnify90 database.

```python
import requests

HMMER = "https://www.ebi.ac.uk/Tools/hmmer/api/v1"
response = requests.get(f"{HMMER}/search/databases", timeout=30)
response.raise_for_status()
targets = [db for db in response.json() if (db.get("id") or "").startswith("mgnify")]
for target in targets:
    print(target["id"], target["version"], target["release_date"], target["status"])
```

Submit one protein FASTA from `query.fasta`. Check that your chosen target is
enabled. The submission returns an ID; save it immediately and reuse it to
retrieve the result rather than submitting the same search again.

```python
from pathlib import Path
import json

target = next(db for db in targets if db["id"] == "mgnify30_c2")
if target["status"] != "enabled":
    raise RuntimeError(f"Target is not enabled: {target}")
response = requests.post(
    f"{HMMER}/search/phmmer",
    json={"database": target["id"], "input": Path("query.fasta").read_text()},
    timeout=60,
)
response.raise_for_status()
job_id = response.json()["id"]
Path("hmmer-job.json").write_text(json.dumps({"id": job_id, "database": target}, indent=2))
print(job_id)
```

Poll with a bounded wait and explicit failure handling. If the wait expires,
keep the ID and retry result retrieval later. An HTTP timeout during submission
does not establish whether a job was created; avoid blind automatic resubmission.

```python
import time

job_id = json.loads(Path("hmmer-job.json").read_text())["id"]
for attempt in range(30):
    response = requests.get(
        f"{HMMER}/result/{job_id}", params={"page": 1, "page_size": 100}, timeout=30
    )
    response.raise_for_status()
    page = response.json()
    if page["status"] == "SUCCESS":
        break
    if page["status"] in {"FAILURE", "REVOKED"}:
        raise RuntimeError(f"HMMER job {job_id}: {page}")
    time.sleep(5)
else:
    raise TimeoutError(f"Job {job_id} is still pending; resume using the saved ID")

Path("hmmer-first-page.json").write_text(json.dumps(page, indent=2))
print("Result pages:", page["page_count"])
```

This saves **only the first result page**. To retrieve all hits, request pages 2
through `page_count` with the same `page_size` and job ID, checking each response.
Keep the original sequence, target metadata, search parameters and retrieval date
alongside the results. A returned MGYP may not be a current MGnify90
representative; use the [bulk sequence files](mgnify-proteins-programmatic.md#bulk)
if it has no detail record in the Proteins API.

## Downloading MGnify protein data

MGnify protein releases and supporting files are also available from the
[MGnify FTP server](https://ftp.ebi.ac.uk/pub/databases/metagenomics/peptide_database/).
For questions or feedback, please [contact the MGnify team](https://www.ebi.ac.uk/support/metagenomics).
