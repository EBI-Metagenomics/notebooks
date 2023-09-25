FROM continuumio/miniconda3 as build
WORKDIR /work

RUN conda config --system --prepend channels bioconda
COPY dependencies/r-environment.yml /tmp/r-environment.yml
RUN conda env create -f /tmp/r-environment.yml

COPY dependencies/py-environment.yml /tmp/py-environment.yml
RUN conda env create -f /tmp/py-environment.yml
RUN conda clean -afy

COPY dependencies/dependencies.R /tmp/dependencies.R
SHELL ["conda", "run", "-n", "mgnify-r-env", "/bin/bash", "-c"]
RUN Rscript /tmp/dependencies.R
SHELL ["/bin/bash", "-c"]

RUN conda install -c conda-forge conda-pack && conda clean --all -f -y

RUN conda-pack -n mgnify-r-env \
    -o /tmp/mgnify-r-env.tar \
    --exclude *.js.map \
    --exclude *.pyc \
    --exclude *.a && \
    mkdir -p /tmp/envs/mgnify-r-env && cd /tmp/envs/mgnify-r-env && tar xf /tmp/mgnify-r-env.tar && \
    rm /tmp/mgnify-r-env.tar && \
    rm -rf /opt/conda/envs/mgnify-r-env && \
    mv /tmp/envs/mgnify-r-env /opt/conda/envs/mgnify-r-env && \
    /opt/conda/envs/mgnify-r-env/bin/conda-unpack

RUN conda-pack -n mgnify-py-env \
    -o /tmp/mgnify-py-env.tar \
    --exclude *.js.map \
    --exclude *.pyc \
    --exclude *.a && \
    mkdir -p /tmp/envs/mgnify-py-env && cd /tmp/envs/mgnify-py-env && tar xf /tmp/mgnify-py-env.tar && \
    rm /tmp/mgnify-py-env.tar && \
    rm -rf /opt/conda/envs/mgnify-py-env && \
    mv /tmp/envs/mgnify-py-env /opt/conda/envs/ && \
    /opt/conda/envs/mgnify-py-env/bin/conda-unpack

# ------------------- #

FROM jupyter/base-notebook:lab-3.6.3@sha256:8a15ee10ec8be7c760c83f8fb87445530bf8a92dfddd99ec8dab240f388fdfdf as runtime
LABEL maintainer="EMBL-EBI Microbiome Informatics (MGnify) Team <metagenomics-help@ebi.ac.uk>"
USER root
ENV CHOWN_HOME_OPTS='-R'
ENV CHOWN_HOME='yes'

WORKDIR /work

COPY --chown=root:100 --from=build /opt/conda/envs /opt/conda/envs

# Install Jupyter (non kernel) dependencies
RUN mamba install -y conda-forge::nb_conda_kernels conda-forge::leafmap=0.26.0 --freeze-installed && mamba clean --all -f -y

# Place / check / populate MGnifyR cache for example used in studies
# Zipped cache should be up to date in repo, but run populate to be sure nothing is missing
COPY dependencies/mgnify-cache.tgz /tmp/mgnify-cache.tgz
RUN tar -xzf /tmp/mgnify-cache.tgz -C /

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

WORKDIR /home/jovyan
