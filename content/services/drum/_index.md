---
title: DRUM
---

The [Digital Repository at the University of Maryland
(DRUM)](https://drum.lib.umd.edu) collects, preserves, and provides public
access to the scholarly output of the university. Faculty and researchers can
upload research products for rapid dissemination, global visibility and impact,
and long-term preservation.

## OAI-PMH

API Description: [OAI-PMH](/apis#oai-pmh)

Endpoint: <https://api.drum.lib.umd.edu/server/oai/request>

Example:

```bash {filename="drum-oaipmh.sh"}
curl "https://api.drum.lib.umd.edu/server/oai/request?verb=Identify"

curl "https://api.drum.lib.umd.edu/server/oai/request?verb=ListSets"

curl "https://api.drum.lib.umd.edu/server/oai/request?verb=ListMetadataFormats"
```

Additional Examples:

* [drum-oaipmh.py](/code/drum-oaipmh.py) Use OAI-PMH to harvest metadata in DRUM.

## OpenSearch

API Description: [OpenSearch](/apis#opensearch)

Endpoint: <https://api.drum.lib.umd.edu/server/opensearch/search>

Example: [drum-search.py](/code/drum-search.py)

{{< code filename="static/code/drum-search.py" name="drum-search.py" language="python" >}}

## DSpace REST API

API Description: [DSpace REST API](/apis#dspace-rest-api)

Endpoint: <https://api.drum.lib.umd.edu/server/api>

The endpoint is explorable using the [HAL](http://stateless.co/hal_specification.html)
Browser at <https://api.drum.lib.umd.edu/server>.

Example:
{{< code filename="static/code/drum-api.py" name="drum-api.py" language="python" >}}

Additional Example:

* [drum-harvest.py](/code/drum-harvest.py) Harvest metadata and files for every
  item in DRUM.
