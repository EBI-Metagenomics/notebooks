# Pre-populate MGnifyR Cache with default examples, to save expensive API calls
library(MGnifyR)
library(stringr)


mg <- mgnify_client(usecache = T, cache_dir = '/home/jovyan/.mgnify_cache')

# For the "Comparative Metagenomics 1" notebook
tara_all = mgnify_analyses_from_studies(mg, 'MGYS00002008')
metadata = mgnify_get_analyses_metadata(mg, tara_all)
v5_metadata = metadata[which(metadata$'analysis_pipeline-version'=='5.0'), ]
sub1 = v5_metadata[str_detect(v5_metadata$'sample_environment-feature', "ENVO:00002042"), ]
sub2 = v5_metadata[str_detect(v5_metadata$'sample_environment-feature', "ENVO:00000213"), ]
filtered_samples = rbind(sub1,sub2)
ps = mgnify_get_analyses_phyloseq(mg, filtered_samples$'analysis_accession')

