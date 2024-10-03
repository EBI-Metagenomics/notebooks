FROM ghcr.io/prefix-dev/pixi:0.27.1-jammy AS build
LABEL maintainer="EMBL-EBI Microbiome Informatics (MGnify) Team <metagenomics-help@ebi.ac.uk>"

WORKDIR /nb-envs
COPY pixi.* .

RUN pixi install -v --frozen
RUN pixi shell-hook > /shell-hook.sh
RUN echo 'exec "$@"' >> /shell-hook.sh

# Install JupyterLab extension to handle query parameter > env vars in ShinyProxy
COPY jlab_query_params /tmp/jlab_query_params
RUN pixi run install_query_params_plugin

# Install Jupyter Lab extension providing MGnify-specific help 
COPY mgnify_jupyter_lab_ui /tmp/mgnify_jupyter_lab_ui
RUN pixi run install_mgnify_jupyter_ui

ENTRYPOINT ["/bin/bash", "/shell-hook.sh"]

# ---

FROM rocker/r2u:24.04 as rbuild
RUN apt-get update --yes
RUN apt-get install --yes r-bioc-phyloseq \
	r-bioc-metagenomeseq \
	r-bioc-genomeinfodbdata \
	r-bioc-pathview \
	r-bioc-aldex2 \
	r-bioc-keggrest \
	r-cran-reshape2 \
	r-cran-vegan \
	r-cran-irkernel \
	r-cran-ggplot2 \
	r-cran-dplyr \
	r-cran-tidyjson \
	r-cran-devtools \
	r-cran-tidyverse

RUN Rscript -e "install.packages('devtools')"
RUN Rscript -e "require(devtools); devtools::install_github(repo = 'zellerlab/siamcat')"
RUN Rscript -e "remotes::install_github('yiluheihei/microbiomeMarker')"
# For some reason r-bioc-microbiomemarker isnt apt installable
RUN Rscript -e "remotes::install_github('EBI-Metagenomics/MGnifyR')"
# MGnifyR not yet on bioconductor release
# --- 

# inspired by Jupyter Stacks, but with pixi instead of conda/mamba
FROM rbuild as jupyter

ARG NB_USER="mgnify"
ARG NB_UID="1000"
ARG NB_GID="100"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update --yes && \
    apt-get upgrade --yes && \
    apt-get install --yes --no-install-recommends \
    ca-certificates \
    locales \
    netbase \
    sudo \
    tini \
    run-one \
    wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    echo "C.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen

COPY --from=build --chown=$NB_UID:$NB_GID /nb-envs/.pixi /nb-envs/.pixi

ENV PIXI_DIR=/nb-envs/.pixi \
    SHELL=/bin/bash \
    NB_USER="${NB_USER}" \
    NB_UID=${NB_UID} \
    NB_GID=${NB_GID} \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    LANGUAGE=C.UTF-8
ENV HOME="/home/${NB_USER}"


COPY docker/fix-permissions /usr/local/bin/fix-permissions
RUN chmod a+rx /usr/local/bin/fix-permissions

RUN if grep -q "${NB_UID}" /etc/passwd; then \
        userdel --remove $(id -un "${NB_UID}"); \
    fi

RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su && \
    sed -i.bak -e 's/^%admin/#%admin/' /etc/sudoers && \
    sed -i.bak -e 's/^%sudo/#%sudo/' /etc/sudoers && \
    useradd --no-log-init --create-home --shell /bin/bash --uid "${NB_UID}" --no-user-group "${NB_USER}" && \
    chmod g+w /etc/passwd && \
    fix-permissions "/home/${NB_USER}"

COPY --from=build /shell-hook.sh /shell-hook.sh
ENTRYPOINT ["tini", "-g", "--", "/bin/bash", "/shell-hook.sh"]

# Place / check / populate MGnifyR cache for example used in studies
# Zipped cache should be up to date in repo, but run populate to be sure nothing is missing
COPY dependencies/mgnify-cache.tgz /tmp/mgnify-cache.tgz
RUN tar -xzf /tmp/mgnify-cache.tgz -C /

# Clean yarn cache else chown'ing home is very slow on container start
RUN rm -rf /home/${NB_USER}/.yarn
RUN rm -rf /home/${NB_USER}/.cache
RUN rm -rf /home/${NB_USER}/.npm

# Clean tmp
RUN rm -rf /tmp/*

COPY jupyter_config/custom.js $HOME/.jupyter/custom/custom.js
COPY jupyter_config/jupyter_config.json $HOME/.jupyter/jupyter_config.json
COPY src/notebooks $HOME/mgnify-examples
RUN /nb-envs/.pixi/envs/default/bin/jupyter labextension disable "@jupyterlab/apputils-extension:announcements"

ENV PATH="/nb-envs/.pixi/envs/default/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN Rscript -e "IRkernel::installspec()"

RUN echo "bspm::disable()" > ~/.Rprofile
RUN fix-permissions "/home/${NB_USER}"

# turn off bspm, it causes warnings
RUN sed -i '/options(bspm.version.check=FALSE)/d' /etc/R/Rprofile.site
RUN sed -i '/suppressMessages(bspm::enable())/d' /etc/R/Rprofile.site


USER ${NB_UID}

ENV JUPYTER_PORT=8888
EXPOSE $JUPYTER_PORT

WORKDIR "${HOME}"

CMD ["run-one-constantly", "jupyter", "lab", "--IdentityProvider.token=''", "--IdentityProvider.password=''", "--no-browser", "--ip=0.0.0.0"]

