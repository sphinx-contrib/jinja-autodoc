"""The autotemplate directive.

:copyright: Copyright 2012 by Jaka Hudoklin
:license: BSD, see LICENSE for details.
"""

import itertools
import os
import re
from typing import Optional

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList
from sphinx.util.docstrings import prepare_docstring
from sphinx.util.nodes import nested_parse_with_titles


def autotemplate_directive(path, content):
    content = content.splitlines() if isinstance(content, str) else content
    yield ""
    yield f".. jinja:template:: {path}"
    yield ""
    for line in content:
        yield "   " + line
    yield ""


def parse_template_paths(
    path: str, filename_filter: Optional[str] = None
) -> list[Optional[str]]:
    if not os.path.isdir(path):
        return [path]

    filepath_collections = [
        os.path.join(dirpath, filename)
        for dirpath, _, filenames in os.walk(path)
        for filename in filenames
        if (not filename_filter or re.match(filename_filter, filename))
    ]
    return list(itertools.chain(filepath_collections))


def parse_jinja_comment(path: str) -> Optional[str]:
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
        root_path = os.path.join(env.config["jinja_template_path"], path)
        template_paths = parse_template_paths(
            root_path, env.config["jinja_template_pattern"]
        )
        raw_docstrings = [parse_jinja_comment(path) for path in template_paths]
        docstrings = [
            prepare_docstring(raw_docstring)
            for raw_docstring in raw_docstrings
            if raw_docstring is not None
        ]
        if env.config["jinja_template_path"]:
            for docstring in docstrings:
                if docstring is not None:
                    yield from autotemplate_directive(path, docstring)
        yield ""

    def run(self) -> list[nodes.Node]:
        node = nodes.section()
        node.document = self.state.document
        result = StringList()
        for line in self.make_rst():
            result.append(line, "<autotemplate>")
        nested_parse_with_titles(self.state, result, node)
        return node.children
