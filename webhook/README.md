# Docker Documentation Webhook

Dockerfile for `opendata-webhook` container which:

* Receives GitHub webhook push notifications for repository updates
* If an update occurs for the target branch then:
  * Clone the repo
  * Checkout the target branch
  * Build the Hugo website.

Adapted from [kramergroup/hugo-webhook](https://github.com/kramergroup/hugo-webhook/tree/master).

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
GITHUB_REPO_BRANCH="feat/webhook"
docker run --rm -it -p 9000:9000 \
--read-only \
-v ./tmp:/tmp \
-v ./target:/target \
-e GIT_REPO_URL="https://github.com/umd-lib/umd-lib-opendata.git" \
-e GIT_REPO_BRANCH=$GITHUB_REPO_BRANCH \
opendata-webhook:latest

# Trigger webhook to pull and build
curl -X POST -H "Content-Type: application/json" -d '{"ref": "refs/heads/'$GITHUB_REPO_BRANCH'", "repository": {"clone_url": "https://github.com/umd-lib/umd-lib-opendata.git"}}' http://localhost:9000/hooks/refresh

# Exec into the webhook to observe/debug
docker exec -it $(docker ps | grep opendata-webhook | awk '{print $1}') /bin/bash
```
