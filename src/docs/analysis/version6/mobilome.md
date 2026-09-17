---
title: Mobilome annotation pipeline v4.2.3
author:
  - name: MGnify
    url: https://www.ebi.ac.uk/metagenomics
    affiliation: EMBL-EBI
    affiliation-url: https://www.ebi.ac.uk
date: last-modified
citation: true
description: Description of mobilome annotation in the MGnify assembly analysis bundle.
---

The [Mobilome annotation pipeline](https://github.com/EBI-Metagenomics/mobilome-annotation-pipeline) is a separate pipeline run after [VIRify](virify.md) as part of the [assembly analysis bundle](assembly.md). It predicts and annotates mobile genetic elements (MGEs) — including plasmids, phages, insertion sequences, and integrative conjugative elements — in prokaryotic genomes and metagenomes, outputting results in GFF3 format. VIRify results are incorporated into the mobilome annotation.

## Results available on MGnify

- `mobilome.gff.gz`: Integrated MGE annotations in GFF3 format
- `mobilome.fasta`: Sequence records for all predicted mobile genetic elements

## Technical and download reference

### Tools used

| Tool | Version | Purpose |
|---|---|---|
| [geNomad](https://github.com/apcamargo/genomad) | 1.11.1 | Plasmid and phage prediction |
| [ICEfinder](https://bioinfo-mml.sjtu.edu.cn/ICEfinder/) | 2.0 | Integrative conjugative element detection |
| [IntegronFinder2](https://github.com/gem-pasteur/Integron_Finder) | 2.0.6 | Integron identification |
| [ISEScan](https://github.com/xiezhq/ISEScan) | 1.7.3 | Insertion sequence detection |
| [Prodigal](https://github.com/hyattpd/Prodigal) | 2.6.3 | Protein-coding sequence prediction |

### Reference databases

| Reference Database | Version | Purpose |
|---|---|---|
| geNomad database | 1.9 | Reference database for plasmid and phage prediction |
| ICEfinder2 databases | N/A | MacSyFinder models, HMM models, and UniProt reference sequences |

### Pipeline workflow

1. Preprocessing: Contig filtering and protein-coding sequence prediction
2. Prediction: Concurrent execution of geNomad, ICEfinder2, IntegronFinder2, and ISEScan, plus compositional outlier detection for contigs >100 kb
3. Integration: Results parsing and incorporation of VIRify output; fragments <500 bp and elements lacking genes are filtered out
4. Postprocessing: GFF validation and output compression

See the [Mobilome annotation pipeline repository](https://github.com/EBI-Metagenomics/mobilome-annotation-pipeline) for detailed documentation. <!-- TODO(review): Confirm the repository link and whether additional user-facing explanation is needed. -->
