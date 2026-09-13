"""Sphinx configuration of the WhalePy documentation."""

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "WhalePy"
author = "Kaja Dudek, Natalia Luberda, Wojciech Książek"
copyright = "2026, the whalepy authors"
release = "1.0.0"
version = release

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.mathjax",
]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# autodoc
autodoc_member_order = "bysource"
autodoc_inherit_docstrings = False
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"

# napoleon (Google-style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_custom_sections = ["Links"]

# HTML output
html_theme = "sphinx_rtd_theme"
html_title = f"WhalePy {release}"
html_static_path = ["_static"]
html_theme_options = {
    "navigation_depth": 2,
}
