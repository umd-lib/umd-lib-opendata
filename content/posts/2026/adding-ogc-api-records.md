---
publishDate: '2026-09-08T00:00:01-04:00'
draft: false
title: 'Adding OGC API - Records'
type: blog
---

We have added information on [OGC API - Records](/apis#ogc-api-records) to the
APIs page, with a runnable example for the
[BTAA Geoportal](/services/btaa-geoportal), the Big Ten Academic Alliance's
(BTAA) shared catalog of geospatial data.

From the [OGC API - Records](https://ogcapi.ogc.org/records/) home page:

> OGC API - Records is a multi-part Standard that offers the capability to
> create, modify, and query metadata on the Web. The Standard enables the
> discovery of geospatial resources by standardizing the way collections of
> descriptive information about the resources (metadata) are exposed.

The example walks the standard's discovery chain against the BTAA Geoportal's
catalog and prints each request URL, so any step can be replayed with `curl`. It
uses [uv](https://docs.astral.sh/uv/), so you can run it directly:

```bash
uv run https://opendata.lib.umd.edu/code/geoportal-ogc-records.py
```
