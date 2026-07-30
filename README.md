# umd-lib-opendata

Source for the University of Maryland Libraries Open Data website,
<https://opendata.lib.umd.edu/>. The site is a [Hugo](https://gohugo.io/)
static site built with the [Hextra](https://github.com/imfing/hextra) theme.
It documents the APIs, services, and datasets that UMD Libraries makes openly
available, and ships runnable [Python code examples](static/code) that
demonstrate how to use them.

This README covers two audiences:

* **Site contributors** — building and serving the website locally
  (start with [Prerequisites](#prerequisites)).
* **Data and API users** — running the example scripts against UMD Libraries
  services (skip to [Python code examples](#python-code-examples)).

## Prerequisites

Building the site requires two command-line tools:

* [Hugo](https://gohugo.io/) — the **extended** edition (the Hextra theme
  requires it)
* [go-task](https://taskfile.dev/) — the task runner used for all build
  commands

On macOS with [Homebrew](https://brew.sh/):

```bash
brew install hugo go-task
```

Running the Python code examples additionally requires
[uv](https://docs.astral.sh/uv/) (see
[Python code examples](#python-code-examples)).

## Getting started

Clone the repository, then start the local development server:

```bash
task serve
```

This serves the site with drafts enabled at <http://localhost:1314/> and
rebuilds automatically as you edit. Open the URL in a browser:

```bash
open http://localhost:1314/
```

Other common tasks:

```bash
# Build the static site into public/
task build

# Remove build artifacts
task clean
```

For more options, see the [Hugo CLI docs](https://gohugo.io/commands/).

## Python code examples

The [`static/code/`](static/code) directory contains standalone Python
scripts that demonstrate how to query UMD Libraries services (OAI-PMH,
OpenSearch, the DSpace REST API, JSON-LD, and more).

Each script declares its own dependencies in a
[PEP 723](https://peps.python.org/pep-0723/) inline metadata block, so
[uv](https://docs.astral.sh/uv/) can run any of them with no environment
setup — locally or straight from the published site:

```bash
# Install uv (macOS with Homebrew; see the uv docs for other platforms)
brew install uv

# Run a local copy
uv run static/code/drum-oaipmh.py

# Or run directly from the published URL — no clone required
uv run https://opendata.lib.umd.edu/code/drum-oaipmh.py
```

uv reads the metadata block, installs the declared dependencies into a cached
ephemeral environment, and executes the script. The scripts remain plain
Python: they also run with `python script.py` inside any environment that
already has their dependencies installed.

To work on the repo itself, create the project environment — it is what the
test suite runs in:

```bash
# Create the environment and install dependencies
# (uv installs the pinned Python version automatically if needed)
uv sync

# Confirm the examples still work
task test-python
```

See [TEST_PYTHON_EXAMPLES.md](TEST_PYTHON_EXAMPLES.md) for details on testing
the code examples.

## Project structure

| Path | Contents |
| --- | --- |
| `content/` | Site content: `services/`, `apis/`, `datasets/`, `posts/` |
| `static/code/` | Downloadable Python API examples |
| `layouts/` | Custom templates and shortcodes overriding Hextra defaults |
| `hugo.yaml` | Hugo site configuration |
| `Taskfile.yaml` | Build, serve, and deploy tasks |

Content pages live under `content/` and use the `code` shortcode
(`layouts/_shortcodes/code.html`) to embed the example scripts.

## Contributing

Markdown content follows [markdownlint](https://github.com/DavidAnson/markdownlint)
conventions — notably asterisk-style lists (MD004), blank lines around lists
(MD032), and angle-bracketed bare URLs (MD034).

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE).
