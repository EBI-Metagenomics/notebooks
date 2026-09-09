---
title: Transfer Services (FTP) file server
author: 
  - name: MGnify
    url: https://www.ebi.ac.uk/metagenomics
    affiliation: EMBL-EBI
    affiliation-url: https://www.ebi.ac.uk
date: last-modified
citation: true
description: How to download data from MGnify's file server
order: 9
---

## Transfer Services

EMBL-EBI operates a Transfer Services file server, providing high-bandwidth access to datasets from EMBL-EBI services including MGnify.

MGnify's (public) results are available in the following directories:

- Metagenomic analyses (i.e. the files produced when analysing MGYA-accessioned analyses) from [https://ftp.ebi.ac.uk/pub/databases/metagenomics/mgnify_results/](https://ftp.ebi.ac.uk/pub/databases/metagenomics/mgnify_results/)
  - These files are arranged into directories using the studies' [INSDC](glossary.md#INSDC) acccessions, with substring-prefixed folder names, and then their MGnify [Pipeline](glossary.md#Pipeline) version number. E.g. the version 5.0 analysis of `ERP003408` is found in `ERP003/ERP003408/version_5.0`.
- Genomes (i.e. the files produced when analysing MGYG-accessioned genomes from catalogues) from [https://ftp.ebi.ac.uk/pub/databases/metagenomics/mgnify_genomes/](https://ftp.ebi.ac.uk/pub/databases/metagenomics/mgnify_genomes/)
  - These files are arranged into the biome-specific catalogues according to the [MGnify Genomes](mgnify-genomes.md) schema
- Proteins (the [MGnify Protein database](mgnify-proteins.md) of proteins found in [metagenome assemblies](glossary.md#Assembly)) from [https://ftp.ebi.ac.uk/pub/databases/metagenomics/peptide_database/](https://ftp.ebi.ac.uk/pub/databases/metagenomics/peptide_database/)
  - These files are arranged into date-versioned releases. The latest release is always linked from [https://ftp.ebi.ac.uk/pub/databases/metagenomics/peptide_database/current_release/](current_release/)