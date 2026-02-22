# umd-lib-opendata

University of Maryland Libraries Open Data Website, built using the
[Hugo](https://gohugo.io/) static site generator.

## Building

Install go-task.

```bash
# Intall using Homebrew
brew install task

# Install using golang
go install github.com/go-task/task/v3/cmd/task@latest
```

Build and serve the website using hugo:

``` bash
task serve
open http://localhost:1314/
```

For more information see [Hugo CLI docs](https://gohugo.io/commands/).

## Python Environment

Set up a Python environment to run the [code examples](static/code), using pyenv
and venv.

```bash
# Setup the Python version
pyenv install --skip-existing $(cat .python-version)

# Setup the virtual environment
python -m venv .venv
source .venv/bin/activate

# Install the requirements
pip install -r requirements.txt
```
