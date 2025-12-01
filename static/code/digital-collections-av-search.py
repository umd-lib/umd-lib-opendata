#!/usr/bin/env python3

import urllib.request
import json

# Search Digital Collections Audio/Video using JSON OpenSearch

BASE = 'https://av.lib.umd.edu/'
ENDPOINT = 'https://av.lib.umd.edu/catalog.json'

# Keyword query on 'Maryland'
params = {
    "search_field": "all_fields",
    "q": "maryland",
}

search_url = ENDPOINT + '?' + urllib.parse.urlencode(params)

# Get search results as parsed JSON
with urllib.request.urlopen(search_url) as request:
    response = json.loads(request.read())

    # Iterate over the returned items
    for item in response['data']:
        link = item['links']['self']
        title = item['attributes']['title_tesi']['attributes']['value']

        print('----')
        print(f'Title: {title}')
        print(f'Link:  {link}')
