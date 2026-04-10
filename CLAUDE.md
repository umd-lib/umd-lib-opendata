# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the University of Maryland Libraries Open Data Website, a Hugo static site that provides documentation, APIs, services, and datasets available from UMD Libraries. The site uses the [Hextra](https://github.com/imfing/hextra) Hugo theme and includes Python code examples demonstrating API usage.

## Build System

The project uses [go-task](https://taskfile.dev/) for build automation. All commands should be run via `task`.

### Common Commands

```bash
# Build the site
task build

# Serve locally with drafts (runs on port 1314)
task serve

# Clean build artifacts
task clean

# Build and push Docker image (requires appropriate permissions)
task deploy
```

### Direct Hugo Commands

If needed, Hugo can be invoked directly:

```bash
# Build the site
hugo build

# Serve with custom options
hugo server --logLevel debug --disableFastRender --port 1314 --buildDrafts --buildFuture
```

## Python Environment

Python scripts in `static/code/` demonstrate API usage for various UMD Libraries services. These scripts require Python 3.12+ and specific dependencies.

### Setup Python Environment

```bash
# Install Python version from .python-version
pyenv install --skip-existing $(cat .python-version)

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Testing Python Examples

Test all Python code examples to ensure they run correctly:

```bash
# Run all tests
task test-python

# Or run directly with options
python test_python_examples.py --verbose
python test_python_examples.py --file drum-api.py
```

See `TEST_PYTHON_EXAMPLES.md` for detailed documentation.

### Python Dependencies

The `requirements.txt` includes:
- `pyoai==2.5.0` - OAI-PMH protocol client for metadata harvesting
- `rdflib==7.6.0` - RDF and JSON-LD processing for semantic data
- `requests==2.32.3` - HTTP client for API requests
- `sru-queryer==2.1.3` - SRU (Search/Retrieve via URL) protocol client

## Architecture

### Content Structure

The Hugo site content is organized as follows:

- **`content/services/`** - Documentation for each service (DRUM, Digital Collections, Archive-It, etc.)
- **`content/apis/`** - API documentation and specifications (OAI-PMH, OpenSearch, DSpace REST API, JSON-LD, etc.)
- **`content/datasets/`** - Dataset descriptions
- **`content/posts/`** - Blog posts and updates
- **`static/code/`** - Downloadable Python code examples demonstrating API usage

### Hugo Configuration

- **`hugo.yaml`** - Main Hugo configuration file
- **`go.mod`** - Hugo modules configuration (imports Hextra theme v0.12.0)
- **Theme**: Uses Hextra theme as a Hugo module, not a git submodule

### Custom Components

- **`layouts/partials/`** - Custom partial templates overriding Hextra defaults
  - `navbar-title.html` - Custom navbar with UMD Libraries logo
  - `navbar.html` - Navigation bar customizations
  - `search.html` - Search functionality customizations

- **`layouts/_shortcodes/code.html`** - Custom shortcode for embedding Python code files directly into content with syntax highlighting and copy button

### Python Code Examples

The `static/code/` directory contains working Python examples for:
- OAI-PMH metadata harvesting (various services)
- OpenSearch API queries
- DSpace REST API usage
- JSON-LD structured data extraction
- Internet Archive searches
- Geoportal searches

Key example: `static/code/drum-harvest.py` - A comprehensive script for harvesting items from DRUM with resumable downloads.

### Harvest Directory

The `harvest/` directory contains harvested metadata and files from DRUM items. Each subdirectory is named by item UUID and contains:
- `{uuid}.json` - Item metadata
- Downloaded files/bitstreams for that item

## Docker Deployment

The `Dockerfile` uses a multi-stage build:
1. **Build stage**: Uses golang:1-trixie to install Hugo and task, then builds the static site
2. **Runtime stage**: Uses nginx:1.20 to serve the static files

Build arguments:
- `HUGO_BASEURL` - Base URL for the site (default: https://opendata.lib.umd.edu/)
- `HUGO_BUILDOPTS` - Additional Hugo build options (e.g., `--buildDrafts --buildFuture`)

## Working with Content

### Creating New Service Documentation

Service documentation pages should include:
- Description of the service
- Available API endpoints with examples
- Code examples using the `code` shortcode
- Links to downloadable Python scripts in `/code/`

Example shortcode usage:
```
{{< code filename="static/code/drum-api.py" name="drum-api.py" language="python" >}}
```

### API Documentation

API documentation in `content/apis/_index.md` provides overviews of:
- OAI-PMH
- OpenSearch
- DSpace REST API
- OpenAPI Specification
- SRU (Search/Retrieve via URL)
- JSON-LD

Individual service pages reference these API descriptions with anchor links.

## Important Notes

- The site runs on port 1314 locally (not the standard Hugo port 1313)
- Python code examples are meant to be runnable and demonstrate best practices for API usage
- The `harvest/temp/` directory is used for interrupted downloads and should be cleaned between runs
- All Python scripts in `static/code/` should use proper error handling and be well-documented
