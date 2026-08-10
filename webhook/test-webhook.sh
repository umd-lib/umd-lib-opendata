#!/bin/bash -x
# Test script for triggering the webhook locally

signature=$(python3 test-secret.py)

curl \
-X POST \
-H "Content-Type: application/json" \
-H "X-Hub-Signature-256: ${signature}" \
--data-binary '@test-payload.json' \
http://localhost:9000/hooks/refresh
