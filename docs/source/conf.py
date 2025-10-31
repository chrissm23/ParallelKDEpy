# -- Path Setup --------------------------------------------------------------

import os
import sys
import subprocess

# Defaults
release = version = "dev"

# Get version from SMV
smv_name = os.environ.get("SPHINX_MULTIVERSION_NAME")
if smv_name:
    if smv_name.startswith("v") and "-" not in smv_name:
        parsed = smv_name.lstrip("v")
        release = parsed
        version = ".".join(parsed.split(".")[:2])
    else:
        release = version = "dev"

# Fallback when not using SMV
if not smv_name:
    try:
        tag = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"], text=True
        ).strip()
        if tag.startswith("v") and "-" not in tag:
            parsed = tag.lstrip("v")
            release = parsed
            version = ".".join(parsed.split(".")[:2])
    except Exception:
        pass

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
    "sphinx_multiversion",
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

# -- sphinx-multiversion configuration ---------------------------------------
smv_branch_whitelist = r"^(dev)$"
smv_tag_whitelist = r"^v\d+\.\d+\.\d+$"
smv_released_pattern = r"^tags/v\d+\.\d+\.\d+$"
smv_outputdir_format = "{ref.name}"
smv_remote_whitelist = r"^origin$"
