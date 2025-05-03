#!/usr/bin/env python3

import urllib.request
import json
import time


# ENDPOINT = 'https://api.drum-qa.lib.umd.edu/server/api'
ENDPOINT = 'https://api.drum.lib.umd.edu/server/api'

# Accession count by year
stats = {}

# Get a list of item in the Electronic Theses and Dissertations collection

# def process_bundle(bundle):
#     if bundle['name'] == 'ORIGINAL':
#         bitstreams_url = bundle['_links']['bitstreams']['href']
#         print(bitstreams_url)
#         with urllib.request.urlopen(bitstreams_url) as request:
#             bitstreams = json.loads(request.read())
#             for bitstream in bitstreams['_embedded']['bitstreams']:
#                 size_bytes = int(bitstream['sizeBytes'])
#                 print(size_bytes)


def process_item(item):
    # bundles_url = item['_links']['bundles']['href']
    # print(bundles_url)
    # with urllib.request.urlopen(bundles_url) as request:
        # bundles = json.loads(request.read())
        # for bundle in bundles['_embedded']['bundles']:
        #     process_bundle(bundle)

    year_accessioned = item['metadata']['dc.date.accessioned'][0]['value'][0:4]
    if year_accessioned not in stats:
        stats[year_accessioned] = 0
    stats[year_accessioned] += 1

items_url = ENDPOINT + '/discover/search/objects?scope=ba3ddc3f-7a58-4fd3-bde5-304938050ea2&size=100'

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

            for backoff in [0,2,3,5,8,13,21,34,55,89,144,233,377,610,987]:
                time.sleep(backoff)
                try:
                    process_item(item)
                    break
                except urllib.error.HTTPError as e:
                    print(f'HTTPError: {e}')
                    # if e.code == 429:
                    #     print('Rate limit exceeded, sleeping...')
                    #     time.sleep(60)
                    # else:
                    #     raise
                except Exception as e:
                    print(f'Error: {e}')
                    # raise

        if 'next' in result['_links']:
            items_url = result['_links']['next']['href']
        else:
            items_url = None

    # break

for year in sorted(stats.keys()):
    print(f'{year}, {stats[year]}')
