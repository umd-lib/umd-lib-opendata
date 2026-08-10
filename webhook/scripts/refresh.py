#!/usr/bin/env python3

import os
import sys
import subprocess
import tempfile
import fcntl
import time
import shutil

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
    s3_bucket = os.environ.get('S3_BUCKET', '')

    if not git_repo_branch:
        log_error("Missing configuration! GIT_REPO_BRANCH cannot be empty")
        sys.exit(1)

    if not git_repo_url:
        log_error("Missing configuration! GIT_REPO_URL cannot be empty")
        sys.exit(1)

    if not s3_bucket:
        log_error("Missing configuration! S3_BUCKET cannot be empty")
        sys.exit(1)

    return git_repo_branch, git_repo_url, s3_bucket

def validate_webhook(git_repo_branch, git_repo_url):
    """Validate webhook payload matches expected repository and branch."""
    expected_ref = f"refs/heads/{git_repo_branch}"
    hook_ref = os.environ.get('HOOK_ref', '')
    hook_clone_url = os.environ.get('HOOK_repository_clone_url', '')

    if hook_ref != expected_ref or hook_clone_url != git_repo_url:
        log_warn(f"Validation failed! Ignoring webhook for ref={hook_ref} and repository={hook_clone_url}")
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
    git_repo_branch, git_repo_url, s3_bucket = validate_environment()

    # Validate webhook
    validate_webhook(git_repo_branch, git_repo_url)

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

            # Build the docs to a local directory first
            # This avoids Hugo's fsync operations on S3-backed filesystems
            # which can fail with EPERM when Hugo tries to open existing files
            # for comparison during static file copying. Building to a local
            # POSIX filesystem first, then copying, is more reliable.
            log_info("Executing task build:docker")
            run_command("task build:docker -v", cwd=content_dir)

            # Copy built site to S3 bucket directory
            log_info(f"Copying built site to S3 bucket: {s3_bucket}")

            build_dir = os.path.join(content_dir, 'build')

            # Use rclone to sync the built site to the S3 bucket
            if os.path.exists(build_dir):
                try:
                    run_command(f"rclone --config /etc/rclone.conf --verbose --delete-during sync {build_dir} s3:{s3_bucket}")
                    log_info(f"Site successfully copied to S3 bucket: {s3_bucket}")
                except subprocess.CalledProcessError as e:
                    log_error("rclone sync failed. Check: AWS credentials (env_auth), bucket permissions, network connectivity")
                    raise
            else:
                log_error(f"Build directory not found: {build_dir}")
                sys.exit(1)

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
