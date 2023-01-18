# Glossary

    Study
        Represents a collection of :term:`samples<sample>` and experiments applied to these :term:`samples<sample>`.


    Sample
        A representation of the physical amount of material collected. It represents a specimen of a :term:`biome`.


    Run
        The sequence file obtained from performing an experiment (an experiment generally includes several steps such as filtration, metatranscriptomic extraction and Illumina MiSeq sequencing, for example) on all or part of a :term:`sample`. Several runs can therefore be generated from a single :term:`sample`.


    Analysis result
        The end result of the :term:`pipeline` analysis of a :term:`run`.


    Biome
        An ecological community type. In MGnify, :term:`biomes<biome>` are organised hierarchically going from large types (such as soil, host-associated or aquatic) to more precise types (such as forest soil, skin or coastal) based on the `GOLD classification <https://gold.jgi.doe.gov/distribution#Classification>`_.


    Pipeline
        A prescribed set of successive steps needed to transform an input (raw reads and contigs for MGnify) into an output with added information (annotated files with taxonomy and functional assignments for MGnify) 
        
        
    Pipeline tool	
        A software or script used during the individual step of an analysis pipeline.


    GO term
        A defined vocabulary term to represent the functional attributes of a protein. Defined by the the `Gene Ontology <http://geneontology.org/>`_ initiative, GO terms are organised hierarchically to unambiguously define the biological process, precise molecular function or cellular location of a protein.


    GO slim
        A GO slim is a cut-down version of the GO hierarchy to give an overview of the functional results. It is used on MGnify website. The GO slim hierarchy lacks the fine granularity of the full GO hierarchy.


    InterPro
        Combines protein signatures from a number of member databases into a single searchable resource, capitalising on their individual strengths to produce a powerful integrated database and diagnostic tool.


    Metagenomic
        Refers to environmental sample where Whole Genome Shotgun sequencing method has been applied. Analysis will yield taxonomic and functional information.


    Metatranscriptomic
        Refera to environmental sample where whole transcriptome sequencing method has been applied. Analysis will yield taxonomic and functional information.


    Amplicon
        Refers to environmental sample where a marker gene has been amplified and sequenced. On the EMG website, we use the term amplicon when the amplified marker gene is ribosomal RNA gene. Analysis will yield taxonomic information.


    Assembly
        Refers to environmental sample where Whole Genome Shotgun sequencing reads have been assembled to form larger fragments called contigs. Analysis will yield taxonomic and functional information.


    Metabarcoding
        Refers to environmental sample where a marker gene, different from ribosomal RNA gene, has been amplified and sequenced. Analysis will yield taxonomic information.


    Predicted coding sequence (pCDS)
        Partial or complete gene sequence as predicted by the gene caller (FragGenScan for read submissions, Prodigal and FragGenScan for assembly submissions).


    16S rRNA genes
        Main prokaryotic ribosomal RNA genes used for taxonomic assignments. 


    18S rRNA genes
        Main eukaryotic ribosomal RNA genes used for taxonomic assignments.


    OTU
        Operational Taxonomic Unit representing a group of sequences sharing high similarity with each other.


    LSU, SSU
        Clusters of Large and Small Subunit ribosomal RNA genes. LSU comprises 23S (for prokaryotes) and 28S (for eukaryotes) sequences while the SSU represents 16S (for prokaryotes) and 18S (for eukaryotes) sequences.


    MAGs
        Metagenome assembled genomes are binned or de-replicated metagenome assemblies belonging to one taxon.


    Pan-genome
        The entire set of genes (core and accessory) within a species.


    KEGG
        Kyoto Encyclopedia of Genes and Genomes - a database used to assign high level functional and pathway annotations.


    COG
        Cluster of Orthologous Groups of proteins - a database of groups of proteins inferred by orthology.


    ITS
        The internal transcribed spacers are regions situated between the :term:`LSU and SSU<LSU, SSU>` genes.


