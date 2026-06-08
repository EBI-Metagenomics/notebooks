FROM ghcr.io/prefix-dev/pixi:0.67.2-noble

LABEL maintainer="EMBL-EBI Microbiome Informatics (MGnify) Team <metagenomics-help@ebi.ac.uk>"

ARG NB_USER=jovyan
ARG NB_UID=2001
ARG NB_GID=2001

ENV NB_USER=${NB_USER}
ENV NB_UID=${NB_UID}
ENV NB_GID=${NB_GID}
ENV HOME=/home/${NB_USER}
ENV SHELL=/bin/bash

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates bash tini && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd --gid ${NB_GID} ${NB_USER} && \
    useradd --uid ${NB_UID} --gid ${NB_GID} --create-home --shell /bin/bash ${NB_USER}

WORKDIR /opt/mgnify
COPY images/r/pixi.toml /opt/mgnify/pixi.toml
COPY images/r/pixi.lock /opt/mgnify/pixi.lock
RUN pixi install --locked && pixi run install-kernel

COPY dependencies/dependencies.R /tmp/dependencies.R
RUN pixi run Rscript /tmp/dependencies.R

COPY jlab_query_params /tmp/jlab_query_params
COPY mgnify_jupyter_lab_ui /tmp/mgnify_jupyter_lab_ui
RUN pixi run python -m pip install --no-build-isolation /tmp/jlab_query_params /tmp/mgnify_jupyter_lab_ui

COPY dependencies/mgnify-cache.tgz /tmp/mgnify-cache.tgz
RUN tar -xzf /tmp/mgnify-cache.tgz -C / && rm /tmp/mgnify-cache.tgz

COPY jupyter_config/custom.js ${HOME}/.jupyter/custom/custom.js
COPY jupyter_config/jupyter_config.json ${HOME}/.jupyter/jupyter_config.json
COPY src/notebooks ${HOME}/mgnify-examples
COPY images/common/start-notebook.sh /usr/local/bin/start-notebook.sh

RUN pixi run jupyter labextension disable "@jupyterlab/apputils-extension:announcements" && \
    chmod +x /usr/local/bin/start-notebook.sh && \
    rm -rf /tmp/* ${HOME}/.cache ${HOME}/.npm ${HOME}/.yarn && \
    chown -R ${NB_UID}:${NB_GID} ${HOME} /opt/mgnify

USER ${NB_USER}
WORKDIR ${HOME}

EXPOSE 8888
ENTRYPOINT ["tini", "-g", "--"]
CMD ["start-notebook.sh"]
