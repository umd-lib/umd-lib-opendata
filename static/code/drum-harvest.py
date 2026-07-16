#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests==2.32.3",
# ]
# ///

# Use the DSpace API to harvest all items in DRUM
#
# If this script is restarted, it will skip any items
# already downloaded, but first you must remove the
# files/temp directory.

import json
from pathlib import Path
import argparse
import time

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
    dir = args.directory / Path(uuid)
    if dir.exists():
        return

    # Setup the temporary item directory
    temp_dir = args.directory / Path('temp')

    if temp_dir.exists():
        if args.delete_temp:
            import shutil
            shutil.rmtree(temp_dir)
            print(f'Deleted existing temp directory: {temp_dir}')
        else:
            raise Exception(f'{temp_dir} exists; please review and delete it to proceed')

    temp_dir.mkdir(parents=True)

    # Write the item file
    if 'item-metadata' in args.harvest:
        with (temp_dir / Path(f'{uuid}.json')).open(mode='w', encoding='utf-8') as f:
            json.dump(item, f)
            f.write('\n')

    # Harvest this item's bundles
    if 'files' in args.harvest:
        harvest_bundles(item, temp_dir)

    # Rename the temp directory to the item directory
    # This indicates the downloads for this item are complete
    temp_dir.rename(dir)


def harvest_items():
    ''' Browse over all items, harvest each one '''

    if args.collection_id:
        items_url = args.endpoint + f'/discover/search/objects?configuration=collection&scope={args.collection_id}'
    else:
        items_url = args.endpoint + '/discover/browses/title/items'

    # Iterate over paged results
    while True:

        response = requests.get(items_url, params={'size': 100})

        if not response.ok:
            print(f'Error reading response: {response}')
            return

        response = json.loads(response.text)

        if args.collection_id:
            response = response['_embedded']['searchResult']

        # Iterate over the returned items
        if args.collection_id:
            for object in response['_embedded']['objects']:
                harvest_item(object['_embedded']['indexableObject'])
        else:
            for item in response['_embedded']['items']:
                harvest_item(item)

        if 'next' in response['_links']:
            items_url = response['_links']['next']['href']
        else:
            print("Harvest complete")
            break

        # Delay between requests
        if args.delay > 0:
            time.sleep(args.delay)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Harvest items from DRUM',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog='''
Example file structure for two items in the <harvest> directory:

harvest
├── 065fa8e1-e9ad-4c4a-ab8e-0f4e34733f47 # Item ID
│   ├── 065fa8e1-e9ad-4c4a-ab8e-0f4e34733f47.json # Item metadata
│   └── Puchtel et al. (2018 Geochimical et Cosmochimica Acta).pdf # Downloaded file for the item
├── 2c7918c8-17c7-449d-ba02-28b92c252cac
│   ├── 24SS_URSP673_15MinuteNeighborhoods_FinalPresentation_POST.pdf
│   ├── 24SS_URSP673_15MinuteNeighborhoods_FinalReport_POST.pdf
│   └── 2c7918c8-17c7-449d-ba02-28b92c252cac.json

If this script is restarted, it will skip any items already downloaded, but
first you must remove the {directory}/temp directory, which may contain files
harvested from an item which was interrupted in progress.
''')

    harvest_options = ['item-metadata', 'files']
    parser.add_argument('--harvest',
                        type=lambda s: [item.strip() for item in s.split(',')],
                        default=', '.join(harvest_options),
                        help=f'Comma-separated list of data to harvest: (default: {", ".join(harvest_options)})')

    parser.add_argument('--delay',
                        type=float,
                        default=2.0,
                        help='Delay in seconds between requests (default: 2.0)')

    parser.add_argument('--delete-temp',
                        action='store_true',
                        default=False,
                        help='Delete the temporary item directory if it exists (default: False)')

    parser.add_argument('--directory',
                        type=Path,
                        default=Path('harvest'),
                        help='Directory to store harvested items (default: harvest)')

    parser.add_argument('--collection-id',
                        type=str,
                        default=None,
                        help='Limit harvesting to items in a collection (default: None)')

    parser.add_argument('--endpoint',
                        type=str,
                        default=ENDPOINT,
                        help=f'DSpace API endpoint base url (default: {ENDPOINT})'
                        )

    global args
    args = parser.parse_args()

    # Validate harvest options
    for option in args.harvest:
        if option not in harvest_options:
            parser.error(f'Invalid --harvest option: {option if option else "<empty>"}')

    # Validate the directory path
    if not args.directory.exists():
        parser.error(f'Directory does not exist: {args.directory}')
    elif not args.directory.is_dir():
        parser.error(f'Invalid --directory option: {args.directory} is not a directory')

    print("Harvest configuration:")
    for arg, value in vars(args).items():
        print(f"  {arg}: {value}")

    harvest_items()
