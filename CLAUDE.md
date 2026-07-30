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

Python scripts in `static/code/` demonstrate API usage for various UMD Libraries services. Each script is a self-contained [uv script](https://docs.astral.sh/uv/guides/scripts/): it declares its Python version and dependencies in a [PEP 723](https://peps.python.org/pep-0723/) inline metadata block, so no virtual environment or install step is needed.

### Running the Examples

The project uses [uv](https://docs.astral.sh/uv/) for Python environment and
dependency management:

```bash
# uv resolves each script's inline metadata automatically
uv run static/code/drum-oaipmh.py

# The published copies work the same way
uv run https://opendata.lib.umd.edu/code/drum-oaipmh.py
```

Running an example needs no checkout and no install step. The project
environment declared in `pyproject.toml` is only for the test harness and
other repo-level tooling:

```bash
# Create the environment and install dependencies
# (uv installs the pinned Python version from .python-version if needed)
uv sync
```

Requires [uv](https://docs.astral.sh/uv/) (e.g. `brew install uv`).

### Testing Python Examples

Test all Python code examples to ensure they run correctly:

```bash
# Run all tests
task test-python

# Or run directly with options
uv run test_python_examples.py --verbose
uv run test_python_examples.py --file drum-api.py
```

See `TEST_PYTHON_EXAMPLES.md` for detailed documentation.

### Python Dependencies

Dependencies are declared in two places, and the two must agree:

* `pyproject.toml` (locked in `uv.lock`) - the project environment used by
  `task test-python` and other repo-level tooling
* each script's PEP 723 block - what a reader gets when they run one example
  on its own, with no checkout

Both use the same set, at the same version floors:

* `oaipmh>=3.2.0` - OAI-PMH protocol client for metadata harvesting (maintained
  fork of `pyoai`; same API and import path, and unlike `pyoai` it does not
  need a pinned legacy `setuptools` for `pkg_resources`)
* `rdflib>=7.6.0` - RDF and JSON-LD processing for semantic data
* `requests>=2.32.4` - HTTP client for API requests (the floor fixes
  CVE-2024-47081, a `.netrc` credential leak)
* `sru-queryer>=2.1.3` - SRU (Search/Retrieve via URL) protocol client

Scripts that import `requests` also declare `urllib3>=2.5.0`, matching the
constraint in `pyproject.toml` (CVE-2025-50181/50182). A standalone script has
no project constraints to inherit, so the floor has to be stated inline.

When bumping a floor for a security fix, change it in `pyproject.toml` **and**
in every script metadata block that names the package.

Scripts that use only the standard library declare `dependencies = []` to make that explicit. When adding a new script, declare every third-party import in its metadata block — `task test-python` runs each script via `uv run` and will fail if the block is incomplete.

## Architecture

### Content Structure

The Hugo site content is organized as follows:

* **`content/services/`** - Documentation for each service (DRUM, Digital Collections, Archive-It, etc.)
* **`content/apis/`** - API documentation and specifications (OAI-PMH, OpenSearch, DSpace REST API, JSON-LD, etc.)
* **`content/datasets/`** - Dataset descriptions
* **`content/posts/`** - Blog posts and updates
* **`static/code/`** - Downloadable Python code examples demonstrating API usage

### Hugo Configuration

* **`hugo.yaml`** - Main Hugo configuration file
* **`go.mod`** - Hugo modules configuration (imports Hextra theme v0.12.0)
* **Theme**: Uses Hextra theme as a Hugo module, not a git submodule

### Custom Components

* **`layouts/partials/`** - Custom partial templates overriding Hextra defaults
  * `navbar-title.html` - Custom navbar with UMD Libraries logo
  * `navbar.html` - Navigation bar customizations
  * `search.html` - Search functionality customizations

* **`layouts/_shortcodes/code.html`** - Custom shortcode for embedding Python code files directly into content with syntax highlighting and copy button

### Editing Design System Content and Brand

The brand shell is built on the UMD Libraries Drupal theme,
`umd-lib/umdlib-design-system-theme` (machine name `umdlib_umdds`), not on the
central `@universityofmaryland` web components. Its CSS is fetched at build time
in `layouts/partials/custom/head-end.html` and inlined as a fingerprinted,
SRI-hashed stylesheet, so nothing is vendored here and the visitor's browser
loads nothing from a third party.

Where things are edited:

* **Hero** - front-matter `hero.*` in `content/_index.md`; markup in
  `layouts/home.html`
* **Cards** - the overridden shortcode `layouts/_shortcodes/card.html`;
  authored as normal `{{< card >}}` in content
* **Brand color / type** - `--primary-*` (Hextra's accent) in
  `assets/css/custom.css`; everything else uses the Libraries theme's own
  tokens (`--maryland-red`, `--space-*`, the gray ramp)
* **Card-portal landings** (sidebar hidden, card grid as the only navigation) -
  `portal: true` front matter, handled by `layouts/list.html`
* **Which upstream ref we pin** - the single `$dsRef` line in `head-end.html`

Three things to know before editing:

1. **The token layer is a semantic inversion, not a palette swap.** Under
   `.dark-theme`, `--white` becomes `#000000`, `--black` becomes `#ffffff`,
   `--maryland-red` becomes the brand yellow, and the gray ramp reverses. So
   `var(--white)` is not "white". Surfaces that must keep a fixed appearance in
   both themes - the red university strip, the dark footer, the Give Now button
   - use literal values on purpose; a token there would invert underneath its own
   text. Hextra toggles `.dark`, and a small script in `head-end.html` mirrors
   that onto `.dark-theme`.

2. **Never put a `t-*` class on a wrapper around page content.** They are written
   `.t-x, .t-x *`, so a `t-` class on a content region restyles every element
   Goldmark emits inside it. Apply them to individual chrome elements only.

3. **`css/base.css` is deliberately not fetched.** It carries a Tailwind v3-era
   preflight and Hextra already compiles its own Tailwind v4 preflight; taking
   both puts two generations of reset in one cascade.

The font layer is subset at build time: `css/fonts.css` upstream is 739 KB of
base64 TTF/OTF across twelve faces, only three of which any rule we consume
names. `head-end.html` extracts those three and adds `font-display: swap`. If
upstream re-cuts or renames a face, the build fails with a named error rather
than silently falling back to a system font.

### Python Code Examples

The `static/code/` directory contains working Python examples for:

* OAI-PMH metadata harvesting (various services)
* OpenSearch API queries
* DSpace REST API usage
* JSON-LD structured data extraction
* Internet Archive searches
* Geoportal searches

Key example: `static/code/drum-harvest.py` - A comprehensive script for harvesting items from DRUM with resumable downloads.

### Harvest Directory

The `harvest/` directory contains harvested metadata and files from DRUM items. Each subdirectory is named by item UUID and contains:

* `{uuid}.json` - Item metadata
* Downloaded files/bitstreams for that item

## Docker Deployment

The `Dockerfile` uses a multi-stage build:
1. **Build stage**: Uses golang:1-trixie to install Hugo and task, then builds the static site
2. **Runtime stage**: Uses nginx:1.20 to serve the static files

Build arguments:

* `HUGO_BASEURL` - Base URL for the site (default: <https://opendata.lib.umd.edu/>)
* `HUGO_BUILDOPTS` - Additional Hugo build options (e.g., `--buildDrafts --buildFuture`)

## Documentation Standards

### Markdown Formatting

Follow markdownlint rules when creating or editing markdown files:

* **MD004**: Use asterisk-style lists (`*`) instead of dash-style (`-`)
  for unordered lists
* **MD032**: Add blank lines before and after lists
* **MD034**: Wrap bare URLs in angle brackets `<https://example.com>`

Example:

```markdown
Here is a list:

* First item
* Second item
  * Nested item
* Third item

Another paragraph here.
```

### Git Commit Standards

When creating commits, always include a "Co-authored-by" trailer to acknowledge
AI assistance:

```bash
git commit -m "feat: add new feature

Detailed description of the changes.

Co-authored-by: Claude <noreply@anthropic.com>"
```

**Important**: Every commit made by Claude Code must include this trailer.
This provides transparency about AI-assisted development and maintains proper
attribution in the repository history.

## Working with Content

### Creating New Service Documentation

Service documentation pages should include:

* Description of the service
* Available API endpoints with examples
* Code examples using the `code` shortcode
* Links to downloadable Python scripts in `/code/`

Example shortcode usage:

```go-html-template
{{< code filename="static/code/drum-api.py" name="drum-api.py" language="python" >}}
```

### API Documentation

API documentation in `content/apis/_index.md` provides overviews of:

* OAI-PMH
* OpenSearch
* DSpace REST API
* OpenAPI Specification
* SRU (Search/Retrieve via URL)
* JSON-LD

Individual service pages reference these API descriptions with anchor links.

## Important Notes

* The site runs on port 1314 locally (not the standard Hugo port 1313)
* Python code examples are meant to be runnable and demonstrate best
  practices for API usage
* The `harvest/temp/` directory is used for interrupted downloads and should
  be cleaned between runs
* All Python scripts in `static/code/` should use proper error handling and be well-documented
