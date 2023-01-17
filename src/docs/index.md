<!-- EMG-docs documentation master file, created by
sphinx-quickstart on Tue Jun 13 14:20:37 2017.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive. -->
# MGnify documentation

# Contents:


* [About](about.md)


    * [The MGnify service](about.md#the-mgnify-service)


    * [What does MGnify offer](about.md#what-does-mgnify-offer)


    * [Funding](about.md#funding)


    * [How to cite](about.md#how-to-cite)


    * [Contact](about.md#contact)


    * [News and updates](about.md#news-and-updates)


    * [Service status](about.md#service-status)


* [Data flow from submission to results](dataflow.md)


* [Analysis pipeline v5.0](analysis.md)


    * [Overview](analysis.md#overview)


    * [Amplicon analysis pipeline](analysis.md#amplicon-analysis-pipeline)


    * [Raw reads analysis pipeline](analysis.md#raw-reads-analysis-pipeline)


    * [Assembly analysis pipeline](analysis.md#assembly-analysis-pipeline)


* [Website and portal](portal.md)


    * [Sections of the MGnify website](portal.md#sections-of-the-mgnify-website)


        * [Text Search](portal.md#text-search)


        * [Browse Data](portal.md#browse-data)


        * [Submit or request data, and My Data](portal.md#submit-or-request-data-and-my-data)


        * [API](portal.md#id1)


    * [Organisation and access of data on the MGnify website](portal.md#organisation-and-access-of-data-on-the-mgnify-website)


        * [Super Studies](portal.md#super-studies)


        * [Studies](portal.md#studies)


        * [Samples](portal.md#samples)


        * [Publications](portal.md#publications)


        * [Genomes](portal.md#genomes)


    * [Viewing metadata for MGnify Samples, Studies, Publications](portal.md#viewing-metadata-for-mgnify-samples-studies-publications)


        * [Sample metadata from ENA](portal.md#sample-metadata-from-ena)


        * [Sample metadata from BioSamples](portal.md#sample-metadata-from-biosamples)


        * [Sample metadata from the Elixir Contextual Data Clearing House](portal.md#sample-metadata-from-the-elixir-contextual-data-clearing-house)


        * [Additional metadata from text-mining on Publications](portal.md#additional-metadata-from-text-mining-on-publications)


    * [Content of the ‘Associated runs’ table on project page](portal.md#content-of-the-associated-runs-table-on-project-page)


    * [Finding quality control information about runs on the MGnify website](portal.md#finding-quality-control-information-about-runs-on-the-mgnify-website)


    * [Finding functional information about runs on the MGnify website](portal.md#finding-functional-information-about-runs-on-the-mgnify-website)


    * [Finding pathways/systems information about runs on the MGnify website](portal.md#finding-pathways-systems-information-about-runs-on-the-mgnify-website)


    * [Viewing functional annotation per contig](portal.md#viewing-functional-annotation-per-contig)


    * [Finding taxonomic information about runs on the MGnify website](portal.md#finding-taxonomic-information-about-runs-on-the-mgnify-website)


    * [Files available to download on the MGnify website](portal.md#files-available-to-download-on-the-mgnify-website)


        * [Description of fasta files available to download](portal.md#description-of-fasta-files-available-to-download)


        * [Description of functional annotation files available to download](portal.md#description-of-functional-annotation-files-available-to-download)


        * [Description of pathway and system annotation files available to download](portal.md#description-of-pathway-and-system-annotation-files-available-to-download)


        * [Description of taxonomic assignment files available to download](portal.md#description-of-taxonomic-assignment-files-available-to-download)


    * [Summary files](portal.md#summary-files)


    * [Data discovery on MGnify portal](portal.md#data-discovery-on-mgnify-portal)


        * [Text search](portal.md#id2)


        * [Browsing options](portal.md#browsing-options)


    * [Private area](portal.md#private-area)


* [RESTful API](api.md)


    * [API Overview](api.md#api-overview)


        * [Current version](api.md#current-version)


        * [Base URL](api.md#base-url)


        * [The Browsable API](api.md#the-browsable-api)


        * [HTTP methods](api.md#http-methods)


        * [Response](api.md#response)


        * [Hypermedia](api.md#hypermedia)


        * [Pagination](api.md#pagination)


        * [Parameters](api.md#parameters)


        * [Customising queries: compound documents](api.md#customising-queries-compound-documents)


        * [Errors](api.md#errors)


        * [Cross Origin Resource Sharing](api.md#cross-origin-resource-sharing)


    * [Examples](api.md#examples)


    * [Interactive documentation](api.md#interactive-documentation)


* [MGnify Notebooks Server](notebooks.md)


    * [A Jupyter Lab environment for the MGnify API](notebooks.md#a-jupyter-lab-environment-for-the-mgnify-api)


        * [Short video tutorial](notebooks.md#short-video-tutorial)


        * [About the notebooks.mgnify.org resource](notebooks.md#about-the-notebooks-mgnify-org-resource)


        * [Use cases for the Notebooks Server](notebooks.md#use-cases-for-the-notebooks-server)


        * [MGnifyR: an R package for accessing MGnify](notebooks.md#mgnifyr-an-r-package-for-accessing-mgnify)


        * [Using a Jupyter Notebook](notebooks.md#using-a-jupyter-notebook)


        * [Jumping to a Notebook from the MGnify website](notebooks.md#jumping-to-a-notebook-from-the-mgnify-website)


        * [Using the notebooks on your own computer instead](notebooks.md#using-the-notebooks-on-your-own-computer-instead)


* [Sequence search](sequence-search.md)


    * [Landing page](sequence-search.md#landing-page)


    * [Result page](sequence-search.md#result-page)


    * [Build process](sequence-search.md#build-process)


    * [Partial and full length peptides](sequence-search.md#partial-and-full-length-peptides)


    * [Availability](sequence-search.md#availability)


    * [Further information](sequence-search.md#further-information)


* [MGnify Genomes](genome-viewer.md)


    * [Genome Catalogues](genome-viewer.md#genome-catalogues)


    * [Generating genome catalogues](genome-viewer.md#generating-genome-catalogues)


        * [Updating an existing catalogue](genome-viewer.md#updating-an-existing-catalogue)


    * [Searching across catalogues](genome-viewer.md#searching-across-catalogues)


        * [By accession or taxonomy](genome-viewer.md#by-accession-or-taxonomy)


        * [By gene fragment](genome-viewer.md#by-gene-fragment)


        * [By whole genome /  MAG](genome-viewer.md#by-whole-genome-mag)


    * [Browsing a catalogue](genome-viewer.md#browsing-a-catalogue)


        * [Searching a catalogue](genome-viewer.md#searching-a-catalogue)


    * [Genome detail](genome-viewer.md#genome-detail)


        * [Genome annotation browser](genome-viewer.md#genome-annotation-browser)


    * [Pan-genome](genome-viewer.md#pan-genome)


* [Guides and Tutorials](tutorials.md)


    * [MGnify and EMBL-EBI online tutorials](tutorials.md#mgnify-and-embl-ebi-online-tutorials)


    * [ENA online guides](tutorials.md#ena-online-guides)


* [FAQs](faqs.md)


    * [What kind of sequence data does the service accept?](faqs.md#what-kind-of-sequence-data-does-the-service-accept)


    * [Can I submit assembled metagenomic sequences for analysis?](faqs.md#can-i-submit-assembled-metagenomic-sequences-for-analysis)


    * [Can I submit ITS amplicon sequences?](faqs.md#can-i-submit-its-amplicon-sequences)


    * [Can I submit viral sequences?](faqs.md#can-i-submit-viral-sequences)


    * [How do I run a sequence search against the metagenomics datasets?](faqs.md#how-do-i-run-a-sequence-search-against-the-metagenomics-datasets)


    * [Can I change the release date of my project?](faqs.md#can-i-change-the-release-date-of-my-project)


    * [How long will it take for my data to be analyzed?](faqs.md#how-long-will-it-take-for-my-data-to-be-analyzed)


    * [I have submitted my data - how do I trigger the analysis?](faqs.md#i-have-submitted-my-data-how-do-i-trigger-the-analysis)


    * [Do you have an API?](faqs.md#do-you-have-an-api)


    * [How can I download multiple sets of data?](faqs.md#how-can-i-download-multiple-sets-of-data)


    * [How can I bulk download metadata?](faqs.md#how-can-i-bulk-download-metadata)


    * [How can I re-analyse my data with a different version of the pipeline?](faqs.md#how-can-i-re-analyse-my-data-with-a-different-version-of-the-pipeline)


    * [Can I request that a dataset is analyzed if I am not the original submitter?](faqs.md#can-i-request-that-a-dataset-is-analyzed-if-i-am-not-the-original-submitter)


    * [Can I request my data to not be analyzed by MGnify?](faqs.md#can-i-request-my-data-to-not-be-analyzed-by-mgnify)


    * [Can I compare the taxonomic assignments between runs of a project?](faqs.md#can-i-compare-the-taxonomic-assignments-between-runs-of-a-project)


    * [Can I know which bacteria encodes particular pCDS in my dataset?](faqs.md#can-i-know-which-bacteria-encodes-particular-pcds-in-my-dataset)


* [Glossary](glossary.md)


# Indices and tables


* [Index](genindex.md)


* [Module Index](py-modindex.md)


* [Search Page](search.md)


* [Glossary](glossary.md#glossary)
