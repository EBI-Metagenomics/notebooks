# EMBL-EBI MGnify user guides and API examples

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-9-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

This repository builds the static site at https://docs.mgnify.org using [Quarto](https://quarto.org/).
Documentation is in `src/docs`; editable Python and R API v2 examples are in
`src/examples`. Code executes in visitors' browsers using Pyodide and webR via
Quarto Live.

## Develop and preview

Install [Quarto](https://quarto.org/docs/get-started/) (CI uses 1.5.56).
Python and R are **not** required to execute cells during rendering: the example
pages disable build-time execution. Node 22+ runs the small static checks.
[Task](https://taskfile.dev/) is optional.

```bash
quarto render
quarto preview --no-browser --port 9000 --host localhost
# Or: task render-static / task preview-static
node --test tests/static/*.test.mjs
```

Serve `_site` over HTTP(S), not `file://`. `task serve-static` serves an existing
build using Python's HTTP server. Runtime downloads require internet access.
Keep `_site` and `.quarto` out of version control.

Quarto Live is vendored in `_extensions/r-wasm/live`, from upstream tag **v0.2.0**
(the upstream manifest still says `0.1.3-dev`). Its defaults pin Pyodide to
**0.28.1** and webR to **0.6.0**. To deliberately update it:

```bash
quarto add r-wasm/quarto-live@v0.2.0 --no-prompt
```

Re-test both runtimes when updating the extension or Quarto. No separate custom
WASM runtime, execution backend, or API proxy is maintained here.

## Supported examples and boundaries

- `src/examples/python.qmd`: requests, pandas, study detail, bounded analysis
  pagination, analysis detail, a small Pfam TSV, and editable table exploration.
- `src/examples/r.qmd`: equivalent operations using jsonlite and base R in webR.
- `src/examples/mgnipy.qmd`: a short introduction linking to MGnipy’s interactive demos.
- `src/examples/download-csv.qmd`: paginated study analyses and a browser CSV download.
- `src/examples/pathways.qmd`: v5 KEGG module completeness, KO exploration and export to KEGG Mapper.
- `src/examples/atlanteco.qmd`: study sample coordinates and an interactive Folium map.

All examples query the live API. Test fixtures live under `tests/static/fixtures`
and are not published. Large matrices, comparative metagenomics and MGnifyR are
outside this migration's scope. The examples use public data only.

Quarto Live supplies the editors and language runtimes; `_extensions/r-wasm/live`
is its packaged upstream code, not a custom application. Static cells use Quarto's
native `code-copy: true`. Quarto Live 0.2.0 has no native copy button for editable
cells; use keyboard copying there. Keep extension behaviour upstream rather than
adding custom editor patches.

MGnipy is not just missing optional browser features: its published 0.3.0 release
has no wheel, requires compiled packages, and eagerly imports the dataset stack.
A future browser subset needs wheel publication, optional dependencies/lazy
imports, and checks of metadata conversion and HTTPX transport. We do not fork,
stub dependencies, or install an unsupported subset here.

## Study deep links from the MGnify website

Use these static-page URLs for the website's buttons:

```text
https://docs.mgnify.org/src/examples/python.html?study=MGYS00010393
https://docs.mgnify.org/src/examples/r.html?study=MGYS00010393
```

Replace the accession using `encodeURIComponent(studyAccession)`. The supported
value is `MGYS` followed by eight digits. Values are normalised and validated,
then passed as OJS input data into Python/R, never interpolated as executable code.
Invalid values produce a visible input error and do not select a substitute study.

The old `jlvar_MGYS` parameter is accepted as an alias on these **new page URLs**.
The first code cell receives `study_accession`; later cells
share the language's global environment. Native form submission reloads the page
when the study changes, avoiding stale results from a previous study.

### Reuse in another example page

This is a shared helper, not an automatic Quarto feature. Currently only
`python.qmd` and `r.qmd` opt in. Any Quarto Live page can use the same pattern.
For a new `live-html` page under `src/examples`, add:

````markdown
```{ojs}
//| echo: false
import {readStudyAccession} from "./study-link.js"
study_accession = readStudyAccession(window.location.search)
```

```{pyodide}
#| input: [study_accession]
STUDY = study_accession
```
````

For R, use a `{webr}` cell with the same `input` option and
`STUDY <- study_accession`. The editable accession form is optional; copy it from
`python.qmd` if needed. Without a query parameter, the helper defaults to
`MGYS00010393`.

Pages outside `src/examples` need an adjusted helper import path and must include
that JavaScript file in their Quarto `resources`. The examples directory already
configures this in `_metadata.yml`. Other query parameters need their own parsing
and validation; they are not automatically passed to Python or R.

## Required API CORS configuration

At initial verification on 2026-09-10, API v2 returned JSON but omitted
`Access-Control-Allow-Origin` for an Origin of `https://docs.mgnify.org`.
The example FTP result did return `Access-Control-Allow-Origin: *`.
Browser access is therefore blocked at the API boundary until its configuration
is updated. This is an API deployment change, not a Quarto setting.

Configure the API (or its ingress) to allow cross-origin **GET** requests from:

- `https://docs.mgnify.org` in production;
- `http://localhost:9000` for local testing (confirmed allowed on 2026-09-11);
- any actual preview origin you choose to support.

For Django with django-cors-headers, this normally means these entries in
`CORS_ALLOWED_ORIGINS` and correctly placed `CorsMiddleware`. Preserve `Vary:
Origin`, include headers on error responses as well as success, and check the
final response after redirects. No cross-origin credential support is required
for these public examples. Do not disable browser security or add a public proxy.

Verify from outside the API host, then run the cells from the deployed docs:

```bash
curl -i -H 'Origin: https://docs.mgnify.org' \
  'https://www.ebi.ac.uk/metagenomics/api/v2/studies/MGYS00010393'
```

The response should contain `Access-Control-Allow-Origin: https://docs.mgnify.org`
(or `*` if the API intentionally supports all public origins). Repeat for study
analyses, analysis detail, and their HTTPS download URLs. Quarto's runtime and R
package CDNs also need to be reachable. webR's default channel can run on static
hosting without configuring COOP/COEP headers for this site.

## Validation and publishing

CI checks the URL contract, renders the site without
executing notebooks or contacting the API, and uploads `_site` as an artifact.
The existing publish workflow still deploys only `main`/`docs-only` (or on manual
invocation); a push to [`pyodide`](https://pyodide.org/) does not automatically publish this work.
The Jupyter Docker build/test/push and release workflow has been retired.

Before publishing, enable API CORS as described above. The optional browser test
runs Python and R against a local fixture API, downloads a real FTP result, and
checks editing, pagination and accession deep links:

```bash
cd tests/static
npm ci
npm run test:browser
```

Serve `_site` at `http://localhost:9000` in a second terminal first. This check downloads the
runtimes and packages.

## Notebook archive

[notebooks_archive](notebooks_archive/) preserves notebooks with material not yet
covered by the browser examples. They are non-functional historical references,
excluded from the site and CI execution; only their `.ipynb` files are retained.

### Docs authoring guidance

Mostly, you can just use normal Markdown – but there are some handy extra features.
We frequently use: YAML Front Matter (metadata for each docs page); Callout Blocks; Figures. E.g.:

```markdown
---
title: My new docs page
author:
  - name: MGnify
    url: https://www.ebi.ac.uk/metagenomics
    affiliation: EMBL-EBI
    affiliation-url: https://www.ebi.ac.uk
date: last-modified
citation: true
description: This page explains everything
---

## Steps to do everything

::: {.callout-warning}

### By the way

This sentence will be rendered as an attention-grabbing box
:::

![This figure shows everything](images/mypage/everything.png){#fig-my-everything .tall-figure fig-align="left"}

As you can see in @fig-my-everything, ...
```

Note the use of `.tall-figure fig-align="left"`: that is a styling hack for figures that are a tall aspect ratio (e.g. a vertical flow diagram, or a scrolled-page screenshot). It makes those images appear less overwhelming. Don't use it for figures that are square or wide.

There are also examples within the existing docs or on the [Quarto website](https://quarto.org/) for how to do subfigures (panels), annotated code blocks, citations etc.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://sa.ndyroge.rs"><img src="https://avatars.githubusercontent.com/u/414767?v=4?s=100" width="100px;" alt="Sandy Rogers"/><br /><sub><b>Sandy Rogers</b></sub></a><br /><a href="https://github.com/EBI-Metagenomics/notebooks/commits?author=SandyRogers" title="Code">💻</a> <a href="#example-SandyRogers" title="Examples">💡</a> <a href="#ideas-SandyRogers" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-SandyRogers" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/EBI-Metagenomics/notebooks/pulls?q=is%3Apr+reviewed-by%3ASandyRogers" title="Reviewed Pull Requests">👀</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Ales-ibt"><img src="https://avatars.githubusercontent.com/u/26798122?v=4?s=100" width="100px;" alt="Ales-ibt"/><br /><sub><b>Ales-ibt</b></sub></a><br /><a href="https://github.com/EBI-Metagenomics/notebooks/commits?author=Ales-ibt" title="Code">💻</a> <a href="#example-Ales-ibt" title="Examples">💡</a> <a href="#ideas-Ales-ibt" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/vestalisvirginis"><img src="https://avatars.githubusercontent.com/u/54766741?v=4?s=100" width="100px;" alt="Virginie Grosboillot"/><br /><sub><b>Virginie Grosboillot</b></sub></a><br /><a href="#ideas-vestalisvirginis" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/EBI-Metagenomics/notebooks/commits?author=vestalisvirginis" title="Code">💻</a> <a href="#content-vestalisvirginis" title="Content">🖋</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://orcid.org/0000-0002-3079-6586"><img src="https://avatars.githubusercontent.com/u/469983?v=4?s=100" width="100px;" alt="Björn Grüning"/><br /><sub><b>Björn Grüning</b></sub></a><br /><a href="#infra-bgruening" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://research.bebatut.fr/"><img src="https://avatars.githubusercontent.com/u/1842467?v=4?s=100" width="100px;" alt="Bérénice Batut"/><br /><sub><b>Bérénice Batut</b></sub></a><br /><a href="#infra-bebatut" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mberacochea"><img src="https://avatars.githubusercontent.com/u/1123897?v=4?s=100" width="100px;" alt="Martín Beracochea"/><br /><sub><b>Martín Beracochea</b></sub></a><br /><a href="#ideas-mberacochea" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/EBI-Metagenomics/notebooks/commits?author=mberacochea" title="Code">💻</a> <a href="#content-mberacochea" title="Content">🖋</a> <a href="#mentoring-mberacochea" title="Mentoring">🧑‍🏫</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tgurbich"><img src="https://avatars.githubusercontent.com/u/63121037?v=4?s=100" width="100px;" alt="tgurbich"/><br /><sub><b>tgurbich</b></sub></a><br /><a href="#ideas-tgurbich" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/EBI-Metagenomics/notebooks/commits?author=tgurbich" title="Code">💻</a> <a href="#content-tgurbich" title="Content">🖋</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://amartya.vercel.app/"><img src="https://avatars.githubusercontent.com/u/51471924?v=4?s=100" width="100px;" alt="Amartya Nambiar"/><br /><sub><b>Amartya Nambiar</b></sub></a><br /><a href="https://github.com/EBI-Metagenomics/notebooks/commits?author=amartyanambiar" title="Code">💻</a> <a href="#example-amartyanambiar" title="Examples">💡</a> <a href="#ideas-amartyanambiar" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.ebi.ac.uk/metagenomics/"><img src="https://avatars.githubusercontent.com/u/49755902?v=4?s=100" width="100px;" alt="Ekaterina Sakharova"/><br /><sub><b>Ekaterina Sakharova</b></sub></a><br /><a href="#ideas-KateSakharova" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/EBI-Metagenomics/notebooks/commits?author=KateSakharova" title="Code">💻</a> <a href="#content-KateSakharova" title="Content">🖋</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
