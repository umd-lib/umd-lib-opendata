---
title: BTAA Geoportal
---

The [Big Ten Academic Alliance (BTAA) Geoportal](https://geo.btaa.org/)
connects users to digital geospatial resources, including GIS datasets, web
services, and digitized historical maps from multiple data clearinghouses and
library catalogs. The site is solely a search tool and does not host any data.

## JSON API

Search Endpoint: <https://geo.btaa.org/api/v1/search>

OpenAPI Description: <https://geo.btaa.org/api/openapi.json>

Interactive Documentation: <https://geo.btaa.org/api/docs>

The geoportal was rebuilt on a new platform and now publishes a documented
JSON:API. The earlier Blacklight-style endpoints — the OpenSearch description
at `/catalog/opensearch.xml` and the `?format=rss` and `?format=json`
parameters on the search page — have been withdrawn. Requests using them
return the HTML page with a `200` status rather than an error, so a client
that checks only the status code fails when it tries to parse the body.

The search endpoint takes `q` for the keyword query, along with `page`,
`per_page` (maximum 100), `sort`, and facet parameters:

```bash
#!/bin/bash

curl "https://geo.btaa.org/api/v1/search?q=maryland"

curl "https://geo.btaa.org/api/v1/search?q=maryland&per_page=25&page=2"
```

Each record in the `data` array carries its metadata under `attributes.ogm`,
using [OpenGeoMetadata Aardvark](https://opengeometadata.org/ogm-aardvark/)
field names such as `dct_title_s`, `dct_publisher_sm`, and
`gbl_resourceClass_sm`. Individual records are also available from
`/api/v1/resources/{id}`, and the API exposes an
[OGC API - Records](https://ogcapi.ogc.org/records/) interface under
`/api/v1/ogc/`.

Example: [geoportal-search.py](/code/geoportal-search.py)

{{< code filename="static/code/geoportal-search.py" name="geoportal-search.py" language="python" >}}
