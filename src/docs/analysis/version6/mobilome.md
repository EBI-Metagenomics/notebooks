---
title: Mobilome annotation pipeline (MAP)
author:
  - name: MGnify
    url: https://www.ebi.ac.uk/metagenomics
    affiliation: EMBL-EBI
    affiliation-url: https://www.ebi.ac.uk
date: last-modified
citation: true
description: Description of mobilome annotation in the MGnify assembly analysis.
order: 3.6
---

The [Mobilome Annotation Pipeline (MAP)](https://github.com/EBI-Metagenomics/mobilome-annotation-pipeline) is a separate pipeline run after the [assembly annotation pipeline](assembly-annotation.md). It is one of the three pipelines of the [assembly analysis](assembly.md). It integrates the prediction and annotation of mobile genetic elements ([MGE](../../glossary.md#mge)) and generates final results in GFF3 format. [VIRify](virify.md) results are incorporated into the mobilome annotation.

## Results available on MGnify

For each analysed [assembly](../../glossary.md#assembly), MGnify displays and provides downloads for:

- The integrated [MGE](../../glossary.md#mge) annotations in GFF3 format.
- A FASTA file with the sequence records for all predicted mobile genetic elements.

## Technical details and results reference

### Tools used

| Tool | Version | Purpose |
|---|---|---|
| [geNomad](https://github.com/apcamargo/genomad) | 1.11.1 | Plasmid and phage prediction |
| ICEfinder2-lite refactored from [ICEfinder2](https://tool2-mml.sjtu.edu.cn/ICEberg3/ICEfinder.php) | 2.0 | Detection of integrative conjugative and mobilisable elements |
| [IntegronFinder2](https://github.com/gem-pasteur/Integron_Finder) | 2.0.6 | Integron identification |
| [ISEScan](https://github.com/xiezhq/ISEScan) | 1.7.3 | Insertion sequence detection |
| Compositional Outliers | 1.0 | Non-autonomous MGEs detection based on sequence composition |

### Reference databases

| Reference Database | Version | Purpose |
|---|---|---|
| geNomad database | 1.9 | Reference database for plasmid and phage prediction |
| ICEfinder2 databases | N/A | MacSyFinder models, HMM models, and UniProt reference sequences |

See [Downloading databases](https://github.com/EBI-Metagenomics/mobilome-annotation-pipeline/blob/dev/docs/usage.md#downloading-databases) in the MAP documentation for the full list of databases.

### Pipeline workflow

1. Preprocessing: Contig filtering. MAP uses the protein-coding sequences predicted by the [assembly annotation pipeline](assembly-annotation.md)
2. Prediction: Concurrent execution of geNomad, ICEfinder2-lite, IntegronFinder2, and ISEScan, plus compositional outlier detection for contigs >100 kb
3. Integration: Results parsing and incorporation of VIRify output; fragments <500 bp and elements lacking genes are filtered out
4. Postprocessing: GFF validation and output compression

See the [Mobilome annotation pipeline repository](https://github.com/EBI-Metagenomics/mobilome-annotation-pipeline) for detailed documentation.
