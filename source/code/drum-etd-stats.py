#!/usr/bin/env python3

import urllib.request
import json
import time


ENDPOINT = 'https://api.drum-qa.lib.umd.edu/server/api'
# ENDPOINT = 'https://api.drum.lib.umd.edu/server/api'

# Get a list of item in the Electronic Theses and Dissertations collection

def process_item(item):
    bundles_url = item['_links']['bundles']['href']
    print(bundles_url)
    with urllib.request.urlopen(bundles_url) as request:
        bundles = json.loads(request.read())
        # print(bundles)

        # for bundle in bundles['_embedded']['bundles']:
        #     if bundle['name'] == 'ORIGINAL':
        #         bitstreams_url = bundle['_links']['bitstreams']
        #         with urllib.request.urlopen(bitstreams_url) as request:
        #             bitstreams = json.loads(request.read())
        #             for bitstream in bitstreams['_embedded']['bitstreams']:
        #                 if bitstream['bundleName'] == 'ORIGINAL':
        #                     print(bitstream['uuid'])

items_url = ENDPOINT + '/discover/search/objects?scope=ba3ddc3f-7a58-4fd3-bde5-304938050ea2'

while items_url is not None:
    print(items_url)
    with urllib.request.urlopen(items_url) as request:
        response = json.loads(request.read())
        result = response['_embedded']['searchResult']

        # Iterate over the returned items
        for item in result['_embedded']['objects']:
            item = item['_embedded']['indexableObject']
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
            process_item(item)
            break
            # time.sleep(1)

        if 'next' in response['_links']:
            items_url = response['_links']['next']['href']
        else:
            items_url = None

    break