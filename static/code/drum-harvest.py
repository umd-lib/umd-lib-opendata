#!/usr/bin/env python3

# Use the DSpace API to harvest all items in DRUM
#
# If this script is restarted, it will skip any items
# already downloaded, but first you must remove the
# files/temp directory.

import logging
from http.client import HTTPConnection
import sys
import json
from pathlib import Path

import requests

ENDPOINT = 'https://api.drum.lib.umd.edu/server/api'


def harvest_bitstream(bitstream, dir):
    ''' Harvest one bitstream for one item. '''

    if bitstream['embargoRestriction'] != "NONE":
        return

    if 'content' not in bitstream['_links']:
        return

    name = bitstream['name']
    content_url = bitstream['_links']['content']['href']

    file = dir / name

    print(f'  downloading {file}')

    # Download via chunked streaming
    response = requests.get(content_url, stream=True)
    with open(file, 'wb') as fd:
        for chunk in response.iter_content(chunk_size=1024):
            fd.write(chunk)


def harvest_bitstreams(bundle, dir):
    ''' Harvest bitstreams for one item. '''

    if 'bitstreams' not in bundle['_links']:
        return

    bitstreams_url = bundle['_links']['bitstreams']['href']

    response = requests.get(bitstreams_url)

    if not response.ok:
        print(f'Error reading response: {response}')
        return

    response = json.loads(response.text)

    # Iterate over the returned bitstreams
    for bitstream in response['_embedded']['bitstreams']:
        harvest_bitstream(bitstream, dir)


def harvest_bundles(item, dir):
    ''' Harvest bundles for one item. '''

    if 'bundles' not in item['_links']:
        return

    bundles_url = item['_links']['bundles']['href']

    response = requests.get(bundles_url)

    if not response.ok:
        print(f'Error reading response: {response}')
        return

    response = json.loads(response.text)

    # Iterate over the returned bundles
    for bundle in response['_embedded']['bundles']:
        if bundle['name'] == 'ORIGINAL':
            harvest_bitstreams(bundle, dir)


def harvest_item(item):
    ''' Harvest one item. '''

    md = item['metadata']
    uuid = item['uuid']
    if 'dc.title' in md:
        title = "; ".join(entry['value'] for entry in md['dc.title'])
    else:
        title = "n/a"

    print(f'{uuid}: {title}')

    # Determine the item directory, skip if exists
    dir = Path('files') / Path(uuid)
    if dir.exists():
        return

    # Determine the temp directory, error if exists
    temp_dir = dir.parent / Path('temp')

    if temp_dir.exists():
        raise Exception(f'{temp_dir} exists; please review and delete it to proceed')

    temp_dir.mkdir(parents=True)

    # Write the item file
    with (temp_dir / Path(f'{uuid}.json')).open(mode='w', encoding='utf-8') as f:
        json.dump(item, f)

    # Harvest this item's bundles
    harvest_bundles(item, temp_dir)

    # Rename the temp directory to the item directory
    # This indicates the downloads for this item are complete
    temp_dir.rename(dir)


def harvest_items():
    ''' Browse over all items, harvest each one '''

    items_url = ENDPOINT + '/discover/browses/title/items'

    # Iterate over paged results
    while True:

        response = requests.get(items_url)

        if not response.ok:
            print(f'Error reading response: {response}')
            return

        response = json.loads(response.text)

        # Iterate over the returned items
        for item in response['_embedded']['items']:
            harvest_item(item)

        if 'next' in response['_links']:
            items_url = response['_links']['next']['href']
        else:
            break


if __name__ == "__main__":
    harvest_items()
