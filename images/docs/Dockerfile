ARG BASE_IMAGE=quay.io/microbiome-informatics/emg-notebooks-python.dev:latest
FROM ${BASE_IMAGE}

ENV PATH="/opt/mgnify/.pixi/envs/default/bin:${PATH}"

USER root

ARG QUARTO_VERSION=1.5.57
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates wget && \
    arch="$(dpkg --print-architecture)" && \
    case "${arch}" in \
      amd64) quarto_arch="amd64" ;; \
      arm64) quarto_arch="arm64" ;; \
      *) echo "Unsupported architecture: ${arch}" >&2; exit 1 ;; \
    esac && \
    wget -O /tmp/quarto.deb "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-${quarto_arch}.deb" && \
    apt-get install -y --no-install-recommends /tmp/quarto.deb && \
    rm -rf /var/lib/apt/lists/* /tmp/quarto.deb

RUN \
    mkdir -p /usr/local/share/jupyter/kernels && \
    cp -R /opt/mgnify/.pixi/envs/default/share/jupyter/kernels/mgnify-py-env \
      /usr/local/share/jupyter/kernels/conda-env-mgnify-py-env-py && \
    mkdir -p ${HOME}/.cache ${HOME}/.local/share && \
    chown -R ${NB_UID}:${NB_GID} ${HOME}/.cache ${HOME}/.local && \
    chown -R ${NB_UID}:${NB_GID} /usr/local/share/jupyter/kernels

USER jovyan
WORKDIR ${HOME}

ENTRYPOINT ["quarto"]
