#!/usr/bin/env python3

import urllib.request
import json

# Search the Internet Archive

BASE = 'https://archive.org'
ENDPOINT = BASE + '/advancedsearch.php'

# Search the University of Maryland, College Park Collection
params = {
    "q": "collection:(university_maryland_cp)",
    "fl[]": ["identifier", "title"],
    "output": "json",
}

# https://archive.org/advancedsearch.php?q=collection%3A%28university_maryland_cp%29&fl%5B%5D=identifier&fl%5B%5D=title&output=json

search_url = ENDPOINT + '?' + urllib.parse.urlencode(params, doseq=True)
print(search_url)

# Get search results as parsed JSON
with urllib.request.urlopen(search_url) as request:
    response = json.loads(request.read())

    # Iterate over the returned items
    for item in response['response']['docs']:
        link = BASE + "/details/" + item['identifier']
        title = item['title']

        print('----')
        print(f'Title: {title}')
        print(f'Link:  {link}')
