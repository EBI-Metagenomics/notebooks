---
title: MGnify notebooks servers
author: 
  - name: MGnify
    url: https://www.ebi.ac.uk/metagenomics
    affiliation: EMBL-EBI
    affiliation-url: https://www.ebi.ac.uk
date: last-modified
citation: true
description: Using MGnify’s Jupyter Notebooks to explore and access data programatically
order: 8
---

## A Jupyter Lab environment for the MGnify API

### Short video tutorial

<iframe width="560" height="315" src="https://www.youtube.com/embed/B8rw7GTX9GQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>[View on YouTube](https://youtu.be/B8rw7GTX9GQ).

::: {.callout-tip}
### Available notebooks
This website contains [previews of the available notebooks](../notebooks_list.qmd). There are examples in both Python and R.
:::

## Where to run the notebooks
The notebooks can be run on [notebooks.mgnify.org](http://notebooks.mgnify.org) (hosted by EMBL; no login required) or on [Galaxy Europe](https://usegalaxy.eu/root?tool_id=interactive_tool_mgnify_notebook) (login required).


### The notebooks.mgnify.org resource

The [MGnify Notebooks Server](https://shiny-portal.embl.de/shinyapps/app/06_mgnify-notebook-lab?jlpath=mgnify-examples/home.ipynb)
is a [Jupyter Lab](https://jupyter.org) environment for doing data analysis online.

You don’t need to install anything – it is hosted by [EMBL’s Cell Biology & Biophysics Unit](https://www.embl.org/research/units/cell-biology-biophysics/cbbcs/) and you use it in your web browser.

No account is required, but your data and the state of your notebooks will be erased after a short period of inactivity.

![The default "Home" notebook of the [MGnify Notebooks Server](https://shiny-portal.embl.de/shinyapps/app/06_mgnify-notebook-lab?jlpath=mgnify-examples/home.ipynb)](images/notebooks/notebooks-home.png){#fig-notebooks-home}

### The Galaxy Europe server
Galaxy is a platform for FAIR data analysis. 
The MGnify notebooks are [available on the Galaxy Europe server as an "interactive tool"](https://usegalaxy.eu/root?tool_id=interactive_tool_mgnify_notebook).
You need an account (free) and to login to be allocated the compute resources to use the tool there.
Because of this, the notebooks hosted on Galaxy Europe are not directly linked from data objects on the MGnify website.

Your data and notebook state is persistent on Galaxy – you can save and resume your work later.

## Use cases for the Notebooks Server

Programmatic access to MGnify data resources is done via the [the API](api.md).

The Notebooks are useful if you’re just **starting to explore the API** and are looking for code examples to get started.

They are also useful if you only need to access a few pieces of data and so **don’t want to install anything** to get what you need.

There are examples in [Python](https://shiny-portal.embl.de/shinyapps/app/06_mgnify-notebook-lab?jlpath=mgnify-examples/Python%20Examples) and in the [R language](https://shiny-portal.embl.de/shinyapps/app/06_mgnify-notebook-lab?jlpath=mgnify-examples/R%20Examples).

## MGnifyR: an R package for accessing MGnify

The Notebooks include code examples written using [MGnifyR](https://github.com/beadyallen/MGnifyR/),
an R package with convenience wrappers around the MGnify API, as well as recipes for cross-study analysis.

MGnifyR is already installed on the Notebook Server, so you can try it out straight away.

Take a look at [this cross-study analysis example](https://shiny-portal.embl.de/shinyapps/app/06_mgnify-notebook-lab?jlpath=mgnify-examples/R%20Examples/Cross-study%20analysis.ipynb).

## Using a Jupyter Notebook

A Jupyter Notebook is an interactive coding document.
It is based on cells (as in blocks of content).
Some cells are just text, and some contain code.

In our examples, there are text cells to explain what we’re doing, and code cells with example code that you can run.

Any output from the code will be printed directly below the code cell.

Only one cells runs at a time, so you can step through a notebook to step through a workflow.

**Each example notebook we provide should run without any changes needed.** You are free to change these as you wish – you’re working on a copy of the examples.

::: {.callout-warning}
Unless you’re using the notebooks on Galaxy, when you leave your computer for a while or close the website your Jupyter Lab instance will end. Your work usually won't be saved so make sure you download anything you need to keep before finishing.
:::

## Jumping to a Notebook from the MGnify website

![There are deep-links to some Notebooks from the [MGnify website](portal.md)](images/notebooks/website-programmatic-access-box.png){#fig-notebooks-deeplink}
    

Some resource views on the MGnify website show a “Programmatic access” banner.
This lists the [API](api.md) URL for the resource, as well as links to any Notebooks that help you consume that API endpoint.

For example, opening a [Study](glossary.md#study) in R or Python means opening a Notebook on our server with example code to read in that study.

These are [deep links](https://en.wikipedia.org/wiki/Deep_linking), in that following them means the Notebook will already know the Study Accession (ID) you are interested in.

## Using the notebooks on your own computer instead

The [code for our notebooks](https://github.com/ebi-Metagenomics/notebooks/) is open source and available on GitHub.

The notebook server is [containerised with Docker](https://www.docker.com/resources/what-container), making [installation](https://github.com/EBI-Metagenomics/notebooks#running-shinyproxy) fairly simple.

You can also simply copy [the notebooks themselves](https://github.com/EBI-Metagenomics/notebooks/tree/main/notebooks-src/notebooks) from GitHub, but you will have to [install the dependencies](https://github.com/EBI-Metagenomics/notebooks/tree/main/dependencies) using e.g. [Conda](https://docs.conda.io/en/latest/miniconda.html).
