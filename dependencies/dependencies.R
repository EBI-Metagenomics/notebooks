# Many packages are already available from the jupyter-datascience docker image: https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-r-notebook

# Extra pacakges not installed in Docker image, or installable via Conda:

require("devtools")
require("remotes")
devtools::install_github("beadyallen/MGnifyR")
devtools::install_github(“ropensci/plotly”)
remotes::install_github(“jbkunst/highcharter”)