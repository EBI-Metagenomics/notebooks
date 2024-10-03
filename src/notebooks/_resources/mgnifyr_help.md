# Help with MGnifyR

MGnifyR is an R package that provides a convenient way for R users to access data from [the MGnify API](https://www.ebi.ac.uk/metagenomics/api/).

Detailed help for each function is available in R using the standard `?function_name` command (i.e. typing `?doQuery` will bring up built-in help for the `doQuery` command). 


Full documentation is also available [on the MGnifyR website](https://ebi-metagenomics.github.io/MGnifyR/index.html).

## MGnifyR Command cheat sheet

The following list of key functions should give a starting point for finding relevent documentation.

- `MgnifyClient()` : Create the client object required for all other functions.
- `doQuery()`: Search MGnify database for studies, samples, runs, analyses, biomes, assemblies, and genomes.
- `getData()`: Versatile function to retrieve raw results
- `getFile()`,  `searchFile()`: Download any MGnify files, also including processed reads and identified protein sequences
- `getMetadata()`: Get all study, sample and analysis metadata for the supplied analysis accessions
- `getResult()`: Get microbial and/or functional profiling data for a list of accessions
- `searchAnalysis()`: Look up analysis accession IDs for one or more study or sample accessions
