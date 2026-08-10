#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

import urllib.request
import json
import socket
import ssl
import sys
from urllib.error import HTTPError, URLError


# Search Dryad using the Dryad API

ENDPOINT = 'https://datadryad.org/api/v2'

# A host name that does not resolve, or a certificate that will not verify,
# is a settled fact about the URL rather than a passing condition: it means
# this example is pointed somewhere that no longer answers for it. Every other
# connection failure -- refused, reset, timed out -- may succeed on a retry.
PERMANENT_FAILURES = (socket.gaierror, ssl.SSLCertVerificationError)

# Search for datasets which have authors affiliated with the
# University of Maryland, College Park
params = {
    "affiliation": "https://ror.org/047s2c258",
}

search_url = ENDPOINT + '/search?' + urllib.parse.urlencode(params)
print(search_url)

# Get search results as parsed JSON
try:
    with urllib.request.urlopen(search_url) as request:
        response = json.loads(request.read())
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
except json.JSONDecodeError:
    print(f'{ENDPOINT} did not return JSON', file=sys.stderr)
    # A body that is not JSON means the API changed under this example.
    sys.exit(1)

# A search that matches nothing is a legitimate answer, so check for the HAL
# envelope rather than for datasets: "_embedded" carrying a "stash:datasets"
# list is what says the response was understood.
datasets = response.get('_embedded', {}).get('stash:datasets')
if not isinstance(datasets, list):
    print(f'{search_url} did not return an "_embedded.stash:datasets" list',
          file=sys.stderr)
    sys.exit(1)

# Iterate over the returned items
for item in datasets:
    link = item['identifier'].replace('doi:', 'https://doi.org/')
    title = item['title']

    print('----')
    print(f'Title: {title}')
    print(f'Link:  {link}')
