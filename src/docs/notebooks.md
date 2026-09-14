---
title: "MGnify code examples"
author:
  - name: MGnify
    url: https://www.ebi.ac.uk/metagenomics
date: last-modified
description: "Python and R examples for MGnify API v2, replacing the hosted notebooks."
order: 8
---

Edit and run small [API v2 examples](../examples/index.qmd) directly in your browser:

- [Python with requests and pandas](../examples/python.qmd)
- [R with jsonlite and base R](../examples/r.qmd)
- [Download analyses as CSV](../examples/download-csv.qmd)
- [Map AtlantECO samples](../examples/atlanteco.qmd)

For the MGnipy Python client, see the [introduction and demo](../examples/mgnipy.qmd).

The browser pages use WebAssembly and do not start a server-side notebook kernel.
They support study metadata, paginated analyses, analysis detail and a small
result table. Open the introductory Python or R page with
`?study=MGYS00010393` to initialise a specific study. Browser edits and variables disappear when you reload the page.

The historical notebooks are retained in the
[source repository](https://github.com/EBI-Metagenomics/notebooks/tree/main/notebooks_archive)
as non-functional historical material. For larger analyses, use local Python and the
[MGnipy documentation](https://mgnipy.mgnify.org/).
