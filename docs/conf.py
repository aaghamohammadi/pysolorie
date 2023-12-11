project = "pysolorie"
copyright = "2023, Alireza Aghamohammadi"
author = "Alireza Aghamohammadi"


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
