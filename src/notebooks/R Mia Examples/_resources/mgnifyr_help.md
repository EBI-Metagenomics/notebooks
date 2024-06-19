# Help with MGnifyR

MGnifyR is an R package that provides a convenient way for R users to access data from [the MGnify API](https://www.ebi.ac.uk/metagenomics/api/).

Detailed help for each function is available in R using the standard `?function_name` command (i.e. typing `?mgnify_query` will bring up built-in help for the mgnify_query command). 

A vignette is available containing a reasonably verbose overview of the main functionality. 
This can be read either within R with the `vignette("MGnifyR")` command, or [in the development repository](https://htmlpreview.github.io/?https://github.com/beadyallen/MGnifyR/blob/master/doc/MGnifyR.html)

## MGnifyR Command cheat sheet

The following list of key functions should give a starting point for finding relevent documentation.

- `MgnifyClient()` : Create the client object required for all other functions.
- `doQuery()` : Query and search the whole MGnify database.
- `searchAnalysis()` : 	Look up analysis accession IDs for one or more study or sample accessions
- `getMetadata()` : Retrieve all study, sample and analysis metadata for given analyses.
- `getResult` : Get microbial and/or functional profiling data for a list of accessions
- `getFile` : Download raw results files from MGnify.
- `getData()` : Low level API access helper function to retrieve raw results.
