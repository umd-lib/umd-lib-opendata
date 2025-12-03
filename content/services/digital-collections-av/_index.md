---
title: Digital Collections Audio/Video
---

[University of Maryland Libraries' Digital Collections Audio/Video Content](https://av.lib.umd.edu)

## OpenSearch

API Description: [OpenSearch](/apis#opensearch)

OpenSearch Description: <https://av.lib.umd.edu/catalog/opensearch.xml>

JSON Endpoint: <https://av.lib.umd.edu/catalog.json>

Example:

```bash {filename="digital-collections-av-search.sh"}
PARAMS='search_field=all_fields&q=athletics'

curl "https://av.lib.umd.edu/catalog?$PARAMS"

curl "https://av.lib.umd.edu/catalog.rss?$PARAMS"
```

Example: [digital-collections-av-search.py](/code/digital-collections-av-search.py)

{{< code filename="static/code/digital-collections-av-search.py" name="digital-collections-av-search.py" language="python" >}}

## OAI-PMH

API Description: [OAI-PMH](/apis#oai-pmh)

Endpoint: <https://api.av.lib.umd.edu/oai/api>

Example:

```bash {filename="digital-collections-av-oaipmh.sh"}
curl "https://api.av.lib.umd.edu/oai/api?verb=Identify"

curl "https://api.av.lib.umd.edu/oai/api?verb=ListSets"

curl "https://api.av.lib.umd.edu/oai/api?verb=ListMetadataFormats"
```

Additional Examples:

* [digital-collections-av-oaipmh.py](/code/digital-collections-av-oaipmh.py)
  Use OAI-PMH to harvest metadata in Digital Collections Audio/Video.
