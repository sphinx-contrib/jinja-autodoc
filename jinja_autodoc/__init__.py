import importlib

from sphinx.application import Sphinx
from sphinx.util.typing import ExtensionMetadata

from .autotemplate import AutojinjaDirective
from .domain import JinjaDomain


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_domain(JinjaDomain)

    app.add_directive("autotemplate", AutojinjaDirective)
    app.add_config_value("jinja_template_path", "", "")
    app.add_config_value("jinja_template_pattern", "", "")

    return {
        "version": importlib.metadata.version("jinja-autodoc"),
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
