#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyoai==2.5.0",
#     # pyoai needs the legacy pkg_resources API (setuptools<81) and lxml<5
#     "setuptools==70.2.0",
#     "lxml==4.9.4",
# ]
# ///

from itertools import islice

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

ENDPOINT = 'https://api.fcrepo.lib.umd.edu/oai/api'

registry = MetadataRegistry()
registry.registerReader('oai_dc', oai_dc_reader)

client = Client(ENDPOINT, registry)
for record in islice(client.listRecords(metadataPrefix='oai_dc'), 10):
    print('----')
    header, metadata, _ = record
    for md in ('title', 'identifier', 'creator', 'subject'):
        print(f"{md}: {', '.join(metadata[md])}")
