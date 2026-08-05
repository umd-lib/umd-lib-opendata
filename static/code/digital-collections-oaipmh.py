#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "oaipmh==3.2.0",
# ]
# ///

import socket
import ssl
import sys
from itertools import islice
from urllib.error import HTTPError, URLError

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

ENDPOINT = 'https://api.fcrepo.lib.umd.edu/oai/api'

# A host name that does not resolve, or a certificate that will not verify,
# is a settled fact about the URL rather than a passing condition: it means
# this example is pointed somewhere that no longer answers for it. Every other
# connection failure -- refused, reset, timed out -- may succeed on a retry.
PERMANENT_FAILURES = (socket.gaierror, ssl.SSLCertVerificationError)

registry = MetadataRegistry()
registry.registerReader('oai_dc', oai_dc_reader)

client = Client(ENDPOINT, registry)
try:
    records = list(islice(client.listRecords(metadataPrefix='oai_dc'), 10))
except HTTPError as error:
    # oaipmh speaks HTTP through urllib, so it raises urllib's errors.
    print(f'{ENDPOINT} returned HTTP {error.code}: {error.reason}', file=sys.stderr)
    # 75 = EX_TEMPFAIL: the service is reachable but cannot serve right now.
    # A 4xx means this request is no longer valid, which is this example's problem.
    sys.exit(75 if error.code >= 500 or error.code == 429 else 1)
except URLError as error:
    # Nothing answered, so the request was never judged. What stopped it
    # decides whose problem it is.
    print(f'Could not reach {ENDPOINT}: {error.reason}', file=sys.stderr)
    sys.exit(1 if isinstance(error.reason, PERMANENT_FAILURES) else 75)

for record in records:
    print('----')
    header, metadata, _ = record
    for md in ('title', 'identifier', 'creator', 'subject'):
        print(f"{md}: {', '.join(metadata[md])}")
