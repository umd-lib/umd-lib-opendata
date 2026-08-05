#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

import urllib.request
import socket
import ssl
import sys
from urllib.error import HTTPError, URLError
from xml.etree import ElementTree

# Search Archive-It using XML OpenSearch

ENDPOINT = 'https://archive-it.org/search-master/opensearch'

# A host name that does not resolve, or a certificate that will not verify,
# is a settled fact about the URL rather than a passing condition: it means
# this example is pointed somewhere that no longer answers for it. Every other
# connection failure -- refused, reset, timed out -- may succeed on a retry.
PERMANENT_FAILURES = (socket.gaierror, ssl.SSLCertVerificationError)

# Visit the UMD Organization at https://archive-it.org/organizations/408
# Select one of the collections, e.g., Special Collections at
# https://archive-it.org/collections/2269.  The Collection ID is 2269.

# Keyword query on 'Maryland'
params = {
    "search_field": "all_fields",
    "q": "maryland",
    "i": "2269",  # Collection ID
}

search_url = ENDPOINT + '?' + urllib.parse.urlencode(params)

# Get search results as parsed XML
try:
    with urllib.request.urlopen(search_url) as request:
        result = ElementTree.parse(request).getroot()
except HTTPError as error:
    print(f'{ENDPOINT} returned HTTP {error.code}: {error.reason}', file=sys.stderr)
    # 75 = EX_TEMPFAIL: the service is reachable but cannot serve right now.
    # A 4xx means this request is no longer valid, which is this example's problem.
    sys.exit(75 if error.code >= 500 or error.code == 429 else 1)
except URLError as error:
    # Nothing answered, so the request was never judged. What stopped it
    # decides whose problem it is.
    print(f'Could not reach {ENDPOINT}: {error.reason}', file=sys.stderr)
    sys.exit(1 if isinstance(error.reason, PERMANENT_FAILURES) else 75)
except ElementTree.ParseError:
    print(f'{ENDPOINT} did not return XML', file=sys.stderr)
    # A body that is not XML means the API changed under this example.
    sys.exit(1)

# Iterate over the returned items
for element in result.findall('channel/item'):

    # Extract Item information
    title = element.find('title').text
    link = element.find('link').text
    date = element.find('date').text

    print('----')
    print(f'Title:      {title}')
    print(f'Date:     {date}')
    print(f'Link: {link}')
