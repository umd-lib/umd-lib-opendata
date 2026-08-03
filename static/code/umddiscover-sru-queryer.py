#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "sru-queryer==2.1.3",
# ]
# ///

import sys
from xml.etree import ElementTree

from sru_queryer import SRUQueryer, SearchClause
from sru_queryer.exceptions import (
    ExplainResponseContentTypeException,
    ExplainResponseParserException,
    NoExplainResponseException,
)

# Search UMD Discover via sru-queryer package

ENDPOINT = 'https://usmai-umcp.alma.exlibrisgroup.com/view/sru/01USMAI_UMCP'

# sru-queryer does not surface the HTTP status: it discards the response code
# and reports an unparseable body instead, so an error page from the server
# arrives here as ExplainResponseContentTypeException.
try:
    queryer = SRUQueryer(ENDPOINT)
    sc = SearchClause("alma", "all_for_ui", "=", "libraries")
    content = queryer.search_retrieve(sc, record_schema="dc")
    response = ElementTree.fromstring(content.decode('utf-8'))
except NoExplainResponseException as error:
    # sru-queryer raises this both when the connection fails and when the
    # server answers with a document that has no explainResponse in it -- that
    # is, when the URL is no longer an SRU service. The two arrive as the same
    # exception type with only the message to tell them apart, so this treats
    # them all as a broken example rather than risk reporting a dead endpoint
    # as a passing outage.
    print(f'{ENDPOINT} did not return an SRU explainResponse: {error}',
          file=sys.stderr)
    sys.exit(1)
except PermissionError:
    print(f'{ENDPOINT} refused the request (HTTP 401 or 403)', file=sys.stderr)
    # A 401 or 403 means this request is no longer valid, which is this
    # example's problem.
    sys.exit(1)
except (ExplainResponseContentTypeException, ExplainResponseParserException,
        ElementTree.ParseError):
    print(f'{ENDPOINT} did not return SRU XML', file=sys.stderr)
    # A body that is not SRU XML means the service changed under this example.
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
    print(f'{ENDPOINT} did not return an SRU searchRetrieveResponse', file=sys.stderr)
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
