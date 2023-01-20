---
title: Dataflow from submission to results
author: 
  - name: MGnify Team
    url: https://www.ebi.ac.uk/metagenomics
    affiliation: EMBL-EBI
    affiliation-url: https://www.ebi.ac.uk
date: last-modified
citation: true
description: How MGnify data moves from submission to analysis
---
![MGnify data flow from submission to [analysis results](glossary.md#Analysis%20result).](images/dataflow/submit_graph_08_web032.png){#fig-dataflow-process}

1. Register
: Submissions are handled by the** [European Nucleotide Archive (ENA)](https://www.ebi.ac.uk/ena/) **and therefore users must have an ENA** [Webin account](https://www.ebi.ac.uk/ena/submit/sra/). In addition, users submitting private data must provide an expressed agreement that MGnify can access their data for analysis, as described under [Submit data](https://www.ebi.ac.uk/metagenomics/submit). Otherwise, we will not be able to access their data. MGnify will, of course, handle this data confidentially.

2. Login
: Access to the** [ENA submission page](https://www.ebi.ac.uk/ena/submit/sra/) **requires a login using a registered email address or a Webin identifier (Webin-XXXX).**

3. Upload, and 4. Submission
: These steps are described in detail in the [ENA online guides](tutorials.md#ena-online-guides). The [MGnify and EMBL-EBI online tutorials](tutorials.md#mgnify-and-embl-ebi-online-tutorials) provide a step by step guide to submission. Please also check our [FAQs](faqs.md#faq).

::: {.callout-note}
All queries concerning data submission should be directed to [ENA dedicated help desk](https://www.ebi.ac.uk/ena/browser/support)
:::

**The following ENA submission criteria must be fulfilled. Please note, MGnify will not have access to retrieve data for analyses until these criteria are met.**

* **Assemblies:**
	The associated sample taxonomy must be in the metagenomic tax tree 408169. Please see the [environmental taxonomy](https://ena-docs.readthedocs.io/en/latest/faq/taxonomy.html#environmental-taxonomic-classifications) guidelines for further details.

* **Raw metagenomic or metatranscriptomic reads:**
	Same taxonomy guidelines as assemblies apply AND/OR the library source should be either ‘METAGENOMIC’ or ‘METATRANSCRIPTOMIC’. Please see the [library source](https://ena-docs.readthedocs.io/en/latest/submit/reads/webin-cli.html#permitted-values-for-library-source) guidelines for further details.

After validation by ENA, if the above criteria are met we will be able to access the submitted data.

To request private analysis with MGnify, navigate to the [home page](https://www.ebi.ac.uk/metagenomics/), click ‘Submit and/or Request’ and complete the form. You will need to login to request analysis of private data. To request analysis of a public dataset in ENA click ‘Request’ and complete the form.
Once we have received the requests, they will be queued for analysis (more details about our [Analysis pipeline](analysis.md#analysis)).

The length of time required for analysis varies according to the number of projects in the queue and the nature and number of runs in the submission. However, we aim to have most analyses completed in less than a week once validated by ENA.

5. Accessing analysed data
: Upon completion of analysis, data will be uploaded on the website. MGnify pipeline will generate a number of charts and downloadable files ([Files available to download on the MGnify website](portal.md#files-available-to-download-on-the-mgnify-website)).

6. Private access
: For private data, users will have to login to the MGnify website to access their data, until they become public

7. Public access to private data
: Private data will become public after an initial confidential period of two years. Submitters will receive an email from ENA prior to the public release of their data, giving them the opportunity to extend the confidential period which is set to two years as default (as indicated at [Can I change the release date of my project?](faqs.md#can-i-change-the-release-date-of-my-project)).
