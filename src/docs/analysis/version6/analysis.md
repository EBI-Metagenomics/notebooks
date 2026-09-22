---
title: Analysis pipeline v6
author:
  - name: MGnify
    url: https://www.ebi.ac.uk/metagenomics
    affiliation: EMBL-EBI
    affiliation-url: https://www.ebi.ac.uk
date: last-modified
citation: true
description: Description of the latest MGnify analysis pipeline and the tools it uses.
order: 3
---

## Overview

The latest MGnify analysis service (version 6) offers pipelines for three different data types: [amplicon](../../glossary.md#amplicon), raw [metagenomic](../../glossary.md#metagenomic)/[metatranscriptomic](../../glossary.md#metatranscriptomic) reads, and [assemblies](../../glossary.md#assembly).

For assembled datasets, the assembly analysis pipeline is complemented by [VIRify](virify.md) for viral sequence detection and the [Mobilome annotation pipeline](mobilome.md), both accessible in the same web view.

“MGnify analysis service v6” is the name of this collection of analysis pipelines. Each pipeline and associated service has its own version number.

## Pipeline versions

Each of the pipelines that constitute the service is versioned independently. The current versions are:

- Amplicon analysis pipeline: [v6.1.5](https://github.com/EBI-Metagenomics/amplicon-analysis-pipeline/releases/tag/v6.1.5)
- Raw reads analysis pipeline: [v6.0.0](https://github.com/EBI-Metagenomics/raw-reads-analysis-pipeline/releases/tag/v6.0.0)
- Assembly analysis pipeline: [v6.0.5](https://github.com/EBI-Metagenomics/assembly-analysis-pipeline/releases/tag/6.0.5)
- VIRify: [v3.3.2](https://github.com/EBI-Metagenomics/emg-viral-pipeline/releases/tag/v3.3.2)
- Mobilome annotation pipeline: [v4.2.3](https://github.com/EBI-Metagenomics/mobilome-annotation-pipeline/releases/tag/v4.2.3)

### Comparability between pipeline versions

When comparing results, use the first two numbers of the pipeline version. For example, analyses produced by releases `v6.1.4` and `v6.1.5` both belong to analysis version `v6.1` and can be compared.

- The first two numbers identify the analysis version, such as `v6.1`.
- The final number identifies the exact software release. Patch releases within the same analysis version produce comparable results.
- Results from different analysis versions, such as `v6.0` and `v6.1`, should not be assumed to be directly comparable.

MGnify therefore describes the amplicon pipeline as analysis version `v6.1`, while recording the full three-part software version for reproducibility.

Pipeline-specific change logs provide details about differences between patch releases.

### Changes through pipeline versions

#### Amplicon Analysis Pipeline

##### Version 6.1 [April 2026]

Version 6.1 improved completeness, reporting, and configurability. All ASVs are now published, including those without taxonomic assignments, so no detected sequence diversity is excluded. DADA2 reporting now includes selected truncation points and read counts from intermediate filtering stages, improving transparency and troubleshooting. MapSeq database selection and DADA2 execution are also more configurable, allowing the pipeline to support a wider range of datasets and analysis requirements.

##### Version 6.2 [September 2026]

Version 6.2 improved annotation support for ITS, LSU, and 5.8S-containing sequences. The ITS workflow now recognises and masks 5.8S regions, enabling the analysis of 5.8S+ITS datasets, while a bug preventing LSU annotation has been fixed. Reference databases now use a `target` field so that SSU and LSU databases are applied only to matching sequence types, reducing unnecessary searches; ITS databases continue to run across sequence types because ITS amplicons may contain adjacent ribosomal regions. 

## Analysis pipeline pages

The MGnify analysis service provides three pipelines, selected according to the type of sequence data being analysed.

- [Amplicon analysis pipeline](amplicon.md): analyses amplicon sequencing reads and provides taxonomic profiles, including ASV analysis for supported 16S and 18S datasets.
- [Raw reads analysis pipeline](raw-reads.md): analyses short or long metagenomic and metatranscriptomic reads to provide taxonomic and functional profiles.
- [Assembly analysis pipeline](assembly.md): analyses assembled metagenomic and metatranscriptomic contigs, providing taxonomic, functional, pathway, and systems annotations.

Users can request assembly of their own raw sequencing reads or publicly available datasets using the “Request analysis” section of the [MGnify home page](https://www.ebi.ac.uk/metagenomics/). User-owned raw reads, with host sequences removed, must be uploaded to ENA before an assembly request can be submitted. Alternatively, pre-assembled datasets, including those produced using other assembly algorithms, can be analysed.
