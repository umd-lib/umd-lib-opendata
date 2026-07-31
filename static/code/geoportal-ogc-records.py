#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests==2.34.2",
#     "urllib3==2.7.0",
# ]
# ///

"""Search the BTAA Geoportal through its OGC API - Records catalog.

OGC API - Records (<https://ogcapi.ogc.org/records/>) is the Open Geospatial
Consortium (OGC) standard for searchable catalogs of geospatial resources.
The Big Ten Academic Alliance (BTAA) Geoportal serves one at
`https://geo.btaa.org/api/v1/ogc`.

A Records catalog is self-describing, and this example walks the discovery
chain a client is meant to follow: `/conformance` says which parts of the
standard the server implements, `/collections` lists the record collections
it holds, each collection's `/sortables` names the properties an ordering
can use, and `/items` runs the search itself. Records come back as GeoJSON
Features whose `properties` carry the catalog metadata.
"""

import sys

import requests
import urllib3

API = "https://geo.btaa.org/api/v1/ogc"
QUERY = "maryland"
LIMIT = 3
TIMEOUT_SECONDS = 30

RECORD_PAGE = "https://geo.btaa.org/resources/{id}"


def is_transient(error):
    """Decide whether a failed request is worth trying again later.

    A host name that does not resolve, or a certificate that will not verify,
    is a settled fact about the URL rather than a passing condition. requests
    reports the first as a ConnectionError wrapping urllib3's
    NameResolutionError, and the second as its own SSLError subclass -- which
    carries no response, so a status code alone cannot tell them apart from a
    refused connection.
    """
    if isinstance(error, requests.exceptions.SSLError):
        return False
    cause = error.args[0] if error.args else None
    if isinstance(getattr(cause, "reason", None), urllib3.exceptions.NameResolutionError):
        return False

    status = getattr(error.response, "status_code", None)
    # No status at all means the request never reached an application; 5xx and
    # 429 mean the service cannot serve right now. A 4xx is this example's
    # problem.
    return status is None or status >= 500 or status == 429


def get_json(path, params=None):
    """Fetch one catalog document and echo the URL so it can be replayed."""
    url = API + path
    try:
        response = requests.get(url, params=params, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        payload = response.json()
    except requests.exceptions.JSONDecodeError:
        # requests.exceptions.JSONDecodeError subclasses RequestException, so
        # this clause has to come first to be reachable.
        content_type = response.headers.get("content-type", "an unknown type")
        print(f"{url} returned {content_type} rather than JSON", file=sys.stderr)
        # A body that is not JSON means the API changed under this example.
        sys.exit(1)
    except requests.RequestException as error:
        print(f"{url} could not be read: {error}", file=sys.stderr)
        # 75 = EX_TEMPFAIL: the condition may clear on its own.
        sys.exit(75 if is_transient(error) else 1)

    # response.url is the request as finally encoded, so it can be pasted
    # straight into a browser or curl to see the raw JSON.
    print(f"GET {response.url}")
    return payload


def first(values, default):
    """Return the first entry of a multi-valued property such as `spatial`."""
    if isinstance(values, list) and values:
        return values[0]
    return default


# Every OGC API declares the conformance classes it implements; a class URI
# ending in /conf/sorting, for example, promises the sorting behaviour that
# part of the standard defines.
conformance = get_json("/conformance")
classes = conformance.get("conformsTo")
if not isinstance(classes, list):
    # sys.exit with a string prints it to stderr and exits 1: a document
    # without its defining key means the API changed under this example.
    sys.exit('the conformance document has no "conformsTo" list')
print(f"Conformance: {', '.join(uri.rsplit('/', 1)[-1] for uri in classes)}")

# A catalog groups its records into collections, each searchable through its
# own /items endpoint.
collections = get_json("/collections").get("collections")
if not isinstance(collections, list):
    sys.exit('the collections document has no "collections" list')
if not collections:
    print("The catalog lists no collections.")
    sys.exit(0)
collection = collections[0]
collection_id = collection.get("id")
if not collection_id:
    sys.exit('the collection entry has no "id"')
print(f"Collection:  {collection_id} - {collection.get('title') or '(untitled)'}")

# The sortables document is a JSON Schema whose properties name the fields an
# ordering may use -- the behaviour the "sorting" conformance class above
# promises. "title" below comes from this list.
sortables = get_json(f"/collections/{collection_id}/sortables")
properties = sortables.get("properties")
if not isinstance(properties, dict):
    sys.exit('the sortables document is not a JSON Schema with "properties"')
print(f"Sortables:   {', '.join(sorted(properties))}")

# `q` is the standard's free-text search parameter; `sortby` takes any
# property the sortables document names.
results = get_json(f"/collections/{collection_id}/items",
                   params={"q": QUERY, "sortby": "title", "limit": LIMIT})
# A search that matches nothing is a legitimate answer, so check for the
# GeoJSON envelope rather than for records: a FeatureCollection with a
# "features" list is what says the query was understood.
if results.get("type") != "FeatureCollection" or not isinstance(results.get("features"), list):
    sys.exit("the items response is not a GeoJSON FeatureCollection")

features = results["features"]
if not features:
    print(f'No records matched "{QUERY}".')
    sys.exit(0)

print(f'Showing {len(features)} records matching "{QUERY}":')
for feature in features:
    # A record's catalog metadata rides in the Feature's "properties"; a
    # property the catalog has no value for is present but null.
    record = feature.get("properties") or {}
    print("----")
    print(f"Title:   {record.get('title') or '(untitled)'}")
    print(f"Class:   {first(record.get('resourceClass'), '(unknown)')}")
    print(f"Spatial: {first(record.get('spatial'), '(unknown)')}")
    print(f"Access:  {record.get('accessRights') or '(unknown)'}")
    print(f"Link:    {RECORD_PAGE.format(id=feature.get('id', ''))}")
