import datetime
import os
import pathlib
import sys
from importlib import metadata

sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../jinja_autodoc"))

extensions = [
    "jinja_autodoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
source_suffix = {".rst": "restructuredtext"}
master_doc = "index"
project = "jinja-autodoc"
year = datetime.datetime.now().strftime("%Y")
copyright = f"{year}, Yaal Coop"
version = metadata.version(project)
release = metadata.version(project)
language = "en"
exclude_patterns = ["_build"]
pygments_style = "sphinx"
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

# -- Options for HTML output ----------------------------------------------

html_theme = "shibuya"
html_baseurl = "https://jinja-autodoc.readthedocs.io/"
html_theme_options = {
    "page_layout": "compact",
    "github_url": "https://github.com/sphinx-contrib/jinja-autodoc",
}
html_context = {
    "source_type": "github",
    "source_user": "sphinx-contrib",
    "source_repo": "jinja-autodoc",
    "source_version": "main",
    "source_docs_path": "/doc/",
}

htmlhelp_basename = "jinja-autodoc-doc"

jinja_template_path = str(pathlib.Path(__file__).parent.resolve())
