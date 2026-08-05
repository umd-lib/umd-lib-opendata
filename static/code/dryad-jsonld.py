#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "rdflib==7.6.0",
#     "requests==2.34.2",
#     "urllib3==2.7.0",
# ]
# ///

# Use the Dryad API to harvest JSON-LD metadata for datasetts with authors
# affiliated with the University of Maryland, College Park, and serialize it to
# RDF Trig format.

import io
import sys

import requests
import urllib3
from rdflib import Dataset, Namespace
from rdflib.parser import InputSource

BASE_URL = "https://datadryad.org"

TIMEOUT_SECONDS = 30


def is_transient(error):
    """Decide whether a failed request is worth trying again later.

    A host name that does not resolve, or a certificate that will not verify,
    is a settled fact about the URL rather than a passing condition: it means
    this example is pointed somewhere that no longer answers for it. requests
    reports the first as a ConnectionError wrapping urllib3's
    NameResolutionError and the second as its own SSLError, and neither carries
    a response, so a status code alone cannot tell them apart from a refused
    connection.
    """
    if isinstance(error, requests.exceptions.SSLError):
        return False
    cause = error.args[0] if error.args else None
    if isinstance(getattr(cause, 'reason', None), urllib3.exceptions.NameResolutionError):
        return False

    status = getattr(error.response, 'status_code', None)
    # No status at all means the request never reached an application; 5xx and
    # 429 mean the service cannot serve right now. A 4xx is this example's
    # problem.
    return status is None or status >= 500 or status == 429


def main():

    # Setup a RDF dataset and graph for the harvested items, using the
    # Schema.org vocabulary
    SCHEMA = Namespace("http://schema.org/")

    ds = Dataset()
    ds.bind("schema", SCHEMA)

    g = ds.graph(f"{BASE_URL}/")

    search_url = BASE_URL + "/api/v2/search"
    params={
        'per_page': 10,
        'affiliation': 'https://ror.org/047s2c258', # University of Maryland, College Park
    }

    # Use the Dryad API to get a list of datasets for the specified affiliation
    try:
        response = requests.get(search_url, params=params,
                                timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.JSONDecodeError:
        # JSONDecodeError subclasses RequestException, so this clause has
        # to come first to be reachable.
        print(f'{search_url} did not return JSON', file=sys.stderr)
        # A body that is not JSON means the API changed under this example.
        sys.exit(1)
    except requests.RequestException as error:
        print(f'{search_url} could not be read: {error}', file=sys.stderr)
        # 75 = EX_TEMPFAIL: the condition may clear on its own.
        sys.exit(75 if is_transient(error) else 1)

    for dataset in response['_embedded']['stash:datasets']:
        item_url = dataset['sharingLink']

        print(f"Fetching item: {item_url}")

        # Fetch the dataset page. rdflib can retrieve a URL itself, given
        # source=item_url, but then the HTTP result is invisible: the parser
        # treats every 2xx alike, so a response that carries no document would
        # contribute nothing and look the same as a page without metadata.
        try:
            page = requests.get(item_url, timeout=TIMEOUT_SECONDS)
            page.raise_for_status()
        except requests.RequestException as error:
            print(f'{item_url} could not be read: {error}', file=sys.stderr)
            # 75 = EX_TEMPFAIL: the condition may clear on its own.
            sys.exit(75 if is_transient(error) else 1)

        if page.status_code != 200 or not page.text.strip():
            # A 2xx other than 200, or an empty body, means the request was
            # accepted without the document being sent. Nothing follows about
            # the metadata from a page that never arrived, so ask again later.
            print(f'{item_url} returned HTTP {page.status_code} with '
                  f'{len(page.content)} bytes of body', file=sys.stderr)
            sys.exit(75)

        # Extract the dataset's JSON-LD metadata and add it to the graph. The
        # metadata is carried in a <script type="application/ld+json"> element,
        # and declaring the content type is what tells the JSON-LD parser to
        # look for those rather than read the whole body as JSON-LD.
        source = InputSource(item_url)
        source.setCharacterStream(io.StringIO(page.text))
        source.content_type = "text/html"
        g.parse(source=source, format="json-ld")

    # The JSON-LD parser ignores an HTML document that embeds no JSON-LD, so a
    # page whose metadata has moved or gone parses cleanly and contributes
    # nothing. Every page above was checked to have arrived intact, so an empty
    # graph here means the metadata was not where this example looks for it.
    if len(g) == 0:
        print('No JSON-LD statements were found in the fetched dataset pages',
              file=sys.stderr)
        sys.exit(1)

    # Serialize the dataset to RDF Trig format
    print(ds.serialize(format="trig"))


if __name__ == "__main__":
    main()
