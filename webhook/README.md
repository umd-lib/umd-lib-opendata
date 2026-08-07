# Docker Documentation Webhook

Dockerfile for `opendata-webhook` container which:

* Receives GitHub webhook push notifications for repository updates
* If an update occurs for the target branch then:
  * Clone the repo
  * Checkout the target branch
  * Build the Hugo website to a local directory
  * Sync the built site directly to S3 bucket

Adapted from
[kramergroup/hugo-webhook](https://github.com/kramergroup/hugo-webhook/tree/master).

## Build Strategy

The webhook uses a two-stage build-then-sync approach:

1. **Build locally**: Hugo builds to a local POSIX filesystem directory
   (`/tmp/ci-*/build`)
2. **Sync to S3**: rclone syncs the built site directly to an S3 bucket

### Why Not Build Directly to S3-Backed Filesystem?

Hugo v0.164.0's static file copying fails with "operation not permitted" errors
when building directly to S3-backed (non-POSIX) filesystems like
`mountpoint-s3`. This happens because:

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

Building to a local directory first, then using rclone to sync to S3, avoids
Hugo's file comparison operations on the S3 filesystem entirely.

## AWS Credentials

The container uses rclone with `env_auth = true`, which means it will
authenticate using:

1. **IAM Instance Profile** (recommended for EKS/EC2 deployments)
2. **Environment variables**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`,
   `AWS_SESSION_TOKEN`
3. **AWS config files** (if mounted into the container)

## Testing

### Local

```bash
# Build the webhook
docker build -t opendata-webhook:latest .

# Create temporary directory for the git repo clone
mkdir -p ./tmp

# Run the opendata-webhook container
docker run --rm -it -p 9000:9000 \
--read-only \
-v ./tmp:/tmp \
-e GIT_REPO_URL="https://github.com/umd-lib/umd-lib-opendata.git" \
-e GIT_REPO_BRANCH="feat/webhook" \
-e GIT_REPO_WEBHOOK_SECRET="example-secret" \
-e S3_BUCKET="umd-lib-local-opendata" \
opendata-webhook:latest

# Trigger webhook to pull and build
bash test-webhook.sh

# Verify files were synced to S3
aws s3 ls s3://umd-lib-test-opendata/ --recursive | grep -E "code/|index.html"

# Exec into the webhook to observe/debug
docker exec -it $(docker ps | grep opendata-webhook | awk '{print $1}') /bin/bash
```

### Required Environment Variables

* `GIT_REPO_URL` - GitHub repository URL to clone
* `GIT_REPO_BRANCH` - Git branch to checkout and build
* `GIT_REPO_WEBHOOK_SECRET` - Secret for validating webhook signatures
* `S3_BUCKET` - S3 bucket name (path within bucket) to sync built site to
