FROM jupyter/minimal-notebook:lab-3.6.3@sha256:1443243e00caa7db61de7faaad626a173c4a51d8f15e48e07c6b111de73d0f38
LABEL maintainer="EMBL-EBI Microbiome Informatics (MGnify) Team <metagenomics-help@ebi.ac.uk>"
USER root
ENV CHOWN_HOME_OPTS='-R'
ENV CHOWN_HOME='yes'

# Install Python/R dependencies
RUN mamba install -y nb_conda_kernels
RUN conda config --system --prepend channels bioconda
COPY dependencies/r-environment.yml /tmp/r-environment.yml
RUN mamba env create -f /tmp/r-environment.yml
COPY dependencies/py-environment.yml /tmp/py-environment.yml
RUN mamba env create -f /tmp/py-environment.yml
COPY dependencies/dependencies.R /tmp/dependencies.R

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
COPY jlab_query_params /tmp/jlab_query_params
RUN pip install /tmp/jlab_query_params

# Install Jupyter Lab extension providing MGnify-specific help 
COPY mgnify_jupyter_lab_ui /tmp/mgnify_jupyter_lab_ui
RUN pip install /tmp/mgnify_jupyter_lab_ui

# Clean yarn cache else chown'ing home is very slow on container start
RUN rm -rf /home/jovyan/.yarn
RUN rm -rf /home/jovyan/.cache
RUN rm -rf /home/jovyan/.npm

# Clean tmp
RUN rm -rf /tmp/*

COPY jupyter_config/custom.js /home/jovyan/.jupyter/custom/custom.js
COPY jupyter_config/jupyter_config.json /home/jovyan/.jupyter/jupyter_config.json
COPY src/notebooks /home/jovyan/mgnify-examples
RUN jupyter labextension disable "@jupyterlab/apputils-extension:announcements"
