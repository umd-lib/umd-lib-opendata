---
title: Dryad
---

UMD is a member of the [Dryad Data Community](https://datadryad.org/), which is
a community-owned resource that offers data curation services in addition to
large storage capacity for most kinds of datasets in any discipline. A search
is available with a limit to the [University of Maryland, College Park
Institution](https://datadryad.org/search?org=https%3A%2F%2Fror.org%2F047s2c258).
You can find more information on the [UMD Libraries
website](https://www.lib.umd.edu/research/oss/publishing-and-digital-projects/repository-services/open-data-repositories).

## OpenAPI Specification

The Dryad API is built using the [OpenAPI Specification](/apis#open-api), with
both [YAML-based](https://datadryad.org/openapi.yml) and
[HTML-based](https://datadryad.org/api/v2/docs/) documentation available.

Endpoint: <https://datadryad.org/api/v2/>

Example: [dryad-api.py](/code/dryad-api.py)

{{< code filename="/static/code/dryad-api.py" name="dryad-api.py"
language="python">}}

## JSON-LD

Format Description: [JSON-LD](/apis#json-ld)

You can extract [schema.org](https://schema.org/)
[DataSet](https://schema.org/Dataset) structured data, encoded using
[JSON-LD](/apis#json-ld), from HTML pages in Dryad for University of Maryland,
College Park authors.

Example:

* [dryad-jsonld.py](/code/dryad-jsonld.py) Harvest metadata and files for every
  item in DRUM.
