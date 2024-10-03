#!/bin/bash
rm mgnify-cache.tgz
Rscript populate-mgnifyr-cache.R
tar -czf mgnify-cache.tgz --absolute-names /home/mgnify/.mgnify_cache