FROM jupyter/datascience-notebook:r-4.1.2
USER root
ENV CHOWN_HOME_OPTS='-R'
ENV CHOWN_HOME='yes'

COPY dependencies/environment.yml /tmp/environment.yml
COPY dependencies/dependencies.R /tmp/dependencies.R
RUN mamba env update -n base --file /tmp/environment.yml
RUN Rscript /tmp/dependencies.R

COPY shiny_proxy_jlab_query_parms /tmp/shiny_proxy_jlab_query_parms
RUN pip install /tmp/shiny_proxy_jlab_query_parms
RUN jlpm cache clean  # cleans yarn cache else chown'ing home is very slow on container start