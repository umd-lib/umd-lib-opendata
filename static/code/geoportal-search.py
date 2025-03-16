#!/usr/bin/env python3

import urllib.request
import json

# Search BTAA Geoportal using JSON OpenSearch

ENDPOINT = 'https://geo.btaa.org/'

# Keyword query on 'Maryland'
params = {
    "search_field": "all_fields",
    "q": "maryland",
    "format": "json",
}

# https://geo.btaa.org/?search_field=all_fields&q=maryland&format=json

search_url = ENDPOINT + '?' + urllib.parse.urlencode(params)
print(search_url)
# Get search results as parsed XML
with urllib.request.urlopen(search_url) as request:
    response = json.loads(request.read())

    # Iterate over the returned items
    for item in response['data']:
        link = item['links']['self']

        if ('attributes' in item
           and 'dct_description_sm' in item['attributes']):

            title = item['attributes']['dct_description_sm']['attributes']['value']

        else:
            title = "??"

        print('----')
        print(f'Title: {title}')
        print(f'Link:  {link}')
