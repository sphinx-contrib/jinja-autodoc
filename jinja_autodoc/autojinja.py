"""The autojinja directive.

:copyright: Copyright 2012 by Jaka Hudoklin
:license: BSD, see LICENSE for details.
"""

import os
import re

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList
from sphinx.util.docstrings import prepare_docstring
from sphinx.util.nodes import nested_parse_with_titles


def autojinja_directive(path, content):
    content = content.splitlines() if isinstance(content, str) else content
    yield ""
    yield f".. jinja:template:: {path}"
    yield ""
    for line in content:
        yield "   " + line
    yield ""


def parse_jinja_comment(path: str) -> str | None:
    """Parse jinja comment.

    :param path: Path to jinja template
    :returns: Jinja comment docstring
    """
    with open(path) as fd:
        contents = fd.read()

    res = re.match(r"\{\#-?(.+?)-?\#\}", contents, flags=re.MULTILINE | re.DOTALL)
    return res.group(1) if res else None


class AutojinjaDirective(Directive):
    has_content = True
    required_arguments = 1
    option_spec = {}

    def make_rst(self):
        env = self.state.document.settings.env
        path = self.arguments[0]
        docstring = parse_jinja_comment(
            os.path.join(env.config["jinja_template_path"], path)
        )
        docstring = prepare_docstring(docstring)
        if docstring is not None and env.config["jinja_template_path"]:
            yield from autojinja_directive(path, docstring)

        yield ""

    def run(self) -> list[nodes.Node]:
        node = nodes.section()
        node.document = self.state.document
        result = StringList()
        for line in self.make_rst():
            result.append(line, "<autojinja>")
        nested_parse_with_titles(self.state, result, node)
        return node.children
