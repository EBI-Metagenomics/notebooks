---
title: "MGnify code examples"
author:
  - name: MGnify
    url: https://www.ebi.ac.uk/metagenomics
date: last-modified
description: "Python and R examples for MGnify API v2, replacing the hosted notebooks."
order: 8
---

The hosted MGnify Jupyter Lab environment has been retired. You can now edit and
run small [API v2 examples](../examples/index.qmd) directly in your browser:

- [Python with requests and pandas](../examples/python.qmd)
- [R with jsonlite and base R](../examples/r.qmd)
- [Copyable MGnipy code for local Python](../examples/mgnipy.qmd)

The browser pages use WebAssembly and do not start a server-side notebook kernel.
They support study metadata, paginated analyses, analysis detail and a small
result table. Open a page with `?study=MGYS00010397` to initialise a specific
study. Browser edits and variables disappear when you reload the page.

The historical notebooks are retained in the
[source repository](https://github.com/EBI-Metagenomics/notebooks/tree/main/src/notebooks)
as legacy material. They use older APIs or MGnifyR and are not maintained as
runnable examples. For larger analyses, use local Python and the
[MGnipy documentation](https://mgnipy.mgnify.org/).
