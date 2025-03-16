# Digital Collections

<a href="https://digital.lib.umd.edu">University of Maryland Libraries' Digital Collections</a>

## OAI-PMH

Endpoint: `https://api.fcrepo.lib.umd.edu/oai/api`

Example:

```sh
    curl "https://api.fcrepo.lib.umd.edu/oai/api?verb=Identify"

    curl "https://api.fcrepo.lib.umd.edu/oai/api?verb=ListSets"

    curl "https://api.fcrepo.lib.umd.edu/oai/api?verb=ListMetadataFormats"
```

Additional Examples:

* [digital-collections-oaipmh.py](pathname:///code/digital-collections-oaipmh.py)
Use OAI-PMH to harvest metadata in Digital Collections.
