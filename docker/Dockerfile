FROM jupyter/datascience-notebook:r-4.2.2
USER root
ENV CHOWN_HOME_OPTS='-R'
ENV CHOWN_HOME='yes'

# Install Python/R dependencies
COPY dependencies/r-environment.yml /tmp/r-environment.yml
COPY dependencies/py-environment.yml /tmp/py-environment.yml
COPY dependencies/dependencies.R /tmp/dependencies.R
RUN mamba install -y nb_conda_kernels
RUN mamba env create -f /tmp/r-environment.yml
RUN mamba env create -f /tmp/py-environment.yml

SHELL ["conda", "run", "-n", "mgnify-r-env", "/bin/bash", "-c"]
RUN Rscript /tmp/dependencies.R
# Place / check / populate MGnifyR cache for example used in studies
# Zipped cache should be up to date in repo, but run populate to be sure nothing is missing
COPY dependencies/mgnify-cache.tgz /tmp/mgnify-cache.tgz
RUN tar -xzf /tmp/mgnify-cache.tgz -C /
COPY dependencies/populate-mgnifyr-cache.R /tmp/populate-mgnifyr-cache.R
RUN Rscript /tmp/populate-mgnifyr-cache.R
SHELL ["/bin/bash", "-c"]

# Install JupyterLab extension to handle query parameter > env vars in ShinyProxy
COPY shiny_proxy_jlab_query_parms /tmp/shiny_proxy_jlab_query_parms
RUN pip install /tmp/shiny_proxy_jlab_query_parms

# Install Jupyter Lab extension providing MGnify-specific help 
COPY mgnify_jupyter_lab_ui /tmp/mgnify_jupyter_lab_ui
RUN pip install /tmp/mgnify_jupyter_lab_ui

# Clean yarn cache else chown'ing home is very slow on container start
RUN jlpm cache clean 

# Clean tmp
RUN rm -rf /tmp/*

COPY shiny-proxy/custom.js /home/jovyan/.jupyter/custom/custom.js
COPY src/notebooks /home/jovyan/mgnify-examples