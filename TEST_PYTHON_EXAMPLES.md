# Testing Python Code Examples

This repository includes a comprehensive test script for validating all Python code examples in `static/code/`.

## Quick Start

```bash
# Run all tests
uv run python test_python_examples.py

# Run all tests with verbose output
uv run python test_python_examples.py --verbose

# Test a specific file
uv run python test_python_examples.py --file drum-api.py

# Using task (recommended)
task test-python
```

## Test Script Features

The `test_python_examples.py` script:

* **Runs all Python examples** in `static/code/` (except `drum-harvest.py`)
* **Validates execution** - ensures scripts run without errors
* **Checks output** - verifies scripts produce reasonable output
* **Reports results** - provides clear pass/fail summary with detailed error information
* **Configurable timeout** - prevents hanging on slow scripts (default: 30 seconds)
* **Verbose mode** - shows detailed output from each test

## What Gets Tested

All Python files in `static/code/` are tested except:

* `drum-harvest.py` - Excluded because it harvests large amounts of data and is too slow for quick testing

## Understanding Results

### Exit Codes

* **0** - All tests passed
* **1** - One or more tests failed

### Test Status

* **✅ PASSED** - Script ran successfully and produced output
* **❌ FAILED** - Script exited with error or produced no output
* **⊘ SKIPPED** - Script excluded from testing

## Command-Line Options

```bash
uv run python test_python_examples.py [OPTIONS]

Options:
  -v, --verbose          Show detailed output from each test
  -f FILE, --file FILE   Test only a specific file (e.g., drum-api.py)
  -t SECONDS, --timeout SECONDS
                         Timeout in seconds for each script (default: 30)
  --code-dir PATH        Path to code directory (default: static/code/)
  -h, --help            Show help message
```

## Examples

### Run all tests with summary
```bash
uv run python test_python_examples.py
```

### Run with detailed output
```bash
uv run python test_python_examples.py --verbose
```

### Test a specific file
```bash
uv run python test_python_examples.py --file drum-api.py
```

### Increase timeout for slow tests
```bash
uv run python test_python_examples.py --timeout 60
```

## Common Failure Reasons

1. **Network errors** - External APIs might be down or URLs changed
1. **Missing dependencies** - Ensure dependencies are installed with `uv sync`
1. **API changes** - External services may have updated their APIs
1. **Rate limiting** - Too many requests to external services

## Continuous Integration

This test script can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Install uv
  uses: astral-sh/setup-uv@v5

- name: Install dependencies
  run: uv sync

- name: Test Python examples
  run: uv run python test_python_examples.py
```

## Troubleshooting

### Script fails but works when run manually

* Check if the script requires environment variables
* Ensure you're running from the correct directory
* Verify network connectivity to external APIs

### All scripts timeout

* Increase timeout with `--timeout` option
* Check network connectivity
* Some APIs may be temporarily slow

### ImportError or ModuleNotFoundError

* Run the script through `uv run`, which uses the project environment automatically
* Install dependencies: `uv sync`

## Adding New Test Exclusions

To skip additional files, edit the `SKIP_FILES` set in `test_python_examples.py`:

```python
SKIP_FILES = {
    'drum-harvest.py',  # Too slow for testing
    'your-script.py',   # Add your exclusions here
}
```
