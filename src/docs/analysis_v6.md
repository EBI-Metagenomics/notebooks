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

The latest MGnify analysis service (version 6) offers workflows for three different data types: [amplicon](glossary.md#amplicon), raw [metagenomic](glossary.md#metagenomic)/[metatranscriptomic](glossary.md#metatranscriptomic) reads, and [assembly](glossary.md#assembly).

For assembled datasets, the assembly analysis pipeline is complemented by [VIRify](#virify) for viral sequence detection and the [Mobilome annotation pipeline](#mobilome-annotation-pipeline) for mobile genetic element prediction, both accessible in the same web view.

## Amplicon analysis pipeline

The MGnify v6 amplicon analysis pipeline ([GitHub repository](https://github.com/EBI-Metagenomics/amplicon-analysis-pipeline)) analyses [amplicon](glossary.md#amplicon) sequencing reads to provide taxonomic profiles from closed-reference databases. For supported [16S](glossary.md#16s-rrna-genes) and [18S](glossary.md#18s-rrna-genes) datasets, it also infers amplified regions, identifies and trims primers, calls [Amplicon Sequence Variants (ASVs)](glossary.md#amplicon-sequence-variant-asv), and assigns taxonomy to those ASVs.

### Tools and Databases Used

The amplicon analysis pipeline v6 uses the following tools and databases:

| Tool/Database | Version | Purpose |
|---|---|---|
| [bbmap](https://sourceforge.net/projects/bbmap) | 39.18 | Standardise FASTQ read files |
| [fastp](https://github.com/OpenGene/fastp) | 1.0.1 | Read quality control |
| [SeqFu](https://github.com/telatin/seqfu2) | 1.20.3 | FASTQ sanity checking |
| [seqtk](https://github.com/lh3/seqtk) | 1.4 | FASTQ file manipulation |
| [SeqKit](https://bioinf.shenwei.me/seqkit/) | 2.9.0 | FASTQ file manipulation |
| [easel](https://github.com/EddyRivasLab/easel) | 0.49 | FASTA file manipulation |
| [bedtools](https://bedtools.readthedocs.io) | 2.30.0 | FASTA sequence masking |
| [Infernal/cmsearch](https://github.com/EddyRivasLab/infernal) | 1.1.5 | rRNA sequence searching |
| [cmsearch_tblout_deoverlap](https://github.com/nawrockie/cmsearch_tblout_deoverlap) | 0.09 | Deoverlapping of cmsearch results |
| [MAPseq](https://github.com/meringlab/MAPseq) | 2.1.1b | Reference-based taxonomic classification of rRNA |
| [Krona](https://github.com/marbl/Krona) | 2.8.1 | Krona chart visualisation |
| [cutadapt](https://cutadapt.readthedocs.io) | 4.6 | Primer trimming |
| [R](https://www.r-project.org) | 4.3.3 | R programming language (runs DADA2) |
| [DADA2](https://benjjneb.github.io/dada2/index.html) | 1.30.0 | ASV calling |
| [MultiQC](https://github.com/MultiQC/MultiQC) | 1.24.1 | Result aggregation into HTML reports |
| [mgnify-pipelines-toolkit](https://github.com/EBI-Metagenomics/mgnify-pipelines-toolkit) | 0.1.8 | Toolkit containing various in-house processing scripts |
| [PIMENTO](https://github.com/EBI-Metagenomics/PIMENTO) | 1.0.2 | Primer inference toolkit |

### Reference Databases

The pipeline uses the following reference databases:

| Reference Database | Version | Purpose |
|---|---|---|
| [SILVA](https://www.arb-silva.de) | 138.1 | 16S+18S+[LSU](glossary.md#lsu-ssu) rRNA database |
| [PR2](https://pr2-database.org) | 5.0 | Protist-focused 18S+16S rRNA database |
| [UNITE](https://unite.ut.ee) | 9.0 | [ITS](glossary.md#its) database |
| [ITSoneDB](https://itsonedb.cloud.ba.infn.it) | 1.141 | [ITS](glossary.md#its) database |
| [Rfam](https://rfam.org) | 14.10 | rRNA covariance models |

### Pipeline Features

The v6 amplicon analysis pipeline includes the following key features:

- Read Quality Control: Uses fastp for read filtering and SeqFu for FASTQ sanity checking
- rRNA Sequence Categorisation: Uses Infernal/cmsearch and Rfam models to identify [SSU, LSU](glossary.md#lsu-ssu), and [ITS](glossary.md#its) sequences
- Automatic Amplified Region Inference: Automatically identifies amplified regions for 16S and 18S rRNA using PIMENTO
- Automatic Primer Identification and Trimming: Uses cutadapt for primer handling, with validation via Infernal
- ASV Calling: Calls Amplicon Sequence Variants (ASVs) using DADA2 for supported amplicons
- Taxonomic Classification: Produces closed-reference and ASV taxonomy assignments using MAPseq and Krona visualisation
- Reference Databases: Uses SILVA, PR2, UNITE, ITSoneDB, and Rfam

### Supported Amplicons

The pipeline supports the following amplicon types:

| Amplicon | Closed-reference analysis | ASV analysis |
|---|---|---|
| [16S](glossary.md#16s-rrna-genes) | ✓ | ✓ |
| [18S](glossary.md#18s-rrna-genes) | ✓ | ✓ |
| [LSU](glossary.md#lsu-ssu) | ✓ | ✗ |
| [ITS](glossary.md#its) | ✓ | ✗ |

### Pipeline Workflow

1. Quality Control: Reads undergo quality filtering using fastp and sanity checking with SeqFu
2. Amplified Region Inference: Automatic identification of amplified regions using PIMENTO
3. Primer Identification and Trimming: Automatic primer detection and removal using cutadapt
4. rRNA Sequence Extraction: Identification of rRNA sequences using Infernal/cmsearch with Rfam models
5. Closed-reference Taxonomic Classification: Taxonomy assignment using MAPseq with SILVA, PR2, UNITE, and ITSoneDB databases
6. ASV Calling: Amplicon Sequence Variant identification using DADA2
7. ASV Taxonomic Classification: Taxonomy assignment for ASVs using MAPseq against SILVA and PR2
8. Visualisation: Interactive taxonomic visualisation using Krona
9. Result Aggregation: Comprehensive reporting with MultiQC

### Results available on MGnify

For each analysed [run](glossary.md#run), MGnify displays and provides downloads for:

- Quality control summaries, including read filtering and primer trimming metrics.
- Amplified-region and primer-identification summaries for supported 16S and 18S datasets.
- Closed-reference taxonomic profiles for SILVA PR2, UNITE, and ITSoneDB, with interactive Krona visualisations where available.
- ASV sequences, ASV read-count tables, and ASV taxonomic assignments against SILVA and PR2 when ASV analysis is supported for the inferred amplicon.

Study-level pages aggregate run-level quality-control and primer-validation information where multiple runs are available.

## Raw reads analysis pipeline

The MGnify v6 raw reads analysis pipeline ([GitHub repository](https://github.com/EBI-Metagenomics/raw-reads-analysis-pipeline)) analyses whole genome sequencing (WGS) reads, profiling their taxonomy and functions. It is designed to handle both short (paired- and single-end) and long reads, taking raw reads rather than assembled contigs or genomes as input.

### Tools and Databases Used

The raw reads analysis pipeline v6 uses the following tools and databases:

| Tool/Database | Version | Purpose |
|---|---|---|
| [bbmap](https://sourceforge.net/projects/bbmap) | 35.85 | Standardise paired-end FASTQ files |
| [fastp](https://github.com/OpenGene/fastp) | 0.24.0 | Read quality control and paired-end read merging |
| [seqtk](https://github.com/lh3/seqtk) | 1.3-r106 | FASTQ-to-FASTA conversion |
| [seqkit](https://github.com/shenwei356/seqkit) | 2.9.0 | Nucleotide-to-amino-acid sequence translation |
| [bwa-mem2](https://github.com/bwa-mem2/bwa-mem2) | 2.2.1 | Short-read mapping to decontamination reference genomes |
| [minimap2](https://github.com/lh3/minimap2) | 2.3.0 | Long-read mapping to decontamination reference genomes |
| [samtools](https://github.com/samtools/samtools) | 1.21 | FASTA/FASTQ filtering for decontamination |
| [infernal](https://github.com/EddyRivasLab/infernal) | 1.1.5 | Read mapping to rRNA covariance models using cmsearch |
| [easel](https://github.com/EddyRivasLab/easel) | 0.49 | Sequence extraction from cmsearch mapping |
| [mapseq](https://github.com/jfmrod/MAPseq) | 2.1.1b | rRNA read mapping to a reference database |
| [Krona](https://github.com/marbl/Krona) | 2.8.1 | Interactive taxonomic profile generation |
| [mOTUs](https://github.com/motu-tool/mOTUs) | 3.0.3 | Taxonomic profile generation |
| [HMMER](https://github.com/EddyRivasLab/hmmer) | 3.4 | Read mapping to Hidden Markov Models (HMMs) |
| [MultiQC](https://github.com/MultiQC/MultiQC) | 1.27 | Reports containing quality-control and decontamination information |
| [Python](https://www.python.org) | 3.11.8 | Functional profile generation |
| [cmsearch_tblout_deoverlap](https://github.com/nawrockie/cmsearch_tblout_deoverlap) | 0.09 | Resolution of reads mapping to multiple locations |
| [mgnify-pipelines-toolkit](https://github.com/EBI-Metagenomics/mgnify-pipelines-toolkit) | 1.0.4 | Contains mapseq2biom for converting mapseq output |

### Reference Databases

The pipeline uses the following reference databases:

| Reference Database | Version | Purpose |
|---|---|---|
| [mOTUs](https://motu-tool.org) | 3.0.3 | Database for mOTUs tools |
| [Rfam](https://rfam.org) | 15.0 | rRNA covariance models |
| [SILVA](https://www.arb-silva.de) | 138.1 | [LSU and SSU](glossary.md#lsu-ssu) rRNA database with taxonomy |
| [Pfam-A](https://www.ebi.ac.uk/interpro/entry/pfam) | 38.0 | Protein family Hidden Markov Models |
| [hg38](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000001405.40/) | GRCh38.p14 | Human reference genome for host decontamination |
| [phiX](https://www.ncbi.nlm.nih.gov/nuccore/9626372) | phiX174 | PhiX control sequence removed during decontamination (Illumina only) |

### Pipeline Features

The v6 raw reads analysis pipeline includes the following key features:

- Quality Control: Uses fastp for read quality filtering and BBMap for paired-end standardisation
- Long Read Support: Handles both short (Illumina) and long reads (Oxford Nanopore, PacBio) with platform-appropriate tools
- Decontamination: Removes host (human by default) and phiX contamination using bwa-mem2 (short reads) and minimap2 (long reads)
- Dual Taxonomic Profiling: Combines rRNA-based (SILVA) and marker gene (mOTUs) approaches
- Optional subsampling for functional profiling to limit computational expense
- Automated Database Management: Automatic download and caching of reference databases
- Chunking: Efficient processing of large datasets through chunking with empirically tuned resource requirements to match

### Pipeline Workflow

1. Database Management: Automatic checking, downloading, and caching of reference databases
2. Quality Control: Standardisation with BBMap and filtering with fastp
3. Decontamination: Removal of host and phiX reads using bwa-mem2 (short reads) or minimap2 (long reads)
4. Read Merging: Merging of paired-end reads for profiling steps
5. Taxonomic Profiling:
   - rRNA-based: Infernal cmsearch for rRNA extraction, followed by MAPseq mapping to SILVA SSU and LSU databases
   - Marker gene: mOTUs for comprehensive taxonomic classification
6. Functional Profiling: HMMER hmmsearch for mapping reads to Pfam-A HMMs
7. Result Generation: MultiQC reports and interactive Krona visualisations

### Results available on MGnify

For each analysed [run](glossary.md#run), MGnify displays and provides downloads for:

- Quality-control and decontamination summaries.
- Taxonomic profiles from mOTUs3, SILVA SSU, and SILVA LSU, with interactive Krona visualisations where available.
- Pfam-A functional profiles, including read-count tables and mapping statistics.

Study-level pages aggregate quality-control and analysis-status information across runs where multiple runs are available.

## Assembly analysis pipeline

The MGnify v6 [assembly](glossary.md#assembly) analysis pipeline ([GitHub repository](https://github.com/EBI-Metagenomics/assembly-analysis-pipeline)) analyses assembled [metagenomic](glossary.md#metagenomic) and [metatranscriptomic](glossary.md#metatranscriptomic) datasets, providing functional, taxonomic, pathway, and systems annotation for assembled contigs.

### Tools and Databases Used

The assembly analysis pipeline v6 uses the following tools and databases:

| Tool/Database | Version | Purpose |
|---|---|---|
| [antiSMASH](https://antismash.secondarymetabolites.org) | 8.0.1 | Secondary metabolite biosynthetic gene cluster annotation |
| [CAT_pack](https://github.com/MGXlab/CAT_pack) | 6.0 | Taxonomic classification of contigs |
| [cmsearch_tblout_deoverlap](https://github.com/nawrockie/cmsearch_tblout_deoverlap) | 0.09 | Deoverlapping of cmsearch results |
| [Combined Gene Caller](https://ebi-metagenomics.github.io/nf-modules/modules/ebi-metagenomics/combinedgenecaller/merge/) | 1.4.12 | Combined gene caller |
| [DIAMOND](https://github.com/bbuchfink/diamond) | 2.1.11 | Protein sequence-based taxonomic analysis |
| [DRAM](https://github.com/WrightonLabCSU/DRAM) | 13.5 | Summarises annotations from multiple tools |
| [easel](https://github.com/EddyRivasLab/easel) | 0.49 | Extracting sequences from cmsearch results |
| [eggNOG-mapper](https://eggnog-mapper.embl.de) | 5.0.2 | Protein function annotation |
| [Genome Properties](https://www.ebi.ac.uk/interpro/genomeproperties/) | 2.0 | Systems and pathways annotation |
| [FragGeneScanRs](https://github.com/unipept/FragGeneScanRs) | 1.1.0 | Protein coding sequence prediction |
| [HMMER](https://github.com/EddyRivasLab/hmmer) | 3.4 | KEGG Ortholog prediction |
| [Infernal - cmscan](https://github.com/EddyRivasLab/infernal) | 1.1.5 | RNA sequence searching |
| [InterProScan](https://www.ebi.ac.uk/interpro/interproscan.html) | 5.76-107.0 | [InterPro](glossary.md#interpro) protein function annotation |
| [KOfam](https://www.genome.jp/kegg/ko.html) | 2025-04 | KEGG Ortholog prediction |
| [KEGG pathways completeness](https://github.com/EBI-Metagenomics/kegg-pathways-completeness-tool) | 1.3.0 | Computes KEGG pathway module completeness |
| [Krona](https://github.com/marbl/Krona) | 2.8.1 | Visualisation of taxonomic analyses |
| [mgnify-pipelines-toolkit](https://github.com/EBI-Metagenomics/mgnify-pipelines-toolkit) | 1.2.0 | Toolkit containing various in-house processing scripts |
| [minimap2](https://lh3.github.io/minimap2/) | 2.29-r1283 | Assembly decontamination |
| [MultiQC](https://github.com/MultiQC/MultiQC) | 1.29 | Result aggregation into HTML reports |
| [Owltools](https://github.com/owlcollab/owltools) | 2024-06-12 | GO term to GO Slim mapping |
| [Pyrodigal](https://pyrodigal.readthedocs.org) | 3.6.3 | Protein coding sequence prediction |
| [QUAST](http://quast.sourceforge.net/quast) | 5.2.0 | Assembly quality assessment |
| [RHEA](https://www.rhea-db.org) | N/A | Protein reaction assignments |
| [run_dbCAN](https://github.com/bcb-unl/run_dbcan) | 5.1.2 | Carbohydrate-active enzyme annotation |
| [SanntiS](https://github.com/Finn-Lab/SanntiS) | 0.9.4.1 | Biosynthetic gene cluster identification |
| [SeqKit](https://bioinf.shenwei.me/seqkit/) | 2.8.0 | FASTA file manipulation |
| [tabix](http://www.htslib.org/doc/tabix.html) | 1.21 | Indexing compressed annotation files |
| [UniRef90](https://www.uniprot.org/help/uniref) | 2025_01 | Protein sequence-based taxonomic analysis |

### Reference Databases

The assembly analysis pipeline v6 uses the following reference databases:

| Reference Database | Version | Purpose |
|---|---|---|
| [Rfam](https://rfam.org) | 15 | rRNA covariance models |
| [InterProScan databases](https://www.ebi.ac.uk/interpro) | 5.73-104.0 | [InterPro](glossary.md#interpro) protein domain and family annotation |
| [eggNOG](https://eggnog5.embl.de) | 5.0.2 | Clusters of orthologous groups |
| [KOfam](https://www.genome.jp/kegg/ko.html) | 2025-04 | [KEGG](glossary.md#kegg) ortholog HMM profiles |
| [GO Slims](http://geneontology.org/docs/go-subset-guide/) | 20160705 | [Gene Ontology](glossary.md#go-term) mapping |
| [dbCAN](https://bcb.unl.edu/dbCAN2/) | 4.1.4-V13 | CAZy carbohydrate-active enzyme database |
| [CAT_Pack taxonomy](https://github.com/MGXlab/CAT_pack) | 2025_01 | NCBI taxonomy reference for contig classification |
| [DRAM databases](https://github.com/WrightonLabCSU/DRAM) | 1.3.0 | Metabolic annotation databases |

### Pipeline Features

- Quality Control: The pipeline performs quality control on assembled contigs, including optional decontamination to remove human, PhiX, and custom contaminant sequences using [minimap2](https://lh3.github.io/minimap2/). Quality assessment is performed using [QUAST](http://quast.sourceforge.net/quast).

- CDS Prediction: [Protein coding sequences](glossary.md#predicted-coding-sequence-pcds) are predicted using the [MGnify Combined Gene Caller](https://ebi-metagenomics.github.io/nf-modules/modules/ebi-metagenomics/combinedgenecaller/merge/), which combines predictions from [Pyrodigal](https://pyrodigal.readthedocs.org/) and [FragGeneScanRs](https://github.com/unipept/FragGeneScanRs).

- Taxonomic Assignment: Contigs are taxonomically classified using [CAT_pack](https://github.com/MGXlab/CAT_pack), which uses DIAMOND to match predicted CDS against reference databases. Additionally, rRNA sequences are identified using [Infernal](http://eddylab.org/infernal/) with Rfam covariance models.

- Functional Annotation:
  - [InterProScan](https://www.ebi.ac.uk/interpro/interproscan.html) identifies protein domains, families, repeats, structural features, disorder, signal peptides, and functional sites by scanning predicted proteins with a broad set of member analyses: `TIGRFAM`, `SFLD`, `SUPERFAMILY`, `GENE3D`, `HAMAP`, `COILS`, `CDD`, `PRINTS`, `PIRSF`, `PROSITEPROFILES`, `PROSITEPATTERNS`, `PFAM`, `MOBIDBLITE`, `SMART`, and `SIGNALP`. It is run with `--goterms` and `--pathways` to include Gene Ontology and pathway annotations. See the [InterProScan included analyses documentation](https://interproscan-docs.readthedocs.io/en/v5/HowToRun.html#included-analyses).
  - [eggNOG-mapper](https://eggnog-mapper.embl.de/) assigns clusters of orthologous groups ([COGs](glossary.md#cog)), annotations, and functional descriptions
  - [run_dbCAN](https://github.com/bcb-unl/run_dbcan) annotates carbohydrate-active enzymes
  - [KEGG Orthologs](https://www.genome.jp/kegg/ko.html) are assigned using HMMER
  - [RHEA](https://www.rhea-db.org/) reactions are assigned to proteins
  - [Gene Ontology (GO) terms](glossary.md#go-term) are extracted and mapped to metagenomics [GO Slims](glossary.md#go-slim)

- Biosynthetic Gene Cluster Annotation: The pipeline uses both [antiSMASH](https://antismash.secondarymetabolites.org/) and [SanntiS](https://github.com/Finn-Lab/SanntiS) to identify and annotate biosynthetic gene clusters associated with secondary metabolite production.

- Pathway and System Analysis:
  - [KEGG](glossary.md#kegg) pathway completeness is computed using the [kegg-pathways-completeness-tool](https://github.com/EBI-Metagenomics/kegg-pathways-completeness-tool)
  - [Genome Properties](https://www.ebi.ac.uk/interpro/genomeproperties/) provides inference of higher-level pathways and systems
  - [DRAM](https://github.com/WrightonLabCSU/DRAM) generates comprehensive metabolic summaries and visualisations

- Consolidated Annotation: All annotations are aggregated into a single consolidated GFF file for easy integration with genome browsers and other tools.

### Pipeline Workflow

1. Quality Control: Assembly FASTA data are filtered to remove contigs shorter than 500 bases and those with high N-base content.

2. Decontamination (Optional): Contigs can be screened against reference genomes to remove potential contaminants.

3. Gene Prediction: The combined gene caller identifies protein-coding sequences in the assembled contigs.

4. Taxonomic Annotation: Contigs are classified taxonomically using CAT_pack, and rRNA sequences are identified for additional taxonomic validation.

5. Functional Annotation: Predicted proteins undergo comprehensive functional annotation using multiple tools.

6. Biosynthetic Gene Cluster Detection: Both antiSMASH and SanntiS are used to identify potential secondary metabolite production pathways.

7. Pathway Analysis: KEGG module completeness is calculated, and Genome Properties are inferred.

8. DRAM Integration: DRAM provides metabolic summaries and visualisations.

9. Output Generation: All annotations are consolidated into standardised output formats.

### Results available on MGnify

For each analysed [assembly](glossary.md#assembly), MGnify displays and provides downloads for:

- Filtered contigs, assembly quality statistics, and quality-control summaries.
- Predicted coding sequences and consolidated GFF3 annotations.
- Taxonomic assignments for contigs, plus rRNA marker gene sequences where detected.
- Functional annotation summaries from InterProScan, Pfam, Gene Ontology, eggNOG-mapper, KEGG, RHEA, and dbCAN.
- Pathway and systems summaries, including KEGG module completeness, Genome Properties, DRAM metabolism summaries, and biosynthetic gene cluster predictions from antiSMASH and SanntiS.

Assembly analysis results are shown alongside linked VIRify and Mobilome annotations where those additional analyses are available.

## VIRify

[VIRify](https://github.com/EBI-Metagenomics/emg-viral-pipeline) is run on assembled contigs after the assembly analysis pipeline and is accessible in the same web view. It detects, annotates, and taxonomically classifies viral sequences in [metagenomic](glossary.md#metagenomic) and [metatranscriptomic](glossary.md#metatranscriptomic) assemblies. Taxonomy assignment uses a curated collection of viral orthologous protein domains (ViPhOGs).

### Tools Used

| Tool | Purpose |
|---|---|
| [VirSorter2](https://github.com/jiarong/VirSorter2) | Viral contig prediction |
| [VirFinder](https://github.com/jessieren/VirFinder) | Viral contig prediction |
| [PPR-Meta](https://github.com/zhenchengfang/PPR-Meta) | Viral contig prediction |
| [Prodigal](https://github.com/hyattpd/Prodigal) | Protein-coding sequence prediction |
| [HMMER](https://github.com/EddyRivasLab/hmmer) | ViPhOG domain matching for taxonomy assignment |
| [CheckV](https://bitbucket.org/berkeleylab/checkv) | Viral sequence quality assessment |

### Pipeline Workflow

1. Viral contig prediction using VirSorter2, VirFinder, and PPR-Meta
2. Protein-coding sequence prediction on viral contigs using Prodigal
3. HMM-based annotation using ViPhOG protein domain profiles
4. Taxonomic classification based on ViPhOG matches
5. Quality evaluation using CheckV
6. Visualisation using Krona and Sankey plots

### Results available on MGnify

- Annotated viral contigs in FASTA format
- GFF files with sequence ontology-compliant annotations
- Taxonomic assignments
- Krona and Sankey interactive visualisations
- Quality metrics from CheckV

## Mobilome annotation pipeline

The [Mobilome annotation pipeline](https://github.com/EBI-Metagenomics/mobilome-annotation-pipeline) is run after VIRify as part of the assembly analysis bundle. It predicts and annotates mobile genetic elements (MGEs) — including plasmids, phages, insertion sequences, and integrative conjugative elements — in prokaryotic genomes and metagenomes, outputting results in GFF3 format. VIRify results are incorporated into the mobilome annotation.

### Tools Used

| Tool | Version | Purpose |
|---|---|---|
| [geNomad](https://github.com/apcamargo/genomad) | 1.11.1 | Plasmid and phage prediction |
| [ICEfinder](https://bioinfo-mml.sjtu.edu.cn/ICEfinder/) | 2.0 | Integrative conjugative element detection |
| [IntegronFinder2](https://github.com/gem-pasteur/Integron_Finder) | 2.0.6 | Integron identification |
| [ISEScan](https://github.com/xiezhq/ISEScan) | 1.7.3 | Insertion sequence detection |
| [Prodigal](https://github.com/hyattpd/Prodigal) | 2.6.3 | Protein-coding sequence prediction |

### Reference Databases

| Reference Database | Version | Purpose |
|---|---|---|
| geNomad database | 1.9 | Reference database for plasmid and phage prediction |
| ICEfinder2 databases | N/A | MacSyFinder models, HMM models, and UniProt reference sequences |

### Pipeline Workflow

1. Preprocessing: Contig filtering and protein-coding sequence prediction
2. Prediction: Concurrent execution of geNomad, ICEfinder2, IntegronFinder2, and ISEScan, plus compositional outlier detection for contigs >100 kb
3. Integration: Results parsing and incorporation of VIRify output; fragments <500 bp and elements lacking genes are filtered out
4. Postprocessing: GFF validation and output compression

### Results available on MGnify

- `mobilome.gff.gz`: Integrated MGE annotations in GFF3 format
- `mobilome.fasta`: Sequence records for all predicted mobile genetic elements
