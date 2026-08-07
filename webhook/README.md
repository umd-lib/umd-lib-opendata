# Docker Documentation Webhook

Dockerfile for `opendata-webhook` container which:

* Receives GitHub webhook push notifications for repository updates
* If an update occurs for the target branch then:
  * Clone the repo
  * Checkout the target branch
  * Build the Hugo website to a local directory
  * Copy the built site to the target directory

Adapted from
[kramergroup/hugo-webhook](https://github.com/kramergroup/hugo-webhook/tree/master).

## Build Strategy

The webhook uses a two-stage build-then-copy approach to work reliably with
S3-backed target filesystems:

1. **Build locally**: Hugo builds to a local POSIX filesystem directory
   (`/tmp/ci-*/build`)
2. **Copy to target**: The built site is copied to `/target` using Python's
   `shutil`

### Why Not Build Directly to /target?

When `/target` is mounted as an S3-backed (non-POSIX) filesystem (e.g., using
`mountpoint-s3`), Hugo v0.164.0's static file copying fails with "operation not
permitted" errors. This happens because:

* Hugo's dependency `github.com/spf13/fsync` attempts to **open and read
  destination files** before copying to check if they're identical
* On S3 filesystems, if files from a previous build are still uploading in the
  background, the filesystem returns `EPERM` when trying to open them
* This creates a race condition between Hugo's file comparison and S3's
  eventual consistency model

Generated HTML/CSS/JS files succeed because Hugo writes them directly without
pre-existing file checks. Static files (`.py`, images, etc.) fail because they
go through `fsync.Sync()` which always calls `equal()` to compare files.

**References**:

* [mountpoint-s3 #1344](https://github.com/awslabs/mountpoint-s3/issues/1344) -
  EPERM errors on file reopening
* Hugo uses `fsync` library which assumes POSIX semantics where written files
  are immediately readable

Building to a local directory first, then copying to `/target`, avoids Hugo's
file comparison operations on the S3 filesystem entirely.

## Testing

### Local

```bash
# Build the webhook
docker build -t opendata-webhook:latest .

# Create temporary directory for the git repo clone
mkdir -p ./tmp

# Create the target directory for the built website
mkdir -p ./target

# Run the opendata-webhook container
docker run --rm -it -p 9000:9000 \
--read-only \
-v ./tmp:/tmp \
-v ./target:/target \
-e GIT_REPO_URL="https://github.com/umd-lib/umd-lib-opendata.git" \
-e GIT_REPO_BRANCH="feat/webhook" \
-e GIT_REPO_WEBHOOK_SECRET="example-secret" \
opendata-webhook:latest

# Trigger webhook to pull and build
bash test-webhook.sh

# Exec into the webhook to observe/debug
docker exec -it $(docker ps | grep opendata-webhook | awk '{print $1}') /bin/bash
```
