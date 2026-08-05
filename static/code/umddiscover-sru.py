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

# Search UMD Discover via SRU

ENDPOINT = 'https://usmai-umcp.alma.exlibrisgroup.com/view/sru/01USMAI_UMCP'

# A host name that does not resolve, or a certificate that will not verify,
# is a settled fact about the URL rather than a passing condition: it means
# this example is pointed somewhere that no longer answers for it. Every other
# connection failure -- refused, reset, timed out -- may succeed on a retry.
PERMANENT_FAILURES = (socket.gaierror, ssl.SSLCertVerificationError)

# Build the URL
params = {
    "version": "1.2",
    "operation": "searchRetrieve",
    "query": "alma.all_for_ui=\"libraries\"",
    "recordSchema": "dc",
}
search_url = ENDPOINT + '?' + urllib.parse.urlencode(params)

print('\n========================')
print(f'Search URL: {search_url}')

# Get search results as parsed XML
try:
    with urllib.request.urlopen(search_url) as request:
        response = ElementTree.parse(request).getroot()
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

NAMESPACES = {
    'srw': 'http://www.loc.gov/zing/srw/',
    'srw_dc': 'info:srw/schema/1/dc-schema',
    'dc': 'http://purl.org/dc/elements/1.1/',
}

# A search that matches nothing is a legitimate answer, and SRU reports it as
# numberOfRecords 0 with an empty <records/>. So check for numberOfRecords,
# which every searchRetrieveResponse carries, rather than for records.
if response.find('srw:numberOfRecords', NAMESPACES) is None:
    print(f'{search_url} did not return an SRU searchRetrieveResponse', file=sys.stderr)
    sys.exit(1)

records = response.find('srw:records', NAMESPACES)

# Iterate over the returned items
for record in records if records is not None else []:

    dc = record.find('srw:recordData', NAMESPACES).find('srw_dc:dc', NAMESPACES)

    # Extract Item information
    title = dc.find('dc:title', NAMESPACES).text
    contributor = "; ".join([c.text for c in dc.findall('dc:contributor', NAMESPACES)])

    print('----')
    print(f'Title:       {title}')
    print(f'Contributor: {contributor}')
