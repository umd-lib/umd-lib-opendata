Services
########

List of services, with their technologies, endpoints, and examples

DRUM
=======================================================

The `Digital Repository at the University of Maryland (DRUM)
<https://drum.lib.umd.edu>`_ collects, preserves, and provides public access
to the scholarly output of the university. Faculty and researchers can upload
research products for rapid dissemination, global visibility and impact, and
long-term preservation.

OAI-PMH
-------

Endpoint: `<https://api.drum.lib.umd.edu/server/oai/request>`_

Example:

::

    #!/bin/bash

    curl "https://api.drum.lib.umd.edu/server/oai/request?verb=Identify"

    curl "https://api.drum.lib.umd.edu/server/oai/request?verb=ListSets"

    curl "https://api.drum.lib.umd.edu/server/oai/request?verb=ListMetadataFormats"

Additional Examples:

- :download:`drum-oaipmh.py <code/drum-oaipmh.py>` Use OAI-PMH to harvest metadata in DRUM.

OpenSearch
-----------

Endpoint: `<https://api.drum.lib.umd.edu/server/opensearch/search>`_

Example: :download:`drum-search.py <code/drum-search.py>`

.. literalinclude:: code/drum-search.py

DSpace REST API
-----------------

Endpoint: `<https://api.drum.lib.umd.edu/server/api>`_

The endpoint is explorable using the `HAL <http://stateless.co/hal_specification.html>`_
Browser at `<https://api.drum.lib.umd.edu/server>`_.

.. literalinclude:: code/drum-api.py

Additional Example:

- :download:`drum-harvest.py <code/drum-harvest.py>` Harvest metadata and files for every item in DRUM.

Digital Collections
===================

`University of Maryland Libraries' Digital Collections <https://digital.lib.umd.edu>`_ (New Repository)

OAI-PMH
-------

Endpoint: ``https://api.fcrepo.lib.umd.edu/oai/api``

Example:

::

    #!/bin/bash

    curl "https://api.fcrepo.lib.umd.edu/oai/api?verb=Identify"

    curl "https://api.fcrepo.lib.umd.edu/oai/api?verb=ListSets"

    curl "https://api.fcrepo.lib.umd.edu/oai/api?verb=ListMetadataFormats"

Additional Examples:

- :download:`digital-collections-oaipmh.py <code/digital-collections-oaipmh.py>` Use OAI-PMH to harvest metadata in Digital Collections.

Digital Collections Audio/Video
===============================

`University of Maryland Libraries' Digital Collections Audio/Video Content <https://av.lib.umd.edu>`_

OpenSearch
-----------

OpenSearch Description: `<https://av.lib.umd.edu/catalog/opensearch.xml>`_

JSON Endpoint: `<https://av.lib.umd.edu/catalog.json>`_

Example:

::

    #!/bin/bash

    PARAMS='search_field=all_fields&q=athletics'

    curl "https://av.lib.umd.edu/catalog?$PARAMS"

    curl "https://av.lib.umd.edu/catalog.rss?$PARAMS"

Example: :download:`digital-collections-av-search.py <code/digital-collections-av-search.py>`

.. literalinclude:: code/digital-collections-av-search.py

OAI-PMH
-------

Endpoint: ``https://api.av.lib.umd.edu/oai/api``

Example:

::

    #!/bin/bash

    curl "https://api.av.lib.umd.edu/oai/api?verb=Identify"

    curl "https://api.av.lib.umd.edu/oai/api?verb=ListSets"

    curl "https://api.av.lib.umd.edu/oai/api?verb=ListMetadataFormats"

Additional Examples:

- :download:`digital-collections-av-oaipmh.py <code/digital-collections-av-oaipmh.py>` Use OAI-PMH to harvest metadata in Digital Collections Audio/Video.

BTAA Geoportal
=======================================================

The `Big Ten Academic Alliance (BTAA) Geoportal
<https://geo.btaa.org/>`_ connects users to digital geospatial resources,
including GIS datasets, web services, and digitized historical maps from
multiple data clearinghouses and library catalogs. The site is solely a search
tool and does not host any data.

OpenSearch
-----------

OpenSearch Description: `<https://geo.btaa.org/catalog/opensearch.xml>`_

RSS+XML Endpoint: `<https://geo.btaa.org/?format=rss>`_

JSON Endpoint: `<https://geo.btaa.org/?format=json>`_

The OpenSearch API is not officially documented by the
`Geoportal Documentation page <https://sites.google.com/umn.edu/btaa-gdp/about/documentation>`_.

Example: The RSS+XML and JSON endpoints operate using the same set of URL parameters
used by the website interface, eg these curl commands return the same
result set:

::

    #!/bin/bash

    curl "https://geo.btaa.org/?search_field=all_fields&q=maryland"

    curl "https://geo.btaa.org/?search_field=all_fields&q=maryland&format=rss"

    curl "https://geo.btaa.org/?search_field=all_fields&q=maryland&format=json"

Example: :download:`geoportal-search.py <code/geoportal-search.py>`

.. literalinclude:: code/geoportal-search.py

Internet Archive
================

`Internet Archive <https://archive.org>`_ is a non-profit library of millions of free books, movies, software, music, websites, and more, which includes a `University of Maryland, College Park <https://archive.org/details/university_maryland_cp>`_ collection.

Advanced Search
---------------

Endpoint: `<https://archive.org/advancedsearch.php>`_

Example: :download:`code/internet-archive-search.py <code/internet-archive-search.py>`

.. literalinclude:: code/internet-archive-search.py

Dryad
================

UMD is a member of the `Dryad Data Community <https://datadryad.org/>`_, which is a community-owned resource that offers data curation services in addition to large storage capacity for most kinds of datasets in any discipline. A search is available with a limit to the `University of Maryland, College Park Institution <https://datadryad.org/search?f%5Bdryad_author_affiliation_name_sm%5D%5B%5D=University+of+Maryland%2C+College+Park>`_.  You can find more information on the `UMD Libraries website <https://www.lib.umd.edu/research/oss/publishing-and-digital-projects/repository-services/open-data-repositories>`_.

OpenAPI Specification
---------------------

The Dryad API is built using the :any:`OpenAPI Specification <APIs OpenAPI Specification>`, with both `YAML-based <https://datadryad.org/openapi.yml>`_ and `HTML-based <https://datadryad.org/api/v2/docs/>`_ documentation available.

Endpoint: `<https://datadryad.org/api/v2/>`_

Example: :download:`code/dryad-api.py <code/dryad-api.py>`

.. literalinclude:: code/dryad-api.py
