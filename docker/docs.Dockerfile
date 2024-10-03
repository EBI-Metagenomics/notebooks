FROM quay.io/microbiome-informatics/emg-notebooks.dev

ARG QUARTO_VERSION="1.5.57"
WORKDIR /tmp
USER root
RUN wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb
RUN dpkg -i quarto-${QUARTO_VERSION}-linux-amd64.deb
ARG NB_USER="mgnify"
ARG NB_UID="1000"
ARG NB_GID="100"
USER ${NB_UID}

ENTRYPOINT ["tini", "-g", "--", "/bin/bash", "/shell-hook.sh", "quarto"]