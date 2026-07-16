#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "rdflib==7.6.0",
#     "requests==2.32.3",
# ]
# ///

# Use the Dryad API to harvest JSON-LD metadata for datasetts with authors
# affiliated with the University of Maryland, College Park, and serialize it to
# RDF Trig format.

import json

import requests
from rdflib import Dataset, Namespace

BASE_URL = "https://datadryad.org"

def main():

    # Setup a RDF dataset and graph for the harvested items, using the
    # Schema.org vocabulary
    SCHEMA = Namespace("http://schema.org/")

    ds = Dataset()
    ds.bind("schema", SCHEMA)

    g = ds.graph(f"{BASE_URL}/")

    search_url = BASE_URL + "/api/v2/search"
    params={
        'per_page': 10,
        'affiliation': 'https://ror.org/047s2c258', # University of Maryland, College Park
    }

    # Use the Dryad API to get a list of datasets for the specified affiliation
    response = requests.get(search_url, params=params)

    if not response.ok:
        print(f'Error reading response: {response}')
        return

    response = json.loads(response.text)

    for dataset in response['_embedded']['stash:datasets']:
        item_url = dataset['sharingLink']

        print(f"Fetching item: {item_url}")

        # Extract JSON-LD metadata for the item and add it to the graph
        g.parse(source=item_url, format="json-ld")

    response = requests.get(search_url)

    # Serialize the dataset to RDF Trig format
    print(ds.serialize(format="trig"))


if __name__ == "__main__":
    main()
