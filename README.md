# EMBL-EBI MGnify example notebooks

This repository contains example notebooks, written in Python and R, for using the [MGnify API](https://www.ebi.ac.uk/metagenomics/api/).

There are various ways to use these Notebooks, including opening them locally in an existing Jupyter environment or via cloud services.

The Notebooks themselves are in the `notebooks-src` dir.


## Opening the notebooks (for use or development): use Docker
Between the [base image](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-datascience-notebook) 
and the extra requirements (`dependecies/*`), the Docker contains all the libraries we need.

```bash
docker build -f docker/Dockerfile .
docker run -it -v $PWD/notebooks-src/notebooks:/home/jovyan/notebooks -p 8888:8888 <whatever the hash of the docker container built was>
```
This binds the `notebooks-src/notebook` directory of this repo to `/home/jovyan/notebooks` inside the Docker,
so you can edit the notebooks. ("jovyan" is always the user for these Jupyter Docker images.)

Your (host) browser will not automatically open Jupyter Lab. 
Copy one of the URLs from the console into your browser to open it.

## Shiny-Proxy application
The notebooks can also be built into a Docker container suitable for running as an Application on ShinyProxy.
The configuration for this is in the `shiny-proxy` dir.

### (re)Creating the Docker
```bash
docker build -t ebi-metagenomics/notebooks -f shiny-proxy/Dockerfile .
```

### Running ShinyProxy locally
- [Download the latest version of ShinyProxy](https://www.shinyproxy.io/downloads/) (>=2.6 is required). It is a JAR, so you need Java installed. i.e., download ShinyProxy into this repo directory.
- The `application.yml` file must be in the same directory as the location you launch Shiny Proxy from.
- `cd shiny-proxy`, `java -jar shinyproxy-2.6.0.jar`
- Browse to the ShinyProxy URL, likely localhost:8080

