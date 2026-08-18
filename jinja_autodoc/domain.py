"""The jinja domain for documenting jinja templates.

:copyright: Copyright 2012 by Jaka Hudoklin
:license: BSD, see LICENSE for details.
"""

import os
import re
from collections.abc import Set
from typing import Any

from docutils import nodes
from sphinx import addnodes
from sphinx.builders import Builder
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain
from sphinx.domains import Index
from sphinx.domains import ObjType
from sphinx.environment import BuildEnvironment
from sphinx.roles import XRefRole
from sphinx.util.docfields import TypedField
from sphinx.util.nodes import make_refnode


def jinja_resource_anchor(method, path):
    path = re.sub(r"[<>:/]", "-", path)
    return method.lower() + "-" + path


class JinjaResource(ObjectDescription):
    doc_field_types = [
        TypedField(
            "parameter",
            label="Parameters",
            names=("param", "parameter", "arg", "argument"),
            typenames=("paramtype", "type"),
        )
    ]

    method = "template"

    def handle_signature(self, sig, signode):
        method = self.method.upper() + " "
        signode += addnodes.desc_name(method, method)
        signode += addnodes.desc_name(sig, sig)

        fullname = "Template" + " " + sig
        signode["method"] = self.method
        signode["path"] = sig
        signode["fullname"] = fullname
        return (fullname, self.method, sig)

    def add_target_and_index(self, name_cls, sig, signode):
        signode["ids"].append(jinja_resource_anchor(*name_cls[1:]))
        self.env.domaindata["jinja"][self.method][sig] = (self.env.docname, "", None)


class JinjaXRefRole(XRefRole):
    """Cross-reference role targetting the path of a documented template."""

    def process_link(
        self,
        env: BuildEnvironment,
        refnode: nodes.Element,
        has_explicit_title: bool,
        title: str,
        target: str,
    ) -> tuple[str, str]:
        """Let a leading ``~`` shorten the title down to the template file name."""
        if not has_explicit_title and title.startswith("~"):
            title = title.removeprefix("~").rpartition("/")[2]
            target = target.removeprefix("~")
        return title, target


class JinjaIndex(Index):
    name = "jinjatemplates"
    localname = "templates"
    shortname = "templates"

    def grouping_prefix(self, path):
        return os.path.split(path)[0]

    def generate(self, docnames=None):
        content = {}
        items = (
            (method, path, info)
            for method, routes in self.domain.routes.items()
            for path, info in routes.items()
        )
        items = sorted(items, key=lambda item: item[1])
        for method, path, info in items:
            entries = content.setdefault(self.grouping_prefix(path), [])
            entries.append(
                [
                    path,
                    0,
                    info[0],
                    jinja_resource_anchor(method, path),
                    "",
                    "",
                    info[1],
                ]
            )
        content = list(content.items())
        content.sort(key=lambda k: k[0])
        return (content, True)


class JinjaDomain(Domain):
    """Jinja domain."""

    name = "jinja"
    label = "jinja"

    object_types = {"template": ObjType("template", "template")}
    directives = {"template": JinjaResource}
    roles = {"template": JinjaXRefRole()}
    initial_data = {"template": {}}  # path: (docname, synopsis, source)
    indices = [JinjaIndex]

    @property
    def routes(self):
        return dict((key, self.data[key]) for key in self.object_types)

    def clear_doc(self, docname: str) -> None:
        for path, info in list(self.data["template"].items()):
            if info[0] == docname:
                del self.data["template"][path]

    def get_objects(self):
        for method, routes in self.routes.items():
            for path, info in list(routes.items()):
                anchor = jinja_resource_anchor(method, path)
                yield (path, path, method, info[0], anchor, 1)

    def merge_domaindata(self, docnames: Set[str], otherdata: dict[str, Any]) -> None:
        self.data["template"].update(**otherdata["template"])

    def resolve_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        typ: str,
        target: str,
        node: addnodes.pending_xref,
        contnode: nodes.Element,
    ) -> nodes.reference | None:
        if target not in self.data["template"]:
            return None

        docname = self.data["template"][target][0]
        anchor = jinja_resource_anchor(typ, target)
        return make_refnode(builder, fromdocname, docname, anchor, contnode, target)

    def resolve_any_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        target: str,
        node: addnodes.pending_xref,
        contnode: nodes.Element,
    ) -> list[tuple[str, nodes.reference]]:
        refnode = self.resolve_xref(
            env, fromdocname, builder, "template", target, node, contnode
        )
        return [] if refnode is None else [("jinja:template", refnode)]
