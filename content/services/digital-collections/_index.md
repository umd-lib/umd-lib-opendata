---
title: Digital Collections
---

[University of Maryland Libraries' Digital Collections](https://digital.lib.umd.edu)

## OAI-PMH

API Description: [OAI-PMH](/apis#oai-pmh)

Endpoint: <https://api.fcrepo.lib.umd.edu/oai/api>

Example:

```bash {filename="digital-collections-oaipmh.sh"}
curl "https://api.fcrepo.lib.umd.edu/oai/api?verb=Identify"

curl "https://api.fcrepo.lib.umd.edu/oai/api?verb=ListSets"

curl "https://api.fcrepo.lib.umd.edu/oai/api?verb=ListMetadataFormats"
```

Additional Examples:

* [digital-collections-oaipmh.py](/code/digital-collections-oaipmh.py) Use
  OAI-PMH to harvest metadata in Digital Collections.
