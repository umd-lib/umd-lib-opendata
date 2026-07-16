#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

import urllib.request
from xml.etree import ElementTree

# Search UMD Discover via SRU

ENDPOINT = 'https://usmai-umcp.alma.exlibrisgroup.com/view/sru/01USMAI_UMCP'

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
with urllib.request.urlopen(search_url) as request:
    response = ElementTree.parse(request).getroot()

    NAMESPACES = {
        'srw': 'http://www.loc.gov/zing/srw/',
        'srw_dc': 'info:srw/schema/1/dc-schema',
        'dc': 'http://purl.org/dc/elements/1.1/',
    }

    # Iterate over the returned items
    for record in response.find('srw:records', NAMESPACES):

        dc = record.find('srw:recordData', NAMESPACES).find('srw_dc:dc', NAMESPACES)

        # Extract Item information
        title = dc.find('dc:title', NAMESPACES).text
        contributor = "; ".join([c.text for c in dc.findall('dc:contributor', NAMESPACES)])

        print('----')
        print(f'Title:       {title}')
        print(f'Contributor: {contributor}')
