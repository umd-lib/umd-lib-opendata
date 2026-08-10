#!/usr/bin/env python3
# Generate the example webhook signature using the example secret
import hashlib
import hmac

# Shared Webhook Secret
secret="example-secret"

# Payload from file
with open("test-payload.json", "rb") as f:
    payload = f.read()

hash_object = hmac.new(secret.encode('utf-8'), msg=payload, digestmod=hashlib.sha256)
print("sha256=" + hash_object.hexdigest())

