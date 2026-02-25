#!/usr/bin/env python3

from itertools import islice

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

ENDPOINT = 'https://archives-api.lib.umd.edu/oai'

registry = MetadataRegistry()
registry.registerReader('oai_dc', oai_dc_reader)

client = Client(ENDPOINT, registry)
for record in islice(client.listRecords(metadataPrefix='oai_dc'), 10):
    print('----')
    header, metadata, _ = record
    for md in ('title', 'date', 'identifier'):
        print(f"{md}: {', '.join([ s.replace('\n', '') for s in metadata[md]])}")
