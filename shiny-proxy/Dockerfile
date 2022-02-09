FROM jupyter/datascience-notebook:r-4.1.2
USER root
ENV CHOWN_HOME_OPTS='-R'
ENV CHOWN_HOME='yes'

COPY dependencies/environment.yml /tmp/environment.yml
COPY dependencies/dependencies.R /tmp/dependencies.R
RUN mamba env update -n base --file /tmp/environment.yml
RUN Rscript /tmp/dependencies.R
COPY shiny-proxy/custom.js /home/jovyan/.jupyter/custom/custom.js
COPY notebooks-src/notebooks /home/jovyan/mgnify-examples

COPY jlab_redir_from_url_query_params /tmp/jlab_redir_from_url_query_params
RUN jlpm --cwd /tmp/jlab_redir_from_url_query_params run build
RUN jupyter labextension install /tmp/jlab_redir_from_url_query_params
