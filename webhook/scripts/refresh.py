#!/usr/bin/env python3

import os
import sys
import subprocess
import tempfile
import fcntl
import time
import shutil
import hashlib
import hmac

def log_info(message):
    """Print INFO message to stdout."""
    print(f"INFO: {message}", flush=True)

def log_warn(message):
    """Print WARN message to stderr."""
    print(f"WARN: {message}", file=sys.stderr, flush=True)

def log_error(message):
    """Print ERROR message to stderr."""
    print(f"ERROR: {message}", file=sys.stderr, flush=True)

def validate_environment():
    """Validate required environment variables are set."""
    git_repo_branch = os.environ.get('GIT_REPO_BRANCH', '')
    git_repo_url = os.environ.get('GIT_REPO_URL', '')
    git_repo_secret = os.environ.get('GIT_REPO_SECRET', '')
    git_repo_skip_secret_validation = os.environ.get('GIT_REPO_SKIP_SECRET_VALIDATION', 'false')

    if not git_repo_branch:
        log_error("Missing configuration! GIT_REPO_BRANCH cannot be empty")
        sys.exit(1)

    if not git_repo_url:
        log_error("Missing configuration! GIT_REPO_URL cannot be empty")
        sys.exit(1)

    if not git_repo_secret and git_repo_skip_secret_validation != 'true':
        log_error("Missing configuration! GIT_REPO_SECRET cannot be empty")
        sys.exit(1)

    return git_repo_branch, git_repo_url, git_repo_secret, git_repo_skip_secret_validation

def validate_webhook(git_repo_branch, git_repo_url, git_repo_secret, git_repo_skip_secret_validation):
    """Validate webhook payload matches expected repository and branch."""
    expected_ref = f"refs/heads/{git_repo_branch}"
    hook_ref = os.environ.get('HOOK_ref', '')
    hook_clone_url = os.environ.get('HOOK_repository_clone_url', '')
    hook_payload = os.environ.get('HOOK_payload', '')
    hook_signature = os.environ.get('HOOK_signature', '')

    log_info(f"{hook_payload=}")
    log_info(f"{hook_signature=}")

    if git_repo_skip_secret_validation == 'true':
        log_warn("GIT_REPO_SKIP_SECRET_VALIDATION=true, skipping webhook secret validation")
    else:
        if not hook_payload:
            log_warn(f"Validation failed, missing payload! Ignoring webhook for ref={hook_ref}, repository={hook_clone_url}")
            sys.exit(0)

        # Validate the signature
        validate_signature(hook_payload.encode('utf-8'), git_repo_secret, hook_signature)

    if hook_ref != expected_ref or hook_clone_url != git_repo_url:
        log_warn(f"Validation failed, url or branch do not match! Ignoring webhook for ref={hook_ref}, repository={hook_clone_url}")
        sys.exit(0)

def validate_signature(payload_body, secret_token, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Log warnings and exit(0) if unable to verify the signature.

    Args:
        payload_body: original request body to verify
        secret_token: GitHub app webhook secret
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    if not signature_header:
        log_warn("Secret validation failed! x-hub-signature-256 header is missing")
        sys.exit(0)

    hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
        log_warn("Secret validation failed! expected signature does not match x-hub-signature-256 header")
        sys.exit(0)

def acquire_lock(lock_file, timeout=120):
    """Acquire file lock with timeout."""
    log_info(f"Acquiring the lock: {lock_file}")

    try:
        lock_fd = os.open(lock_file, os.O_CREAT | os.O_WRONLY, 0o644)
    except OSError as e:
        log_error(f"failed to open lock file {lock_file}: {e}")
        sys.exit(1)

    start_time = time.time()

    while True:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return lock_fd
        except BlockingIOError:
            elapsed = time.time() - start_time
            if elapsed >= timeout:
                log_error(f"Timed out waiting for lock on {lock_file}")
                os.close(lock_fd)
                sys.exit(1)
            time.sleep(0.5)

def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return the result."""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )

    if result.stdout:
        print(result.stdout, end='')
    if result.stderr:
        print(result.stderr, end='', file=sys.stderr)

    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd)

    return result

def main():
    """Main refresh workflow."""
    log_info("refresh.py invoked")

    # Extend PATH to include Go binaries
    go_bin_path = "/root/go/bin"
    current_path = os.environ.get('PATH', '')
    if go_bin_path not in current_path:
        os.environ['PATH'] = f"{current_path}:{go_bin_path}"

    # Validate environment
    git_repo_branch, git_repo_url, git_repo_secret, git_repo_skip_secret_validation = validate_environment()

    # Validate webhook
    validate_webhook(git_repo_branch, git_repo_url, git_repo_secret, git_repo_skip_secret_validation)

    # Acquire lock
    lock_file = "/tmp/refresh.lock"
    lock_fd = acquire_lock(lock_file, timeout=120)

    try:
        log_info("Refresh started")

        # Create temporary working directory
        content_dir = tempfile.mkdtemp(prefix='ci-', dir='/tmp')
        log_info(f"Working directory: {content_dir}")

        try:
            # Clone the repository
            log_info("Clone the repo")
            run_command(f"git clone {git_repo_url} {content_dir}")

            # Checkout branch
            log_info(f"CD to {content_dir} and Git Checkout {git_repo_branch}")
            run_command(f"git checkout {git_repo_branch}", cwd=content_dir)

            # Log current commit
            result = run_command("git log -1 --oneline", cwd=content_dir)
            log_info(f"git commit is {result.stdout.strip()}")

            # Build the docs
            log_info("Executing task build:docker")
            run_command("task build:docker -v", cwd=content_dir)

        finally:
            # Clean up temporary directory
            shutil.rmtree(content_dir, ignore_errors=True)

    finally:
        # Release lock
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        os.close(lock_fd)

if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as e:
        log_error(f"Command failed with exit code {e.returncode}")
        sys.exit(1)
    except Exception as e:
        log_error(f"Unexpected error: {e}")
        sys.exit(1)
