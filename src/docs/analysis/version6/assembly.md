---
title: Assembly analysis
author:
  - name: MGnify
    url: https://www.ebi.ac.uk/metagenomics
    affiliation: EMBL-EBI
    affiliation-url: https://www.ebi.ac.uk
date: last-modified
citation: true
description: Overview of MGnify assembly analysis.
order: 3
---

MGnify assembly analysis consists of three pipelines: the assembly annotation pipeline, VIRify, and the mobilome annotation pipeline (MAP). Their results are presented together on MGnify, but each pipeline has its own purpose and version.

Assembly analysis accepts assembled [metagenomic](../../glossary.md#metagenomic) and [metatranscriptomic](../../glossary.md#metatranscriptomic) datasets.

## Analyses

1. [Assembly annotation pipeline](assembly-annotation.md) provides quality-control, taxonomic, functional, pathway, and systems annotations for assembled metagenomic contigs.
2. [VIRify](virify.md) detects, annotates, and classifies viral sequences in the metagenomic assembly.
3. [Mobilome annotation pipeline (MAP)](mobilome.md) identifies mobile genetic elements and incorporates results from VIRify.

These pipelines run as connected analyses, and their results are accessible from the same MGnify website and FTP server.

## Submitting data to be assembled

Users can request assembly of their own raw sequencing reads or publicly available datasets using the “Request analysis” section of the [MGnify home page](https://www.ebi.ac.uk/metagenomics/). User-owned raw reads, with host sequences removed, must be archived in ENA before an assembly request can be submitted. Alternatively, pre-assembled datasets, including those produced using other assembly algorithms, can be analysed.

Each pipeline is versioned independently. See [Comparability between pipeline versions](analysis.md#comparability-between-pipeline-versions) for an explanation of MGnify pipeline versions.
