from sphinx.application import Sphinx
from sphinx.util.typing import ExtensionMetadata

from .autojinja import AutojinjaDirective
from .domain import JinjaDomain


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_domain(JinjaDomain)

    app.add_directive("autojinja", AutojinjaDirective)
    app.add_config_value("jinja_template_path", "", "")
    app.add_config_value("jinja_template_pattern", "", "")

    return {}
