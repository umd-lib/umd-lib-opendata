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

    if not git_repo_branch:
        log_error("Missing configuration! GIT_REPO_BRANCH cannot be empty")
        sys.exit(1)

    if not git_repo_url:
        log_error("Missing configuration! GIT_REPO_URL cannot be empty")
        sys.exit(1)

    return git_repo_branch, git_repo_url

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
    git_repo_branch, git_repo_url = validate_environment()

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
            # POSIX filesystem first, then copying to /target, is more reliable.
            log_info("Executing task build:docker")
            run_command("task build:docker -v", cwd=content_dir)

            # Copy built site to S3-backed target directory
            log_info("Copying built site to /target")
            build_dir = os.path.join(content_dir, 'build')

            # Use rsync-like behavior: overwrite existing files, create new ones
            # shutil.copytree with dirs_exist_ok=True (Python 3.8+) merges directories
            if os.path.exists(build_dir):
                # Remove /target contents first to ensure clean state
                target_dir = '/target'
                if os.path.exists(target_dir):
                    for item in os.listdir(target_dir):
                        item_path = os.path.join(target_dir, item)
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                        else:
                            os.remove(item_path)

                # Copy all contents from build to target
                for item in os.listdir(build_dir):
                    src = os.path.join(build_dir, item)
                    dst = os.path.join(target_dir, item)
                    if os.path.isdir(src):
                        shutil.copytree(src, dst, dirs_exist_ok=True)
                    else:
                        shutil.copy2(src, dst)

                log_info("Site successfully copied to /target")
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
