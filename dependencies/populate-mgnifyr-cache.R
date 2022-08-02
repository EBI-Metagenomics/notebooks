# Pre-populate MGonifyR Cache with default examples, to save expensive API calls

library(MGnifyR)

# For the "Fetch Analyses metadata" notebook
mg <- mgnify_client(usecache = T, cache_dir = '/home/jovyan/.mgnify_cache')
analyses_accessions <- mgnify_analyses_from_studies(mg, 'MGYS00005116')
analyses_metadata_df <- mgnify_get_analyses_metadata(mg, analyses_accessions)

# For the "Comparative Metagenomics" notebook
tara_all = mgnify_analyses_from_studies(mg, 'MGYS00002008')
metadata = mgnify_get_analyses_metadata(mg, tara_all)
