---
title: BTAA Geoportal
---

The [Big Ten Academic Alliance (BTAA) Geoportal](https://geo.btaa.org/)
connects users to digital geospatial resources, including GIS datasets, web
services, and digitized historical maps from multiple data clearinghouses and
library catalogs. The site is solely a search tool and does not host any data.

## OpenSearch

OpenSearch Description: <https://geo.btaa.org/catalog/opensearch.xml>

RSS+XML Endpoint: <https://geo.btaa.org/?format=rss>

JSON Endpoint: <https://geo.btaa.org/?format=json>

The OpenSearch API is not officially documented by the
[Geoportal Documentation page](https://sites.google.com/umn.edu/btaa-gdp/about/documentation).

Example: The RSS+XML and JSON endpoints operate using the same set of URL parameters
used by the website interface, eg these curl commands return the same
result set:

```bash {filename="geoportal-search.sh"}
curl "https://geo.btaa.org/?search_field=all_fields&q=maryland"

curl "https://geo.btaa.org/?search_field=all_fields&q=maryland&format=rss"

curl "https://geo.btaa.org/?search_field=all_fields&q=maryland&format=json"
```

Example: [geoportal-search.py](/code/geoportal-search.py)

{{< code filename="static/code/geoportal-search.py" name="geoportal-search.py" language="python" >}}
