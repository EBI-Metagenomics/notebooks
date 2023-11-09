---
title: Glossary
author: 
  - name: MGnify
    url: https://www.ebi.ac.uk/metagenomics
    affiliation: EMBL-EBI
    affiliation-url: https://www.ebi.ac.uk
date: last-modified
citation: true
description: Dictionary of terms used in MGnify and throughout this documentaiton
order: 11
---

## 16S rRNA genes
Main prokaryotic ribosomal RNA genes used for taxonomic assignments. 

## 18S rRNA genes
Main eukaryotic ribosomal RNA genes used for taxonomic assignments.

## Amplicon
Refers to environmental sample where a marker gene has been amplified and sequenced. On the EMG website, we use the term amplicon when the amplified marker gene is ribosomal RNA gene. Analysis will yield taxonomic information.

## Analysis result
The end result of the [pipeline](#pipeline) analysis of a [run](#run).

## Assembly
Refers to environmental sample where Whole Genome Shotgun sequencing reads have been assembled to form larger fragments called contigs. Analysis will yield taxonomic and functional information.

## Biome
An ecological community type. In MGnify, [biomes](#biome) are organised hierarchically going from large types (such as soil, host-associated or aquatic) to more precise types (such as forest soil, skin or coastal) based on the [GOLD classification](https://gold.jgi.doe.gov/distribution#Classification)

## COG
Cluster of Orthologous Groups of proteins - a database of groups of proteins inferred by orthology.

## GO term
A defined vocabulary term to represent the functional attributes of a protein. Defined by the the [Gene Ontology](http://geneontology.org/) initiative, GO terms are organised hierarchically to unambiguously define the biological process, precise molecular function or cellular location of a protein.

## GO slim
A GO slim is a cut-down version of the GO hierarchy to give an overview of the functional results. It is used on MGnify website. The GO slim hierarchy lacks the fine granularity of the full GO hierarchy.

## InterPro
Combines protein signatures from a number of member databases into a single searchable resource, capitalising on their individual strengths to produce a powerful integrated database and diagnostic tool.

## ITS
The internal transcribed spacers are regions situated between the [LSU and SSU](#"lsu,%20ssu") genes.

## KEGG
Kyoto Encyclopedia of Genes and Genomes - a database used to assign high level functional and pathway annotations.

## LSU, SSU
Clusters of Large and Small Subunit ribosomal RNA genes. LSU comprises 23S (for prokaryotes) and 28S (for eukaryotes) sequences while the SSU represents 16S (for prokaryotes) and 18S (for eukaryotes) sequences.

## MAGs
Metagenome assembled genomes are binned or de-replicated metagenome assemblies belonging to one taxon.

## Metabarcoding
Refers to environmental sample where a marker gene, different from ribosomal RNA gene, has been amplified and sequenced. Analysis will yield taxonomic information.

## Metagenomic
Refers to environmental sample where Whole Genome Shotgun sequencing method has been applied. Analysis will yield taxonomic and functional information.

## Metatranscriptomic
Refera to environmental sample where whole transcriptome sequencing method has been applied. Analysis will yield taxonomic and functional information.

## OTU
Operational Taxonomic Unit representing a group of sequences sharing high similarity with each other.

## Pan-genome
The entire set of genes (core and accessory) within a species.

## Pipeline
A prescribed set of successive steps needed to transform an input (raw reads and contigs for MGnify) into an output with added information (annotated files with taxonomy and functional assignments for MGnify) 

## Pipeline tool	
A software or script used during the individual step of an analysis pipeline.

## Predicted coding sequence (pCDS)
Partial or complete gene sequence as predicted by the gene caller (FragGenScan for read submissions, Prodigal and FragGenScan for assembly submissions).

## RO-Crate (Research Object Crate)
A method and standard for describing the metadata associated with a set of research data. [RO-Crates](https://www.researchobject.org/ro-crate/) are implemented as a JSON-LD schema file, which can be packaged as a ZIP file optionally containing some or all of the data it describes, and optionally an HTML file to provide a human-readable view of the crate.

## Run
The sequence file obtained from performing an experiment (an experiment generally includes several steps such as filtration, metatranscriptomic extraction and Illumina MiSeq sequencing, for example) on all or part of a [sample](#sample). Several runs can therefore be generated from a single [sample](#sample).

## Sample
A representation of the physical amount of material collected. It represents a specimen of a [biome](#biome)

## Study
Represents a collection of [samples](#sample) and experiments applied to these [samples](#sample)

















