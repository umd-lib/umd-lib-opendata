#!/usr/bin/env python3

import urllib.request
import json


# Search Dryad using the Dryad API

ENDPOINT = 'https://datadryad.org/api/v2'

# Search for datasets which have authors affiliated with the
# University of Maryland, College Park
params = {
    "affiliation": "https://ror.org/047s2c258",
}

search_url = ENDPOINT + '/search?' + urllib.parse.urlencode(params)
print(search_url)

# Get search results as parsed JSON
with urllib.request.urlopen(search_url) as request:
    response = json.loads(request.read())

    # Iterate over the returned items
    for item in response['_embedded']['stash:datasets']:
        link = item['identifier'].replace('doi:', 'https://doi.org/')
        title = item['title']

        print('----')
        print(f'Title: {title}')
        print(f'Link:  {link}')
