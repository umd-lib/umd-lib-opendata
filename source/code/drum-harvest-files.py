#!/usr/bin/env python3

# Use the output of drum-harvest-metadata.py to
# download DRUM binaries for each item by scraping
# them from the website.

import sys
from pathlib import Path
import re
import urllib.parse
import os.path

import requests
import yaml

# Harvest DRUM files. If this script is restarted,
# it will skip any items already downloaded


ENDPOINT = 'https://drum.lib.umd.edu'

# Harvest files with these extensions
EXTENSION_INCLUDES = set([
    'pdf', 'xml', 'txt', 'asc', 'htm', 'html', 'doc', 'ppt', 'xls', 'pptx', 'rtf',
    'fm', 'ps', 'eps', 'ai', 'ma', 'latex', 'tex', 'dvi', 'sgm', 'sgml', 'wpd',
    'docx', 'docm', 'ppam', 'ppsm', 'ppsx', 'pptx', 'xlam', 'xslx', 'odt', 'odm',
    'odg', 'odp', 'ods', 'odc', 'odf', 'odb', 'odi', 'oxt', 'sxw', 'sxc', 'sxd',
    'sxi', 'sxg', 'sxm', 'sdw', 'sgl', 'sdc', 'sda', 'sdd', 'sdp', 'smf', 'sds',
    'sdm', 'rdf', 'epub'
])

def harvest(url: str):
    ''' Harvest the binaries for one DRUM item. '''

    # Get the item's handle id
    id = re.sub(r'https?://hdl.handle.net/', '', url)

    # Determine the item directory, skip if exists
    dir = Path('files') / Path(id)
    if dir.exists():
        return

    # Determine the temp directory, error if exists
    temp_dir = dir.parent / Path('temp')

    if temp_dir.exists():
        raise Exception(f'{temp_dir} exists; please review and delete it to proceed')

    temp_dir.mkdir(parents=True)

    # Get the DRUM html page for this item
    response = requests.get(url)

    if not response.ok:
        print(f'Error reading response: {response}')
        return

    body = response.text

    # Iterate over the files available for download
    for m in re.findall(rf'href="(/bitstream/handle/{id}/([^?]+)\?.+?isAllowed=([yn])[^"]*?)"', body):
        file_url, file_name, allowed = m

        # Is this file allowed for anonymous download?
        if allowed == 'y':

            # Does the file have an extension we want to include?
            _, file_extension = os.path.splitext(file_name)
            if file_extension[1:].lower() in EXTENSION_INCLUDES:

                file_url = ENDPOINT + file_url
                file_name = urllib.parse.unquote(file_name)

                file = temp_dir / file_name

                print(f'  downloading {file_url} to {file}')

                # Download via chunked streaming
                response = requests.get(file_url, stream=True)
                with open(file, 'wb') as fd:
                    for chunk in response.iter_content(chunk_size=1024):
                        fd.write(chunk)

    # Rename the temp directory to the item directory
    # This indicates the downloads for this item are complete
    temp_dir.rename(dir)


if __name__ == "__main__":

    # Read the YAML output from dum-harvest-metadata.py
    for item in yaml.safe_load_all(sys.stdin):

        url = item['handle_url']
        title = item['title'].replace('\n', '').replace('\r','')
        print(f'{url}: {title}')

        harvest(url)
