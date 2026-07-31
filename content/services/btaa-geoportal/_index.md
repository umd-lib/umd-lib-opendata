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
`/api/v1/resources/{id}`.

Example: [geoportal-search.py](/code/geoportal-search.py)

{{< code filename="static/code/geoportal-search.py" name="geoportal-search.py" language="python" >}}

## OGC API - Records

API Description: [OGC API - Records](/apis#ogc-api-records)

Landing Page: <https://geo.btaa.org/api/v1/ogc/>

The BTAA Geoportal's catalog is also exposed as an [OGC API -
Records](https://ogcapi.ogc.org/records/) service. It declares six Part 1:
Core conformance classes, including sorting, and holds a single collection of
records, `btaa-records`. Each document leads to the next: the collection
list gives the collection id, and the sortables document gives the values
`sortby` accepts:

```bash
#!/bin/bash

curl "https://geo.btaa.org/api/v1/ogc/conformance"

curl "https://geo.btaa.org/api/v1/ogc/collections"

curl "https://geo.btaa.org/api/v1/ogc/collections/btaa-records/sortables"

curl "https://geo.btaa.org/api/v1/ogc/collections/btaa-records/items?q=maryland&sortby=title&limit=3"
```

Records are GeoJSON Features whose `properties` carry the catalog metadata
(`title`, `resourceClass`, `spatial`, `accessRights`, and so on).

Example: [geoportal-ogc-records.py](/code/geoportal-ogc-records.py)

{{< code filename="static/code/geoportal-ogc-records.py" name="geoportal-ogc-records.py" language="python" >}}
