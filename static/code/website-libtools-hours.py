#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

import urllib.request
import json

# Retrieve McKeldin hours from libtools search

BASE = 'https://api.www.lib.umd.edu/api/libtools/'
ENDPOINT = 'mckeldin/hours/today'

hours_url = BASE + ENDPOINT

# Get search results as parsed JSON
with urllib.request.urlopen(hours_url) as request:
    response = json.loads(request.read())

    status = response['status']

    print('----')
    print(f'McKeldin Hours: {status}')
