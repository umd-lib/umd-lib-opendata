#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "sru-queryer==2.1.3",
# ]
# ///

from xml.etree import ElementTree

from sru_queryer import SRUQueryer, SearchClause

# Search UMD Discover via sru-queryer package

ENDPOINT = 'https://usmai-umcp.alma.exlibrisgroup.com/view/sru/01USMAI_UMCP'

queryer = SRUQueryer(ENDPOINT)
sc = SearchClause("alma", "all_for_ui", "=", "libraries")
content = queryer.search_retrieve(sc, record_schema="dc")

# Get search results as parsed XML
response = ElementTree.fromstring(content.decode('utf-8'))

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
