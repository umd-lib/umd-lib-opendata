#!/usr/bin/env python3

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

ENDPOINT = 'https://api.av.lib.umd.edu/oai/api'

registry = MetadataRegistry()
registry.registerReader('oai_dc', oai_dc_reader)

client = Client(ENDPOINT, registry)
for n, record in enumerate(client.listRecords(metadataPrefix='oai_dc')):
    print('----')
    header, metadata, _ = record
    for md in ('title', 'identifier', 'creator', 'subject'):
        print(f"{md}: {', '.join(metadata[md])}")

    if n == 9:
        break
