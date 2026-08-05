---
title: Archival Collections
---

The University of Maryland Libraries collects and preserves archival and
manuscript collections of groups and individuals. The [Archival
Collections](https://archives.lib.umd.edu) database provides descriptions of
many of these collections. Use the website to explore collections and request
material for use from [Special Collections and University
Archives](https://www.lib.umd.edu/collections/special) and [Special Collections
in Performing
Arts](https://www.lib.umd.edu/collections/special/performing-arts).

Learn more about our efforts to correct [harmful language in finding
aids](https://www.lib.umd.edu/find/request-special-collections/harmful-language-finding-aids).

## OAI-PMH

API Description: [OAI-PMH](/apis#oai-pmh)

Endpoint: <https://archives-api.lib.umd.edu/oai>

Example:

```bash
#!/bin/bash

curl "https://archives-api.lib.umd.edu/oai?verb=Identify"

curl "https://archives-api.lib.umd.edu/oai?verb=ListSets"

curl "https://archives-api.lib.umd.edu/oai?verb=ListMetadataFormats"
```

Additional Examples:

* [archival-collections-oaipmh.py](/code/archival-collections-oaipmh.py) Use
  OAI-PMH to harvest metadata in Archival Collections.
