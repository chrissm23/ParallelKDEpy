# -- Path Setup --------------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))
sys.path.append(os.path.abspath("_ext"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "ParallelKDEpy"
copyright = "2025, Christian Sustay Martinez"
author = "Christian Sustay Martinez"
release = "1.0.0-beta.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "auto_examples",
]

# Allow both .rst and .md
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

templates_path = ["_templates"]
exclude_patterns = []

# -- Autodoc configuration ---------------------------------------------------

autosummary_generate = True

autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "private-members": False,
    "inherited-members": True,
    "show-inheritance": True,
}

# -- Myst Parser configuration -----------------------------------------------

myst_enable_extensions = ["colon_fence", "deflist", "tasklist"]

# -- Notebook configuration -------------------------------------------------

nb_execution_mode = "auto"
nb_execution_timeout = 60

# -- Napoleon / NumPy configuration ---------------------------------------------

napoleon_numpy_docstring = True
napoleon_google_docstring = True
napoleon_use_ivar = True
napoleon_attr_annotations = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_logo = "_static/logo.png"
