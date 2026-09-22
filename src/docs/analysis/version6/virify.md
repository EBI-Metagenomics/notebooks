---
title: VIRify
author:
  - name: MGnify
    url: https://www.ebi.ac.uk/metagenomics
    affiliation: EMBL-EBI
    affiliation-url: https://www.ebi.ac.uk
date: last-modified
citation: true
description: Description of viral analysis with VIRify in the MGnify assembly analysis.
---

[VIRify](https://github.com/EBI-Metagenomics/emg-viral-pipeline) is a separate pipeline run on assembled contigs after the [assembly annotation pipeline](assembly-annotation.md) and accessible in the same web view. It detects, annotates, and taxonomically classifies viral sequences in [metagenomic](../../glossary.md#metagenomic). Taxonomy assignment uses a curated collection of viral orthologous protein domains (ViPhOGs).

## Results available on MGnify

- Annotated viral contigs in FASTA format.
- GFF files with sequence ontology-compliant annotations.
- Taxonomic assignments.
- Krona and Sankey interactive visualisations.
- Quality metrics from CheckV.

## Technical details and results reference

### Tools used

| Tool | Purpose |
|---|---|
| [VirSorter2](https://github.com/jiarong/VirSorter2) | Viral contig prediction |
| [VirFinder](https://github.com/jessieren/VirFinder) | Viral contig prediction |
| [PPR-Meta](https://github.com/zhenchengfang/PPR-Meta) | Viral contig prediction |
| [Prodigal](https://github.com/hyattpd/Prodigal) | Protein-coding sequence prediction |
| [HMMER](https://github.com/EddyRivasLab/hmmer) | ViPhOG domain matching for taxonomy assignment |
| [CheckV](https://bitbucket.org/berkeleylab/checkv) | Viral sequence quality assessment |

### Pipeline workflow

1. Viral contig prediction using VirSorter2, VirFinder, and PPR-Meta
2. Protein-coding sequence prediction on viral contigs using Prodigal
3. HMM-based annotation using ViPhOG protein domain profiles
4. Taxonomic classification based on ViPhOG matches
5. Quality evaluation using CheckV
6. Visualisation using Krona and Sankey plots

See the [VIRify repository](https://github.com/EBI-Metagenomics/emg-viral-pipeline) for detailed pipeline documentation.
