#!/usr/bin/env python3

import urllib.request
import json

# Get a list of items from DRUM using the REST API

ENDPOINT = 'https://api.drum.lib.umd.edu/server/api'

items_url = ENDPOINT + '/discover/browses/title/items'

# Get JSON results
with urllib.request.urlopen(items_url) as request:
    response = json.loads(request.read())

    # Iterate over the returned items
    for item in response['_embedded']['items']:
        md = item['metadata']
        if 'dc.identifier.uri' in md:
            link = "; ".join(entry['value'] for entry in md['dc.identifier.uri'])
        else:
            link = "n/a"
        if 'dc.title' in md:
            title = "; ".join(entry['value'] for entry in md['dc.title'])
        else:
            title = "n/a"

        print('----')
        print(f'Title: {title}')
        print(f'Link:  {link}')
