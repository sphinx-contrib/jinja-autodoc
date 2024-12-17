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


def jinja_directive(path, content):
    content = content.splitlines() if isinstance(content, str) else content
    yield ""
    yield f".. jinja:template:: {path}"
    yield ""
    for line in content:
        yield "   " + line
    yield ""


def parse_jinja_comment(path):
    """Parse jinja comment.

    :param path: Path to jinja template
    :type path: str
    :returns: Jinja comment docstring
    :rtype: str
    """
    f = open(path)
    contents = f.read()
    res = re.match(r"\{\#-?(.+?)-?\#\}", contents, flags=re.MULTILINE | re.DOTALL)
    if res:
        return res.group(1)

    return None


class AutojinjaDirective(Directive):
    has_content = True
    required_arguments = 1
    option_spec = {}

    @property
    def endpoints(self):
        try:
            endpoints = re.split(r"\s*,\s*", self.options["endpoints"])
        except KeyError:
            # means 'endpoints' option was missing
            return None
        return frozenset(endpoints)

    @property
    def undoc_endpoints(self):
        try:
            endpoints = re.split(r"\s*,\s*", self.options["undoc-endpoints"])
        except KeyError:
            return frozenset()
        return frozenset(endpoints)

    def make_rst(self):
        env = self.state.document.settings.env
        path = self.arguments[0]
        docstring = parse_jinja_comment(
            os.path.join(env.config["jinja_template_path"], path)
        )
        docstring = prepare_docstring(docstring)
        if docstring is not None and env.config["jinja_template_path"]:
            yield from jinja_directive(path, docstring)

        yield ""

    def run(self) -> list[nodes.Node]:
        node = nodes.section()
        node.document = self.state.document
        result = StringList()
        for line in self.make_rst():
            result.append(line, "<autojinja>")
        nested_parse_with_titles(self.state, result, node)
        return node.children
