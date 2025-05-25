# Configuration file for Sphinx
import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

project = "ParallelKDEpy"
autohr = "Christian Sustay"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # for Google/NumPy docstrings
]
templates_path = ["_templates"]
exclude_patterns = []

# Options for HTML output
html_theme = "alabaster"  # or "sphinx_rtd_theme" if installed
