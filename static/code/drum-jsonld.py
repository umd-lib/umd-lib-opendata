#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "rdflib==7.6.0",
#     "requests==2.32.3",
# ]
# ///

# Use the DSpace API to harvest JSON-LD metadata for items in the UMD Data
# Community collection in DRUM, and serialize it to RDF Trig format.

import json

import requests
from rdflib import Dataset, Namespace

ENDPOINT = 'https://api.drum.lib.umd.edu/server/api'
BASE_URL = 'https://drum.lib.umd.edu'
SCOPE = '7ad10635-e9f1-4f35-a1c9-52c94761192f' # UMD Data Community


def main():

    # Setup a RDF dataset and graph for the harvested items, using the
    # Schema.org vocabulary
    SCHEMA = Namespace("http://schema.org/")

    ds = Dataset()
    ds.bind("schema", SCHEMA)

    g = ds.graph(f'{BASE_URL}/')

    # Use the DSpace API to get a list of items in the specified collection
    # (scope)
    items_url = f'{ENDPOINT}/discover/search/objects?configuration=collection&scope={SCOPE}'

    response = requests.get(items_url, params={'size': 10})

    if not response.ok:
        print(f'Error reading response: {response}')
        return

    response = json.loads(response.text)

    response = response['_embedded']['searchResult']

    # Iterate over the returned items
    for object in response['_embedded']['objects']:
        uuid = object['_embedded']['indexableObject']['uuid']
        item_url = f'{BASE_URL}/items/{uuid}'

        print(f'Fetching item: {item_url}')

        # Extact JSON-LD metadata for the item and add it to the graph
        g.parse(source=item_url, format='json-ld')

    # Serialize the dataset to RDF Trig format
    print(ds.serialize(format='trig'))


if __name__ == "__main__":
    main()
