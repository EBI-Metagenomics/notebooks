# FAQs

## What kind of sequence data does the service accept?

MGnify accepts sequencing data from a wide range of platforms, including Roche 454, Illumina and Ion Torrent. In addition to analysis of whole-genome shotgun (WGS) assemblies, sequenced metagenomic and metatranscriptomic samples, it also provides analysis of 16S and 18S ribosomal RNA (rRNA) amplicon data. We do not currently support analysis of long read data. We are in the process of expanding our assembly pipeline to make this available to users in the future.

## Can I submit assembled metagenomic sequences for analysis?

Yes, we welcome submission of assembled data.

## Can I submit ITS amplicon sequences?

Yes, the v5.0 analysis pipeline classifies ITS sequences for amplicon studies based on two databases: UNITE and ITSoneDB

## Can I submit viral sequences?

Although MGnify does not currently provide taxonomic analysis of viral sequences, any reads submitted to the pipeline that encode predicted protein coding sequences (pCDS) undergo functional analysis using InterPro. Therefore, while no taxonomic data will be returned for viral sequences, it should be possible to obtain functional analysis results. We hope to make specific viral analysis available in the near future.

## How do I run a sequence search against the metagenomics datasets?

We offer HMMER searches against our metagenomic protein database via the web site [sequence search facility](https://www.ebi.ac.uk/metagenomics/sequence-search/search/phmmer).

## Can I change the release date of my project?

The date of release is set by you during the submission in ENA. If you do not explicitly choose a date, it is set to two years from the submission date by default. You can reduce or extend the release date by going to the ‘Submit & update’ page of the ENA website, logging in using your Webin account id, selecting the relevant study and then clicking the pen icon near the current release date to alter it.

## How long will it take for my data to be analyzed?

We aim to analyze submitted data as quickly as possible. However, submitted data are only available to us once they have been validated and archived by ENA. This process takes at least 24 hours, and in some cases several days. Once the sequence files are made available, the analysis time depends on our current analysis backlog, and the size and number of runs in the project you have submitted. Most studies will be validated, archived and analysed within two weeks. If you are concerned that your data is taking a long time to be analysed, please [contact us](https://www.ebi.ac.uk/about/contact/support/metagenomics).

## I have submitted my data - how do I trigger the analysis?

There is no manual way to trigger analysis. If you have provided [access agreement](https://www.ebi.ac.uk/metagenomics/submit) for MGnify, we will pick up your sequences from ENA automatically and queue them for analysis.
Access agreements previously provided to EBI Metagenomics will apply to MGnify.

## Do you have an API?

Yes, we do. In December 2017 we released the first version of our new [RESTful API](api.md#restapi), which provides a rich search and retrieval interface for programmatic access to our data.

## How can I download multiple sets of data?

While our API currently does not support this, we have Python scripts allowing users to automatically download most processed files from the MGnify website. The scripts and instructions for bulk downloading from the resource can be found [here](https://github.com/ProteinsWebTeam/ebi-metagenomics/wiki/Downloading-results-programmatically).

## How can I bulk download metadata?

It is possible to access all the metadata associated with projects, samples and runs programmatically using our [RESTful API](api.md#restapi).

## How can I re-analyse my data with a different version of the pipeline?

It is possible to analyse data sets with different versions of our analysis pipeline. The original analyses are not deleted and are available side by side on our website. Users interested in having data re-analysed should [contact](https://www.ebi.ac.uk/about/contact/support/metagenomics) us.

## Can I request that a dataset is analyzed if I am not the original submitter?

We are currently working through the analysis of all publicly available metagenomic datasets in ENA, so if there is a publicly available study that you would like to see analysed in MGnify, please get in touch and we will prioritise it.

## Can I request my data to not be analyzed by MGnify?

We can only access private data for analysis if you give us permission to do so. If, for any reason, you do not want MGnify to analyze one of your datasets, please [contact us](https://www.ebi.ac.uk/about/contact/support/metagenomics) .
If your data is public in ENA, we are able to analyse this data without restriction.

## Can I compare the taxonomic assignments between runs of a project?

Please refer to the summary files provided on the project page under the ‘Analysis summary’ tab. They summarize the counts per feature across the runs and provide an easy way to identify patterns.

The ‘OTUs, reads and taxonomic assignments.tsv’ can be directly imported into  [Megan 6](http://ab.inf.uni-tuebingen.de/software/megan6/) to perform comparison and visualisation. The Biom format can also be imported into third-party tools.

## Can I know which bacteria encodes particular pCDS in my dataset?

The short answer is that it is generally not possible. The reason is that we annotate directly the reads and select the reads containing small subunit rRNA and large subunit rRNA for taxonomy assignments. The protein prediction is then performed on all reads after masking the tRNA and rRNA sequences. To link a predicted protein to a taxonomic assignments, the protein-coding gene would need to be on the same read as the annotated SSU/LSU sequence. It is possible to check if this is the case using the sequence headers from the ‘InterPro matches.tsv’ and ‘Reads encoding SSU/LSU rRNA.fasta’ files, both available on the ‘Download’ for each run.
The same answer applies for assembly. However, depending on the contig length, more protein-coding genes may be located near the 16S rRNA genes.
