# Digital Collections Audio/Video

<a href="https://av.lib.umd.edu">University of Maryland Libraries' Digital
Collections Audio/Video Content</a>

## OpenSearch

OpenSearch Description: `https://av.lib.umd.edu/catalog/opensearch.xml`

JSON Endpoint: `https://av.lib.umd.edu/catalog.json`

Example:

```sh
    PARAMS='search_field=all_fields&q=athletics'

    curl "https://av.lib.umd.edu/catalog?$PARAMS"

    curl "https://av.lib.umd.edu/catalog.rss?$PARAMS"
```

Example:
[digital-collections-av-search.py](pathname:///code/digital-collections-av-search.py)

.. literalinclude:: code/digital-collections-av-search.py

## OAI-PMH

Endpoint: `https://api.av.lib.umd.edu/oai/api`

Example:

```sh
    curl "https://api.av.lib.umd.edu/oai/api?verb=Identify"

    curl "https://api.av.lib.umd.edu/oai/api?verb=ListSets"

    curl "https://api.av.lib.umd.edu/oai/api?verb=ListMetadataFormats"
```

Additional Examples:

* [digital-collections-av-oaipmh.py](pathname:///code/digital-collections-av-oaipmh.py)
  Use OAI-PMH to harvest metadata in Digital Collections Audio/Video.
