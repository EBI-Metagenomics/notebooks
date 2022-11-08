# EMBL-EBI MGnify example notebooks
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
[![Quay.io docker container build](https://quay.io/repository/microbiome-informatics/emg-notebooks.dev/status)](https://quay.io/repository/microbiome-informatics/emg-notebooks.dev)
![Tests](https://github.com/ebi-metagenomics/notebooks/actions/workflows/test.yaml/badge.svg)


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

### Testing with a locally built Docker
```bash
docker build -f shiny-proxy/Dockerfile .
```
Put the created image ID into the value of `shiny-proxy/application.yml:container-img` (or use `-t quay.io/microbiome-informatics/emg-notebooks.dev` in the docker build).

### Updating the image on Quay.io
There is an on-push build trigger for this repository that builds images to quay.io/quay.io/microbiome-informatics/emg-notebooks.dev

Just push to the repository (all branches are built and tagged). If you push to the `main` branch, the `:latest` tag will point to that version, once it is built.

### Running ShinyProxy
- [Download the latest version of ShinyProxy](https://www.shinyproxy.io/downloads/) (>=2.6 is required). It is a JAR, so you need Java installed. i.e., download ShinyProxy into this repo directory.
- The `application.yml` file must be in the same directory as the location you launch Shiny Proxy from.
- `docker pull quay.io/microbiome-informatics/emg-notebooks.dev`
- `cd shiny-proxy`, `java -jar shinyproxy-2.6.0.jar`
- Browse to the ShinyProxy URL, likely localhost:8080

## Jupyter Lab Extension, for deep-linking
`shiny_proxy_jlab_query_parms` contains a [JupyterLab Extension](https://jupyterlab.readthedocs.io/en/stable/user/extensions.html) to support deep-linking into JupyterLab, especially when running inside Shiny Proxy.

This extension was created using the [JupyterLab Extension Cookiecutter TS project](https://github.com/jupyterlab/extension-cookiecutter-ts), which is [BSD3 Licensed](https://github.com/jupyterlab/extension-cookiecutter-ts/blob/3.0/LICENSE).

This extenion is needed because Shiny Proxy does not pass the URL path beyond an app's identifier down to the iframe running the app (JupyterLab).

The extension does two things:
1. **Allows deeplinking to notebooks.** It watches for a URL querystring parameter, `?jlpath=`, and uses this to forward Jupyter Lab to an internal URI which activates that path. This works because Shiny Proxy **does** include the query params in the iframe. E.g. browsing to `localhost:8080/app/mgnify-notebook-lab?jlpath=notebooks/home.ipynb` will trigger Jupyter Lab to open the `home.ipynb` notebooks once the application initialises. This is a frontend extension in `shiny_proxy_jlab_query_params/src/index.ts`.
2. **Sets ENV VARs based on query params.** On Jupyter Lab launch, it sends the querystring parameters to a Jupyter Lab "server-side" extension handler. The handler takes any querystring params beginning `?jlvar_` and sets corresponding ENV VARs. E.g., `?jlvar_MGYS=MGYS007` results in an ENV VAR of `MGYS=MGYS007` being available to any kernels launched after this. These ENV VARs can then, of course, be read in Notebooks (e.g. `os.getenv('MGYS')` in Python or `Sys.getenv('MGYS')` in R). There are helper utilities for both R and Python, that try to read such an ENV VAR otherwise ask for user input. These are in `notebooks-src/notebooks/{Python Examples | R Examples}/lib/variable_utils.{R|Python}`.

Together, this means a URL like: `localhost:8080/app/mgnify-notebook-lab?jlpath=notebooks/home.ipynb&jlvar_MGYS=MGYS00005116` will trigger Shiny Proxy to start the container, then open the `home` notebook, and have an MGYS environment variable ready to use in code.


## Testing
A small integration test suite is written using Jest-Puppetteer.
You need to have built or pulled the shiny-proxy/Dockerfile (`quay.io/microbiome-informatics/emg-notebooks.dev`), and have Shiny Proxy downloaded first.
The test suite runs Shiny Proxy, and makes sure Jupyter Lab opens, the deep-linking works, and variable insertion works in R and Python.

```bash
cd tests
npm install
npm test
```

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://github.com/Ales-ibt"><img src="https://avatars.githubusercontent.com/u/26798122?v=4?s=100" width="100px;" alt="Ales-ibt"/><br /><sub><b>Ales-ibt</b></sub></a><br /><a href="https://github.com/EBI-Metagenomics/notebooks/commits?author=Ales-ibt" title="Code">💻</a> <a href="#example-Ales-ibt" title="Examples">💡</a> <a href="#ideas-Ales-ibt" title="Ideas, Planning, & Feedback">🤔</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!