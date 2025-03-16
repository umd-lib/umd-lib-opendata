# DRUM

The <a href="https://drum.lib.umd.edu">Digital Repository at the University of
Maryland (DRUM)</a> collects, preserves, and provides public access to the
scholarly output of the university. Faculty and researchers can upload research
products for rapid dissemination, global visibility and impact, and long-term
preservation.

## OAI-PMH

Endpoint: `https://api.drum.lib.umd.edu/server/oai/request`

Example:

```sh
    curl "https://api.drum.lib.umd.edu/server/oai/request?verb=Identify"

    curl "https://api.drum.lib.umd.edu/server/oai/request?verb=ListSets"

    curl "https://api.drum.lib.umd.edu/server/oai/request?verb=ListMetadataFormats"
```

Additional Examples:

* [drum-oaipmh.py](pathname:///code/drum-oaipmh.py) Use OAI-PMH to harvest
metadata in DRUM.

## OpenSearch

Endpoint: `https://api.drum.lib.umd.edu/server/opensearch/search`

Example: [drum-search.py](pathname:///code/drum-search.py)

.. literalinclude:: code/drum-search.py

## DSpace REST API

Endpoint: `https://api.drum.lib.umd.edu/server/api`

The endpoint is explorable using the <a href="http://stateless.co/hal_specification.html">HAL
Browser</a> at <a href="https://api.drum.lib.umd.edu/server">https://api.drum.lib.umd.edu/server</a>.

.. literalinclude:: code/drum-api.py

Additional Example:

* [drum-harvest.py](pathname:///code/drum-harvest.py) Harvest metadata and files
for every item in DRUM.
