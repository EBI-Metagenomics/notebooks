# Many packages are already available from the jupyter-datascience docker image: https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-r-notebook

# Extra pacakges not installed in Docker image, or installable via Conda:

require("devtools")
devtools::install_github("EBI-Metagenomics/MGnifyR", ref="d1baca93465f8c97101049bd66b63a8bb5a0d6ab")
