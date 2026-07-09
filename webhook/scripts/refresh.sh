#!/bin/bash

set -euo pipefail

export PATH="${PATH}:/root/go/bin"

echo "INFO: refresh.sh invoked"

if [[ -z "${GIT_REPO_BRANCH:-}" ]]; then
  echo "ERROR: Missing configuration! GIT_REPO_BRANCH cannot be empty" >&2
  exit 1
fi

if [[ -z "${GIT_REPO_URL:-}" ]]; then
  echo "ERROR: Missing configuration! GIT_REPO_URL cannot be empty" >&2
  exit 1
fi

# Ensure this webhook is for the correct branch and repository
REF="refs/heads/${GIT_REPO_BRANCH}"

if [[ "${HOOK_ref:-}" != "${REF}" ]] || [[ "${HOOK_repository_clone_url:-}" != "${GIT_REPO_URL}" ]]; then
  echo "WARN: Validation failed! Ignoring webhook for ref=${HOOK_ref:-} and repository=${HOOK_repository_clone_url:-}" >&2
  exit 0
fi

# Block until the lock is acquired
LOCK_FILE="/tmp/refresh.lock"
echo "INFO: Acquiring the lock: ${LOCK_FILE}"
exec 200>"${LOCK_FILE}" || { echo "ERROR: failed to open lock file ${LOCK_FILE}" >&2; exit 1; }
flock --wait 120 200 || { echo "ERROR: Timed out waiting for lock on ${LOCK_FILE}" >&2; exit 1; }

echo "INFO: Refresh started"

# Make the working directory
CONTENT_DIR=$(mktemp -d -t ci-XXXXXXXXXX)
trap 'rm -rf "${CONTENT_DIR}"' EXIT

echo "INFO: Working directory: ${CONTENT_DIR}"

# Clone the repo
echo "INFO: Clone the repo"
git clone "${GIT_REPO_URL}" "${CONTENT_DIR}"
echo "INFO: CD to ${CONTENT_DIR} and Git Checkout ${GIT_REPO_BRANCH}"
cd "${CONTENT_DIR}" && git checkout "${GIT_REPO_BRANCH}"
echo "INFO: git commit is $(git log -1 --oneline)"

# Build the docs
# --taskfile is a fix for LIBDEVOPS-3143
echo "INFO: Executing task build:docker"
task build:docker -v
