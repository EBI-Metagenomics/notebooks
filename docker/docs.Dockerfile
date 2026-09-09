FROM ghcr.io/quarto-dev/quarto:latest

COPY src/docs /app/docs
COPY src/docs.qmd /app/
COPY src/static-resources /app/static-resources
COPY _quarto.yml /app/

ENTRYPOINT ["quarto"]