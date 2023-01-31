FROM quay.io/microbiome-informatics/emg-notebooks.dev

ARG QUARTO_VERSION="1.3.142"
WORKDIR /tmp
RUN wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb
RUN dpkg -i quarto-${QUARTO_VERSION}-linux-amd64.deb
ENTRYPOINT ["quarto"]
