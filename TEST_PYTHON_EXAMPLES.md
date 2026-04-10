# Testing Python Code Examples

This repository includes a comprehensive test script for validating all Python code examples in `static/code/`.

## Quick Start

```bash
# Run all tests
python test_python_examples.py

# Run all tests with verbose output
python test_python_examples.py --verbose

# Test a specific file
python test_python_examples.py --file drum-api.py

# Using task (recommended)
task test-python
```

## Test Script Features

The `test_python_examples.py` script:

- **Runs all Python examples** in `static/code/` (except `drum-harvest.py`)
- **Validates execution** - ensures scripts run without errors
- **Checks output** - verifies scripts produce reasonable output
- **Reports results** - provides clear pass/fail summary with detailed error information
- **Configurable timeout** - prevents hanging on slow scripts (default: 30 seconds)
- **Verbose mode** - shows detailed output from each test

## What Gets Tested

All Python files in `static/code/` are tested except:
- `drum-harvest.py` - Excluded because it harvests large amounts of data and is too slow for quick testing

## Understanding Results

### Exit Codes
- **0** - All tests passed
- **1** - One or more tests failed

### Test Status
- **✅ PASSED** - Script ran successfully and produced output
- **❌ FAILED** - Script exited with error or produced no output
- **⊘ SKIPPED** - Script excluded from testing

## Command-Line Options

```bash
python test_python_examples.py [OPTIONS]

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
python test_python_examples.py
```

### Run with detailed output
```bash
python test_python_examples.py --verbose
```

### Test a specific file
```bash
python test_python_examples.py --file drum-api.py
```

### Increase timeout for slow tests
```bash
python test_python_examples.py --timeout 60
```

## Common Failure Reasons

1. **Network errors** - External APIs might be down or URLs changed
2. **Missing dependencies** - Ensure `requirements.txt` is installed
3. **API changes** - External services may have updated their APIs
4. **Rate limiting** - Too many requests to external services

## Continuous Integration

This test script can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Setup Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.12'

- name: Install dependencies
  run: pip install -r requirements.txt

- name: Test Python examples
  run: python test_python_examples.py
```

## Troubleshooting

### Script fails but works when run manually
- Check if the script requires environment variables
- Ensure you're running from the correct directory
- Verify network connectivity to external APIs

### All scripts timeout
- Increase timeout with `--timeout` option
- Check network connectivity
- Some APIs may be temporarily slow

### ImportError or ModuleNotFoundError
- Activate the virtual environment: `source .venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

## Adding New Test Exclusions

To skip additional files, edit the `SKIP_FILES` set in `test_python_examples.py`:

```python
SKIP_FILES = {
    'drum-harvest.py',  # Too slow for testing
    'your-script.py',   # Add your exclusions here
}
```
