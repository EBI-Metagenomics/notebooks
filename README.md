# EMBL-EBI MGnify example notebooks
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-6-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
[![Quay.io docker container build](https://quay.io/repository/microbiome-informatics/emg-notebooks.dev/status)](https://quay.io/repository/microbiome-informatics/emg-notebooks.dev)
![Tests](https://github.com/ebi-metagenomics/notebooks/actions/workflows/test.yaml/badge.svg)


This repository contains example notebooks, written in Python and R, for using the [MGnify API](https://www.ebi.ac.uk/metagenomics/api/).

There are various ways to use these Notebooks, including opening them locally in an existing Jupyter environment or via cloud services.

The Notebooks themselves are in the `src/notebooks` dir.


## Development prerequisites
You need [Docker](https://www.docker.com/products/docker-desktop/) installed.
(Podman will also work for basics like editing the notebooks.)

You need [Task](https://taskfile.dev/) installed for handy shortcut commands. If you don't want to install that, check `Taskfile.yml` for the long commands.

## Opening the notebooks (for use or development): use Docker
Between the [base image](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-datascience-notebook) 
and the extra requirements (`dependecies/*`), the Docker contains all the libraries we need.

### To add a new notebook
```bash
TITLE='My New Notebook' AUTHOR='My Name' task add-py-notebook
```
This copies and fills in a template notebook stub file with a standard header, into `src/notebooks/Python Examples`.

(TODO: `R` version).

### To open the notebooks server in edit mode
```bash
task edit-notebooks
```

This runs the Docker image `quay.io/microbiome-informatics/emg-notebooks.dev:latest` which will either by pulled from Quay, 
or run from your local image if you have built it (see below).

The folder `src/notebooks` will be mounted into the Docker container, so that changes you make are reflected in the repository.

Open a web browser to one of the URLs printed in your console to see Jupyter Lab.
It should be localhost port 8888, with a random token.

When you're finished editing, use normal `git add` and `git commit` to contribute your changes.

For info, ("jovyan" is always the user for these Jupyter Docker images.)

#### Guidance for authoring notebooks
- Notebooks should be complete examples, that can be run with zero code changes needed
- Notebooks should showcase good practice and use of popular libraries
- Use the Jupyter menu option to "Clear All Outputs" before checking changes into git
- Datasets should run reasonably quickly (i.e. no step should take more than a few minutes)
  - If large (slow) data fetches are needed, these should be cached in the Docker image.

##### Caching data in the image
MGnifyR uses a cache of pulled MGnify data.
This is populated during the Docker build, into `/home/jovyan/.mgnify_cache`, by the script in `dependencies/populate-mgnify-cache.R`.
Add commands to this to include other datasets in the cache.
The cache is zipped and checked into the repo for faster population during builds (`dependencies/mgnify-cache.tgz`), since it rarely changes.
To check in an updated version of the cache...
```bash
docker run -it -v $PWD/dependencies:/opt/dependencies mgnify-nb-dev /bin/bash
cd /opt/dependencies
rm mgnify-cache.tgz
Rscript populate-mgnifyr-cache.R
tar -czf mgnify-cache.tgz /home/jovyan/.mgnify_cache
exit
git add depdencies/mgnify-cache.tgz
```

### Changing dependencies and Docker build
The add dependencies, edit the `dependencies/environment.yml` file.

You can temporarily try things by opening a Terminal inside Jupyter Lab and `mambda install`ing the package(s).
But make sure you reflect everything in the conda environment file.

Then check the environment builds by (re)building the Docker:
```bash
docker build -f docker/Dockerfile -t quay.io/microbiome-informatics/emg-notebooks.dev:latest .
```

## Generating static previews
There is a setup to use [Quarto](https://quarto.org/) to render the notebooks – including inputs and outputs – as a static website (amongst other mediums).

This is useful as a kind of documentation resource.

There is a Dockerfile to add Quarto on top of the regular Docker stack: `docker/docs.Dockerfile`.

To preview the statically rendered notebooks, use:
```bash
task render-static
```
This builds a docker image tagged as `notebooks-static`, runs Quarto inside it, executes all cells of the notebooks, 
and renders the completed notebooks to the `_site` folder (which is mounted from your host machine into Docker).

You can then open the generated HTML, or use
```bash
task preview-static
```
to render the notebook in watch-mode and serve them to [serve a preview of them](http://localhost:4444).


## Shiny-Proxy application
The notebooks can also be built into a Docker container suitable for running as an Application on ShinyProxy.
The configuration for this is in the `shiny-proxy` dir.

### Testing with a locally built Docker
```bash
docker build -f docker/Dockerfile -t quay.io/microbiome-informatics/emg-notebooks.dev .
```
(or just retag with `docker tag mgnify-nb-dev quay.io/microbiome-informatics/emg-notebooks.dev` if you already built it as above).

### Running ShinyProxy
- [Download the latest version of ShinyProxy](https://www.shinyproxy.io/downloads/) (>=2.6 is required). It is a JAR, so you need Java installed. i.e., download ShinyProxy into this repo directory.
- The `application.yml` file must be in the same directory as the location you launch Shiny Proxy from.
- If you want the currently deployed image instead of your local one... `docker pull quay.io/microbiome-informatics/emg-notebooks.dev`
- `cd shiny-proxy`, `java -jar shinyproxy-2.6.1.jar`
- Browse to the ShinyProxy URL, likely localhost:8080


## Jupyter Lab Extension, for deep-linking
`shiny_proxy_jlab_query_parms` contains a [JupyterLab Extension](https://jupyterlab.readthedocs.io/en/stable/user/extensions.html) to support deep-linking into JupyterLab, especially when running inside Shiny Proxy.

This extension was created using the [JupyterLab Extension Cookiecutter TS project](https://github.com/jupyterlab/extension-cookiecutter-ts), which is [BSD3 Licensed](https://github.com/jupyterlab/extension-cookiecutter-ts/blob/3.0/LICENSE).

This extenion is needed because Shiny Proxy does not pass the URL path beyond an app's identifier down to the iframe running the app (JupyterLab).

The extension does two things:
1. **Allows deeplinking to notebooks.** It watches for a URL querystring parameter, `?jlpath=`, and uses this to forward Jupyter Lab to an internal URI which activates that path. This works because Shiny Proxy **does** include the query params in the iframe. E.g. browsing to `localhost:8080/app/mgnify-notebook-lab?jlpath=notebooks/home.ipynb` will trigger Jupyter Lab to open the `home.ipynb` notebooks once the application initialises. This is a frontend extension in `shiny_proxy_jlab_query_params/src/index.ts`.
2. **Sets ENV VARs based on query params.** On Jupyter Lab launch, it sends the querystring parameters to a Jupyter Lab "server-side" extension handler. The handler takes any querystring params beginning `?jlvar_` and sets corresponding ENV VARs. E.g., `?jlvar_MGYS=MGYS007` results in an ENV VAR of `MGYS=MGYS007` being available to any kernels launched after this. These ENV VARs can then, of course, be read in Notebooks (e.g. `os.getenv('MGYS')` in Python or `Sys.getenv('MGYS')` in R). There are helper utilities for both R and Python, that try to read such an ENV VAR otherwise ask for user input. These are in `src/notebooks/{Python Examples | R Examples}/lib/variable_utils.{R|Python}`.

Together, this means a URL like: `localhost:8080/app/mgnify-notebook-lab?jlpath=notebooks/home.ipynb&jlvar_MGYS=MGYS00005116` will trigger Shiny Proxy to start the container, then open the `home` notebook, and have an MGYS environment variable ready to use in code.


## Jupyter Lab Extension, for MGnify-specific help
There is also an extension to render a MGnify-specific help pane and menu inside Jupyter Lab.
This is in the `mgnify_jupyter_lab_ui` folder.


## Testing
A small integration test suite is written using Jest-Puppetteer.
You need to have built or pulled the docker/Dockerfile (tagegd as `quay.io/microbiome-informatics/emg-notebooks.dev`), and have Shiny Proxy downloaded first.
The test suite runs Shiny Proxy, and makes sure Jupyter Lab opens, the deep-linking works, and variable insertion works in R and Python.

```bash
cd tests
npm install
npm test
```


## Deployment
There is an on-push build trigger for this repository that builds images to `quay.io/quay.io/microbiome-informatics/emg-notebooks.dev`

Just push to the repository (all branches are built and tagged). If you push to the `main` branch, the `:latest` tag will point to that version, once it is built.

This built image can be (and is) deployed to multiple servers, e.g. a ShinyProxy instance or the Galaxy project.
EMBL's ShinyProxy updates to the latest semver tag at 0300 daily. For Galaxy, open a PR to edit [the tool schema](https://github.com/galaxyproject/galaxy/tree/dev/tools/interactive/interactivetool_mgnify_notebook.xml).

### Releases
Tag releases with semver tags, like `v1.0.0`.

- Increment by `0.0.1` for bugfixes, new notebooks, new packages etc.
- Increment by `0.1` for changes in the base docker image, or refactors of the docker/environments etc.
- Increment by `1` for changes in how the entire stack is run.


## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://sa.ndyroge.rs"><img src="https://avatars.githubusercontent.com/u/414767?v=4?s=100" width="100px;" alt="Sandy Rogers"/><br /><sub><b>Sandy Rogers</b></sub></a><br /><a href="https://github.com/EBI-Metagenomics/notebooks/commits?author=SandyRogers" title="Code">💻</a> <a href="#example-SandyRogers" title="Examples">💡</a> <a href="#ideas-SandyRogers" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-SandyRogers" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/EBI-Metagenomics/notebooks/pulls?q=is%3Apr+reviewed-by%3ASandyRogers" title="Reviewed Pull Requests">👀</a></td>
      <td align="center"><a href="https://github.com/Ales-ibt"><img src="https://avatars.githubusercontent.com/u/26798122?v=4?s=100" width="100px;" alt="Ales-ibt"/><br /><sub><b>Ales-ibt</b></sub></a><br /><a href="https://github.com/EBI-Metagenomics/notebooks/commits?author=Ales-ibt" title="Code">💻</a> <a href="#example-Ales-ibt" title="Examples">💡</a> <a href="#ideas-Ales-ibt" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center"><a href="https://github.com/vestalisvirginis"><img src="https://avatars.githubusercontent.com/u/54766741?v=4?s=100" width="100px;" alt="Virginie Grosboillot"/><br /><sub><b>Virginie Grosboillot</b></sub></a><br /><a href="#ideas-vestalisvirginis" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/EBI-Metagenomics/notebooks/commits?author=vestalisvirginis" title="Code">💻</a> <a href="#content-vestalisvirginis" title="Content">🖋</a></td>
      <td align="center"><a href="http://orcid.org/0000-0002-3079-6586"><img src="https://avatars.githubusercontent.com/u/469983?v=4?s=100" width="100px;" alt="Björn Grüning"/><br /><sub><b>Björn Grüning</b></sub></a><br /><a href="#infra-bgruening" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
      <td align="center"><a href="http://research.bebatut.fr/"><img src="https://avatars.githubusercontent.com/u/1842467?v=4?s=100" width="100px;" alt="Bérénice Batut"/><br /><sub><b>Bérénice Batut</b></sub></a><br /><a href="#infra-bebatut" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
      <td align="center"><a href="https://github.com/mberacochea"><img src="https://avatars.githubusercontent.com/u/1123897?v=4?s=100" width="100px;" alt="Martín Beracochea"/><br /><sub><b>Martín Beracochea</b></sub></a><br /><a href="#ideas-mberacochea" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/EBI-Metagenomics/notebooks/commits?author=mberacochea" title="Code">💻</a> <a href="#content-mberacochea" title="Content">🖋</a> <a href="#mentoring-mberacochea" title="Mentoring">🧑‍🏫</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
