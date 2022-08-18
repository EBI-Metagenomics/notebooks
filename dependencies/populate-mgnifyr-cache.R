# Pre-populate MGnifyR Cache with default examples, to save expensive API calls
library(MGnifyR)

mg <- mgnify_client(usecache = T, cache_dir = '/home/jovyan/.mgnify_cache')

# For the "Comparative Metagenomics 1" notebook
tara_all = mgnify_analyses_from_studies(mg, 'MGYS00002008')
metadata = mgnify_get_analyses_metadata(mg, tara_all)

