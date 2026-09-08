---
publishDate: '2026-09-08T00:00:02-04:00'
draft: false
title: 'Running Code Examples Directly from the Site'
type: blog
---

The Python code examples on this site are now self-contained. Each script
declares its own Python version and dependencies inline, using
[PEP 723](https://peps.python.org/pep-0723/) metadata, so you can run any example
directly from this site with a single command, without a checkout or a setup
step:

```bash
uv run https://opendata.lib.umd.edu/code/drum-oaipmh.py
```

This example harvests metadata from [DRUM](/services/drum), UMD's institutional
repository. It uses [uv](https://docs.astral.sh/uv/), which reads each script's
declared dependencies and runs it in a temporary environment. If you do not have
uv installed, run `brew install uv` or see the [uv installation
guide](https://docs.astral.sh/uv/getting-started/installation/).

Each [service](/services) page embeds its own runnable examples, covering
OAI-PMH, OpenSearch, the DSpace REST API, SRU, and JSON-LD.
