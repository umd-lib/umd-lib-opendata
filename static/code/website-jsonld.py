#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "rdflib==7.6.0",
#     "requests==2.34.2",
#     "urllib3==2.7.0",
# ]
# ///

# Extract JSON-LD metadata from Libraries Website pages, storing them
# in-memory to a Dataset, then serialize the RDF to stdout in the trig format.

import io
import sys

import requests
import urllib3
from rdflib import Dataset, Namespace
from rdflib.namespace import RDF
from rdflib.parser import InputSource

BASE_URL = "https://www.lib.umd.edu"

OUTPUT_FULL_RDF = False

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
    if isinstance(getattr(cause, "reason", None), urllib3.exceptions.NameResolutionError):
        return False

    status = getattr(error.response, "status_code", None)
    # No status at all means the request never reached an application; 5xx and
    # 429 mean the service cannot serve right now. A 4xx is this example's
    # problem.
    return status is None or status >= 500 or status == 429


def main():

    # Setup a RDF dataset and graph for the harvested pages, using the
    # Schema.org vocabulary
    SCHEMA = Namespace("http://schema.org/")

    ds = Dataset()
    ds.bind("schema", SCHEMA)

    g = ds.graph(f"{BASE_URL}/")

    # Iterate over the sample pages
    for page_path in (
        "/",
        "/find",
        "/visit/libraries",
        "/about/news/2026-08/dedicated-terp-gives-triple-gift",
        "/visit/libraries/mckeldin/elevator-lobbies-front-wing",
    ):

        page_url = f"{BASE_URL}{page_path}"
        print(f"Fetching page: {page_url}")

        # Fetch the page. rdflib can retrieve a URL itself, given
        # source=page_url, but then the HTTP result is invisible: the parser
        # treats every 2xx alike, so a response that carries no document would
        # contribute nothing and look the same as a page without metadata.
        try:
            page = requests.get(page_url, timeout=TIMEOUT_SECONDS)
            page.raise_for_status()
        except requests.RequestException as error:
            print(f"{page_url} could not be read: {error}", file=sys.stderr)
            # 75 = EX_TEMPFAIL: the condition may clear on its own.
            sys.exit(75 if is_transient(error) else 1)

        if page.status_code != 200 or not page.text.strip():
            # A 2xx other than 200, or an empty body, means the request was
            # accepted without the document being sent. Nothing follows about
            # the metadata from a page that never arrived, so ask again later.
            print(f"{page_url} returned HTTP {page.status_code} with "
                  f"{len(page.content)} bytes of body", file=sys.stderr)
            sys.exit(75)

        # Extract the page's JSON-LD metadata and add it to the graph. The
        # metadata is carried in a <script type="application/ld+json"> element,
        # and declaring the content type is what tells the JSON-LD parser to
        # look for those rather than read the whole body as JSON-LD.
        source = InputSource(page_url)
        source.setCharacterStream(io.StringIO(page.text))
        source.content_type = "text/html"
        g.parse(source=source, format="json-ld")

    # The JSON-LD parser ignores an HTML document that embeds no JSON-LD, so a
    # page whose metadata has moved or gone parses cleanly and contributes
    # nothing. Every page above was checked to have arrived intact, so an empty
    # graph here means the metadata was not where this example looks for it.
    if len(g) == 0:
        print("No JSON-LD statements were found in the fetched pages",
              file=sys.stderr)
        sys.exit(1)

    # Serialize the dataset to RDF Trig format
    if OUTPUT_FULL_RDF:
        print(ds.serialize(format="trig"))

    else:
        # Extract an example subset of triples
        subset = Dataset()
        subset.bind("schema", SCHEMA)
        subset_graph = subset.graph(f"{BASE_URL}/")

        subjects = set(g.subjects(RDF.type, SCHEMA.WebPage))
        for subject, predicate, object_ in g:
            if subject in subjects and predicate in (RDF.type, SCHEMA.description):
                subset_graph.add((subject, predicate, object_))

        print(subset.serialize(format="trig"))


if __name__ == "__main__":
    main()
