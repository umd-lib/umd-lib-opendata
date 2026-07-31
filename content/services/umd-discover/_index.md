---
title: UMD Discover
---

From the [UMD Discover](https://lib.guides.umd.edu/umd-discover) Research Guide:

> UMD Discover allows you to discover resources and materials in various
> formats in the UMD and University System of Maryland (USMAI) collections.
> Filters are available to refine your search by location, format, and many
> other criteria. If you have used UMD's prior interface, WorldCat UMD, you
> will be familiar with Discover's core features such as a single search
> box, and faceted limiters.

## SRU

UMD Discover provides an [SRU API endpoint](/apis#sru) for searching the
UMD and USMAI collections. The ExLibris Developer Network provides documentation
on [how to structure SRU retrieval queries](https://developers.exlibrisgroup.com/blog/how-to-configure-the-sru-integration-profile-and-structure-sru-retrieval-queries/).

Endpoint: <https://usmai-umcp.alma.exlibrisgroup.com/view/sru/01USMAI_UMCP>

```bash
#!/bin/bash

curl "https://usmai-umcp.alma.exlibrisgroup.com/view/sru/01USMAI_UMCP?version=1.2&operation=explain"

curl "https://usmai-umcp.alma.exlibrisgroup.com/view/sru/01USMAI_UMCP?version=1.2&operation=searchRetrieve&query=alma.all_for_ui=%22libraries%22&recordSchema=dc"
```

Example: [umddiscover-sru.py](/code/umddiscover-sru.py)

{{< code filename="/static/code/umddiscover-sru.py" name="umddiscover-sru.py" language="python" >}}

You can also use the [sru-queryer](https://pypi.org/project/sru-queryer/)
Python package to build your query to the SRU endpoint. See
[Working with Bib data – using SRU made easier!](https://developers.exlibrisgroup.com/blog/working-with-bib-data-using-sru-made-easier/).

Example: [umddiscover-sru-queryer.py](/code/umddiscover-sru-queryer.py)
