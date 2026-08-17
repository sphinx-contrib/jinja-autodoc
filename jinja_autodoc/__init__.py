import importlib
import os

from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.util.typing import ExtensionMetadata

from .autotemplate import AutojinjaDirective
from .domain import JinjaDomain


def resolve_template_path(app: Sphinx, config: Config) -> None:
    """Make the template path absolute, relatively to the configuration directory."""
    if not config.jinja_template_path:
        return

    config.jinja_template_path = os.path.abspath(
        os.path.join(app.confdir, config.jinja_template_path)
    )


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_domain(JinjaDomain)

    app.add_directive("autotemplate", AutojinjaDirective)
    app.add_config_value("jinja_template_path", "", "env")
    app.add_config_value("jinja_template_pattern", "", "env")
    app.connect("config-inited", resolve_template_path)

    return {
        "version": importlib.metadata.version("jinja-autodoc"),
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
