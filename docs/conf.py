import os

try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata

project = "pysolorie"
copyright = "2023, Alireza Aghamohammadi"
author = "Alireza Aghamohammadi"
PACKAGE_VERSION = metadata.version("pysolorie")
version = PACKAGE_VERSION
release = PACKAGE_VERSION

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autodoc.typehints",
    "sphinx.ext.viewcode",
]


pygments_style = "sphinx"

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
autoclass_content = "both"


html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
