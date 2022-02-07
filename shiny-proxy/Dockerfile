FROM openanalytics/shinyproxy-juypter-datascience
COPY dependencies/environment.yml /tmp/environment.yml
COPY dependencies/dependencies.R /tmp/dependencies.R
RUN mamba env update -n base --file /tmp/environment.yml
RUN Rscript /tmp/dependencies.R
COPY notebooks-src/notebooks /home/jovyan/mgnify-examples
