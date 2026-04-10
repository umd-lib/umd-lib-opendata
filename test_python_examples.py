#!/usr/bin/env python3
"""
Test runner for Python code examples in static/code/

This script runs each Python example file (except drum-harvest.py) and validates:
- The script runs without errors
- The script produces output
- The script exits with code 0

Usage:
    python test_python_examples.py
    python test_python_examples.py --verbose
    python test_python_examples.py --file drum-api.py
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


# Files to skip (e.g., too slow, interactive, or require special setup)
SKIP_FILES = {
    'drum-harvest.py',  # Harvests large amounts of data, not suitable for quick testing
}

# Timeout in seconds for each script
TIMEOUT_SECONDS = 30


class TestResult:
    """Container for test results"""
    def __init__(self, filename: str, success: bool, output: str, error: str,
                 return_code: int, skipped: bool = False, skip_reason: str = ""):
        self.filename = filename
        self.success = success
        self.output = output
        self.error = error
        self.return_code = return_code
        self.skipped = skipped
        self.skip_reason = skip_reason


def run_python_file(filepath: Path, timeout: int = TIMEOUT_SECONDS) -> TestResult:
    """
    Run a single Python file and capture its output

    Args:
        filepath: Path to the Python file to run
        timeout: Maximum time to wait for the script (seconds)

    Returns:
        TestResult object with execution details
    """
    filename = filepath.name

    try:
        # Run the Python file
        result = subprocess.run(
            [sys.executable, str(filepath)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=filepath.parent
        )

        success = result.returncode == 0 and len(result.stdout) > 0

        # Check for common error indicators in output
        if success and any(indicator in result.stderr.lower() for indicator in
                          ['error', 'exception', 'traceback']):
            success = False

        return TestResult(
            filename=filename,
            success=success,
            output=result.stdout,
            error=result.stderr,
            return_code=result.returncode
        )

    except subprocess.TimeoutExpired:
        return TestResult(
            filename=filename,
            success=False,
            output="",
            error=f"Script exceeded timeout of {timeout} seconds",
            return_code=-1
        )
    except Exception as e:
        return TestResult(
            filename=filename,
            success=False,
            output="",
            error=f"Exception running script: {str(e)}",
            return_code=-1
        )


def find_python_files(code_dir: Path, skip_files: set) -> List[Path]:
    """
    Find all Python files in the code directory

    Args:
        code_dir: Directory containing Python files
        skip_files: Set of filenames to skip

    Returns:
        List of Path objects for Python files to test
    """
    all_files = sorted(code_dir.glob("*.py"))
    return [f for f in all_files if f.name not in skip_files]


def print_result_summary(results: List[TestResult], verbose: bool = False) -> None:
    """
    Print a summary of test results

    Args:
        results: List of TestResult objects
        verbose: Whether to print detailed output
    """
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)

    passed = sum(1 for r in results if r.success and not r.skipped)
    failed = sum(1 for r in results if not r.success and not r.skipped)
    skipped = sum(1 for r in results if r.skipped)
    total = len(results)

    print(f"\nTotal: {total} | Passed: {passed} | Failed: {failed} | Skipped: {skipped}")

    # Print failed tests
    if failed > 0:
        print("\n" + "-" * 80)
        print("FAILED TESTS:")
        print("-" * 80)
        for result in results:
            if not result.success and not result.skipped:
                print(f"\n❌ {result.filename}")
                print(f"   Return code: {result.return_code}")
                if result.error:
                    print(f"   Error output:")
                    for line in result.error.split('\n')[:10]:  # First 10 lines
                        print(f"      {line}")
                if verbose and result.output:
                    print(f"   Standard output:")
                    for line in result.output.split('\n')[:10]:  # First 10 lines
                        print(f"      {line}")

    # Print passed tests
    if passed > 0:
        print("\n" + "-" * 80)
        print("PASSED TESTS:")
        print("-" * 80)
        for result in results:
            if result.success and not result.skipped:
                output_lines = result.output.count('\n')
                print(f"✅ {result.filename} ({output_lines} lines of output)")
                if verbose and result.output:
                    print(f"   Output preview:")
                    for line in result.output.split('\n')[:5]:  # First 5 lines
                        print(f"      {line}")

    # Print skipped tests
    if skipped > 0:
        print("\n" + "-" * 80)
        print("SKIPPED TESTS:")
        print("-" * 80)
        for result in results:
            if result.skipped:
                print(f"⊘ {result.filename} - {result.skip_reason}")

    print("\n" + "=" * 80)


def main():
    """Main test execution function"""
    parser = argparse.ArgumentParser(
        description='Test Python code examples in static/code/',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output from each test'
    )
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='Test only a specific file (e.g., drum-api.py)'
    )
    parser.add_argument(
        '--timeout', '-t',
        type=int,
        default=TIMEOUT_SECONDS,
        help=f'Timeout in seconds for each script (default: {TIMEOUT_SECONDS})'
    )
    parser.add_argument(
        '--code-dir',
        type=Path,
        default=Path(__file__).parent / 'static' / 'code',
        help='Path to code directory (default: static/code/)'
    )

    args = parser.parse_args()

    # Validate code directory
    if not args.code_dir.exists():
        print(f"Error: Code directory not found: {args.code_dir}", file=sys.stderr)
        sys.exit(1)

    # Find Python files to test
    if args.file:
        # Test specific file
        filepath = args.code_dir / args.file
        if not filepath.exists():
            print(f"Error: File not found: {filepath}", file=sys.stderr)
            sys.exit(1)
        python_files = [filepath]
    else:
        # Test all files except skipped ones
        python_files = find_python_files(args.code_dir, SKIP_FILES)

    if not python_files:
        print("No Python files found to test", file=sys.stderr)
        sys.exit(1)

    print(f"Testing {len(python_files)} Python files from {args.code_dir}")
    print(f"Timeout: {args.timeout} seconds per script")
    if SKIP_FILES and not args.file:
        print(f"Skipping: {', '.join(sorted(SKIP_FILES))}")
    print()

    # Run tests
    results = []
    for i, filepath in enumerate(python_files, 1):
        print(f"[{i}/{len(python_files)}] Testing {filepath.name}...", end=' ', flush=True)

        if filepath.name in SKIP_FILES:
            result = TestResult(
                filename=filepath.name,
                success=False,
                output="",
                error="",
                return_code=0,
                skipped=True,
                skip_reason="Excluded from testing"
            )
        else:
            result = run_python_file(filepath, timeout=args.timeout)

        results.append(result)

        if result.skipped:
            print("SKIPPED")
        elif result.success:
            print("PASSED")
        else:
            print("FAILED")

    # Print summary
    print_result_summary(results, verbose=args.verbose)

    # Exit with appropriate code
    failed_count = sum(1 for r in results if not r.success and not r.skipped)
    sys.exit(0 if failed_count == 0 else 1)


if __name__ == '__main__':
    main()
