FROM quay.io/microbiome-informatics/emg-notebooks.dev

ARG QUARTO_VERSION="1.4.358"
WORKDIR /tmp
RUN wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb
RUN dpkg -i quarto-${QUARTO_VERSION}-linux-amd64.deb
# install conda kernels to standard jupyter kernels
RUN python -m nb_conda_kernels list

ENTRYPOINT ["quarto"]
