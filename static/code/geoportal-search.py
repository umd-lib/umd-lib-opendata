#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests==2.34.2",
#     "urllib3==2.7.0",
# ]
# ///

"""Search the BTAA Geoportal and print matching records.

The geoportal serves a JSON:API at `https://geo.btaa.org/api/v1/search`. An
OpenAPI description is published at <https://geo.btaa.org/api/openapi.json>,
with Swagger UI at <https://geo.btaa.org/api/docs>.

Each record carries its metadata under `attributes.ogm`, using OpenGeoMetadata
Aardvark field names (`dct_title_s`, `dct_publisher_sm`, and so on).
"""

import sys

import requests
import urllib3

ENDPOINT = "https://geo.btaa.org/api/v1/search"
QUERY = "maryland"
PER_PAGE = 10
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


try:
    response = requests.get(
        ENDPOINT,
        params={"q": QUERY, "per_page": PER_PAGE},
        timeout=TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    payload = response.json()
except requests.exceptions.JSONDecodeError:
    # requests.exceptions.JSONDecodeError subclasses RequestException, so this
    # clause has to come first to be reachable.
    content_type = response.headers.get("content-type", "an unknown type")
    print(f"{ENDPOINT} returned {content_type} rather than JSON", file=sys.stderr)
    # A body that is not JSON means the API changed under this example.
    sys.exit(1)
except requests.RequestException as error:
    print(f"{ENDPOINT} could not be read: {error}", file=sys.stderr)
    # 75 = EX_TEMPFAIL: the condition may clear on its own.
    sys.exit(75 if is_transient(error) else 1)


def first(values, default):
    """Return the first entry of an Aardvark multi-valued (`_sm`) field."""
    if isinstance(values, list) and values:
        return values[0]
    return default


# response.url is the request as finally encoded, so it can be pasted straight
# into a browser or curl to see the raw JSON.
print(f"GET {response.url}")

# A search that matches nothing is a legitimate answer, so check for the
# JSON:API envelope rather than for records: "meta.totalCount" beside a "data"
# list is what says the response was understood. Defaulting these instead would
# report any other JSON body as a search with no hits.
meta = payload.get("meta")
records = payload.get("data")
if not isinstance(meta, dict) or "totalCount" not in meta or not isinstance(records, list):
    print(f'{ENDPOINT} did not return a JSON:API envelope with "meta.totalCount" '
          f'and a "data" list', file=sys.stderr)
    sys.exit(1)

total = meta["totalCount"]
print(f'{total} records match "{QUERY}"; showing {len(records)}.')

for record in records:
    metadata = record.get("attributes", {}).get("ogm", {})
    identifier = record.get("id", "")

    print("----")
    print(f"Title:     {metadata.get('dct_title_s', '(untitled)')}")
    print(f"Publisher: {first(metadata.get('dct_publisher_sm'), '(unknown)')}")
    print(f"Class:     {first(metadata.get('gbl_resourceClass_sm'), '(unknown)')}")
    print(f"Link:      {RECORD_PAGE.format(id=identifier)}")
