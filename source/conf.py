# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Open Data'
copyright = '2024, University of Maryland Libraries'
author = 'University of Maryland Libraries'

# The full version, including alpha/beta/rc tags
release = '1.0.13'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_sitemap',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# Suppress empty modindex.html
html_domain_indices = False

# Suppress empty genindex.html
html_use_index = False

html_extra_path = [
    'robots.txt',
    'favicon.ico',
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'css/custom.css',
]

html_logo = 'assets/img/liblogo.svg'

language = 'en'

highlight_language = 'none'

html_theme_options = {
    'anchor': '#3E4349',
    'footer_text': '#3E4349',
}

html_sidebars = {
   '**': [
      'about.html',
      'navigation.html',
      'searchbox.html',
      'external_links.html',
    ],
}

# -- Options for sitemap extension -------------------------------------------

html_baseurl = 'https://opendata.lib.umd.edu/'

sitemap_url_scheme = "{link}"
