# Analysis pipeline v5.0

## Overview

The latest MGnify analysis service (version 5.0) offers specialised workflows for three different data types: [amplicon](glossary.md#term-Amplicon), raw [metagenomic](glossary.md#term-Metagenomic)/[metatranscriptomic](glossary.md#term-Metatranscriptomic) reads, and [assembly](glossary.md#term-Assembly). Each workflow is defined in common workflow language ([CWL](https://figshare.com/articles/Common_Workflow_Language_draft_3/3115156/2)). ([MGnify v5.0 CWL repository](https://github.com/EBI-Metagenomics/pipeline-v5))
All databases are available from an [FTP link](ftp://ftp.ebi.ac.uk/pub/databases/metagenomics/pipeline-5.0/ref-dbs)

The software and databases used for the various processing steps and analyses are listed in the following table.

## Software, Databases and Versions used by MGnify:

| **Tool/Database**

 | **Version**

 | **Purpose**

 | **Amplicon**

 | **Raw reads**

 | **Assemblies**

 |
| SeqPrep

       | *1.2*

     | Merging paired end reads

 | Yes

      | Yes

       |            |
| Trimmomatic

   | *0.36*

    | Quality control

          | Yes

      | Yes

       |            |
| Biopython

     | *1.74*

    | Quality control

          | Yes

      | Yes

       | Yes

        |
| bedtools

      | *2.28.0*

  | SSU/LSU rRNA masking for ITS

 | Yes

      |           |            |
| Easel

         | *0.45h*

   | Sequence extraction

          | Yes

      | Yes

       | Yes

        |
| Infernal

      | *1.1.2*

   | RNA prediction

               | Yes

      | Yes

       | Yes

        |
| Rfam

          | *13.0*

    | Identification of SSU/LSU rRNA and other ncRNA

 | Yes

      | Yes

       | Yes

        |
| MAPseq

        | *1.2.3*

   | Taxonomic assignment of SSU/LSU rRNA and ITS

   | Yes

      | Yes

       | Yes

        |
| Kronatools

    | *2.7.1*

   | Visualisation of taxonomic analyses

            | Yes

      | Yes

       | Yes

        |
| biom-format

   | *2.1.6*

   | Formatting of taxonomic analyses

               | Yes

      | Yes

       | Yes

        |
| mOTUs2

        | *2.5.1*

   | Phylogenetic marker gene based taxonomic profiling

 |          | Yes

       |            |
| FragGeneScan

  | *1.20*

    | Protein coding sequence prediction

                 |          | Yes

       | Yes

        |
| Prodigal

      | *2.6.3*

   | Protein coding sequence prediction

                 |          |           | Yes

        |
| InterProScan

  | *75.0*

    | Protein function annotation with separate Pfam results

 |          | Yes

       | Yes

        |
| GO terms in-house scripts

 | *N/A*

     | Assign gene ontology terms

                             |          | Yes

       | Yes

        |
| eggNOG

                    | *4.5.1*

   | Protein function annotation

                            |          |           | Yes

        |
| eggNOG-mapper

             | *1.0.3*

   | Protein function annotation

                            |          |           | Yes

        |
| HMMER

                     | *3.2.1*

   | KEGG Ortholog prediction

                               |          | Yes

       | Yes

        |
| KOfam - a modified version based on KEGG 90.0

 | *2019-04-06*

 | KEGG Ortholog prediction

                               |          | Yes

       | Yes

        |
| KEGG and in-house scripts

                     | *90.0*

       | KEGG pathway predictions

                               |          |           | Yes

        |
| Genome Properties

                             | *2.0.1*

      | Systems and pathways annotation

                        |          |           | Yes

        |
| antiSMASH

                                     | *4.2.0*

      | Secondary metabolite biosynthetic gene cluster annotation

 |          |           | Yes

        |
| DIAMOND

                                       | *0.9.25.126*

 | Protein sequence-based taxonomic analysis

                 |          |           | Yes

        |
| SILVA release

                                 | *132*

        | SSU/LSU rRNA taxonomic database

                           | Yes

      | Yes

       | Yes

        |
| ITSoneDB

                                      | *1.138*

      | ITS1 taxonomic database

                                   | Yes

      |           |            |
| UNITE

                                         | *8.0*

        | ITS taxonomic database

                                    | Yes

      |           |            |
| UniRef90

                                      | *2019_11*

    | Protein sequence-based taxonomic analysis

                 |          |           | Yes

        |
| metaSPAdes

                                    | *3.13*

       | Assembly of raw reads (available on request)

              | N/A

      | N/A

       | N/A

        |
## Amplicon analysis pipeline

Amplicon reads are merged with SeqPrep (where appropriate) and filtered with Trimmomatic to trim sequence regions with an average Phred 33 quality score of less than 15 in a sliding window of 4 base pairs. This is followed by removal of reads less than 100bp in length. An additional Biopython filtering step removes reads with more than 10% ambiguous bases.
[Infernal](http://europepmc.org/abstract/MED/24008419) (running in hmm-only mode) using a library of ribosomal RNA hidden Markov models from [Rfam](http://europepmc.org/articles/PMC4383904) is run to identify large and small subunit ribosomal ribonucleic acid ([LSU and SSU rRNA](glossary.md#term-LSU-SSU)) genes, using families found in the following clans: CL00111 (SSU) and CL00112 (LSU). Theses undergo taxonomic classification using the [SILVA](https://academic.oup.com/nar/article/41/D1/D590/1069277) database in conjunction with [MAPSeq](https://academic.oup.com/bioinformatics/article/33/23/3808/4082276)  which offers fast and accurate classification of reads, and provides corresponding confidence scores for assignment at each taxonomic level.

MGnify can also provide analysis of ITS ([internal transcribed spacer](glossary.md#term-ITS)) amplicons. ITS1 and ITS2 reside between the LSU and SSU genes and can be targeted for accurate classification of eukaryotic organisms. ITS taxonomy is assigned by MAPseq using two reference databases: [ITSoneDB](https://academic.oup.com/nar/article/46/D1/D127/4210943)  containing ITS1 sequences and [UNITE](https://academic.oup.com/nar/article/47/D1/D259/5146189) containing ITS1 and ITS2 sequences. The SSU and LSU regions are masked using Rfam, as described above, prior to ITS classification, minimising cross reactivity.

**Figure 1**. Overview of the main steps in the amplicon workflow.

## Raw reads analysis pipeline

Metagenomic and metatranscriptomic raw reads undergo merging, quality control and SSU/LSU based taxonomic analysis, as described for the amplicon pipeline above.
Additional non-coding RNAs (ncRNAs) are identified with Infernal, using families from the following Rfam clans: CL00001 (tRNA), CL00002 (RNAse) and CL00003 (SRP).
Supplementary phylogenetic classification based on marker gene profiling, is performed using [mOTUs2](https://www.nature.com/articles/s41467-019-08844-4) on the quality controlled reads.

For functional analysis, the sequence regions encoding rRNAs are masked, and [FragGeneScan](https://academic.oup.com/nar/article/38/20/e191/1317565) is used to predict coding sequences (pCDS). Coding sequences are assigned protein annotations with InterProScan, using 5 member databases that are able to process large numbers of potentially fragmented sequences (Gene3D, TIGRFAMs, Pfam, PRINTS and PROSITE patterns). Pfam annotations are provided as separate visualisations and downloads. GO terms are extracted from the InterProScan results and grouped according to category (Biological Process, Molecular Function and Cellular Component). GO terms are also summarized using a specialized [GO Slim](http://www.geneontology.org/ontology/subsets/goslim_metagenomics.obo) developed for metagenomic data. Finally, protein coding sequences undergo KEGG ortholog annotations using HMMER v3.2.1 and a modified version of KOfam 2019-04-06 (based on KEGG 90.0).

**Figure 2**. Overview of the main steps in the raw reads workflow.

## Assembly analysis pipeline

Users can request assembly of their own raw sequencing reads, or publicly available datasets, using the ‘Request analysis’ section of the [MGnify home page](https://www.ebi.ac.uk/metagenomics/). Users own raw reads (with host sequences removed) must be archived in ENA before submitting an assembly request. The sequences then undergo quality control, as well as a precautionary additional host contamination removal process (where applicable) with bwa-mem. [metaSPAdes](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5411777/) is used for assembly of paired end reads and [SPAdes](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3342519/) for single reads. Alternatively, pre-assembled datasets, including those produced using other assembly algorithms, can be analysed. Quality control for assemblies is based on sequence length, with contigs less than 500 nucleotides removed from the analysis process.

rRNAs are identified and undergo taxonomic analysis as for raw reads above. Sequence regions encoding rRNAs are masked and protein coding sequences are predicted using a combined gene caller that utilises both [Prodigal](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-11-119) and FragGeneScan. In addition to rRNA-based taxonomic analyses, [DIAMOND](https://www.nature.com/articles/nmeth.3176) is used to assign taxonomy to protein sequences, based on the top hit to the [UniRef90](https://academic.oup.com/bioinformatics/article/31./6/926/214968) database.

Protein function is assigned in the form of InterProScan annotations, GO terms, and [KEGG](glossary.md#term-KEGG) ortholog predictions, as described for the raw reads analysis pipeline above.
Additionally, clusters of orthologous groups ([COGs](glossary.md#term-COG)) annotations and eggNOG functional descriptions are provided by the [eggNOG-mapper tool](https://www.biorxiv.org/content/10.1101/076331v1.full).

KEGG ortholog annotations are further processed to produce KEGG pathway information, including module presence and completeness. Similarly, InterPro annotations for individual protein sequences are amalgamated to generate [Genome Properties](https://academic.oup.com/nar/article/47/D1/D564/5144958) (GP), providing inference of higher level pathways and systems that may be present in the dataset. Finally, [antiSMASH](https://academic.oup.com/nar/article/45/W1/W36/3778252) is used to identify and annotate biosynthetic gene clusters that code for the production of secondary metabolites.

**Figure 3**. Overview of the main steps in the assembly workflow.
