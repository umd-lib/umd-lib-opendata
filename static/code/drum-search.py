#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

import socket
import ssl
import urllib.request
import sys
from urllib.error import HTTPError, URLError
from xml.etree import ElementTree

# Search DRUM using OpenSearch

ENDPOINT = 'https://api.drum.lib.umd.edu/server/opensearch/search'

ATOM = '{http://www.w3.org/2005/Atom}'
OPENSEARCH = '{http://a9.com/-/spec/opensearch/1.1/}'

# A host name that does not resolve, or a certificate that will not verify,
# is a settled fact about the URL rather than a passing condition: it means
# this example is pointed somewhere that no longer answers for it. Every other
# connection failure -- refused, reset, timed out -- may succeed on a retry.
PERMANENT_FAILURES = (socket.gaierror, ssl.SSLCertVerificationError)


def search(**params):
    ''' Search DRUM using OpenSearch, using named parameters '''

    # Build the URL
    params['rpp'] = 5  # get first 5 results
    search_url = ENDPOINT + '?' + urllib.parse.urlencode(params)

    print('\n========================')
    print(f'Search URL: {search_url}')

    # Get search results as parsed XML
    try:
        with urllib.request.urlopen(search_url) as request:
            atom = ElementTree.parse(request).getroot()
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

    # A search that matches nothing is a legitimate answer, so check for the
    # OpenSearch envelope rather than for entries: an Atom feed carrying
    # opensearch:totalResults is what says the response was understood.
    if atom.tag != ATOM + 'feed' or atom.find(OPENSEARCH + 'totalResults') is None:
        print(f'{search_url} did not return an OpenSearch Atom feed', file=sys.stderr)
        sys.exit(1)

    # Iterate over the returned items
    for element in atom.findall(ATOM + 'entry'):

        # Extract Item information
        title = element.find(ATOM + 'title').text
        handle_url = element.find(ATOM + 'link').get('href')
        author = element.find(f'{ATOM}author/{ATOM}name').text

        print('----')
        print(f'Title:      {title}')
        print(f'Author:     {author}')
        print(f'Handle URL: {handle_url}')


# phrase is "Black Lives Matter"
search(query='"Black Lives Matter"')


# advisor is smela
# collection is http://hdl.handle.net/1903/2795 (Mechanical Engineering ETDs)
search(query='advisor:smela', scope='a96d44b7-57d2-46ed-80e9-98f316a82a19')


# community is http://hdl.handle.net/1903/2278 (Library Staff Research Works)
search(query='*:*', scope='14dd3089-86f9-4bac-949f-347e0c637984')
