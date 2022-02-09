FROM jupyter/datascience-notebook:r-4.1.2
COPY dependencies/environment.yml /tmp/environment.yml
COPY dependencies/dependencies.R /tmp/dependencies.R
RUN mamba env update -n base --file /tmp/environment.yml
RUN Rscript /tmp/dependencies.R
