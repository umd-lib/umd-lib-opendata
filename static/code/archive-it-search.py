#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

import urllib.request
from xml.etree import ElementTree

# Search Archive-It using XML OpenSearch

ENDPOINT = 'https://archive-it.org/search-master/opensearch'

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
with urllib.request.urlopen(search_url) as request:
    result = ElementTree.parse(request).getroot()

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
