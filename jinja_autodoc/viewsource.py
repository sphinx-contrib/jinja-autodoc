"""Source pages for the documented jinja templates.

Each documented template gets a page displaying its highlighted source, and a
``[source]`` link in its documentation, the way :mod:`sphinx.ext.viewcode` does
for python modules.
"""

import html
import os
import posixpath
from collections.abc import Iterator
from typing import TYPE_CHECKING
from typing import Any
from typing import cast

from docutils import nodes
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.locale import _
from sphinx.locale import __
from sphinx.util.display import status_iterator
from sphinx.util.nodes import make_refnode

from .domain import jinja_resource_anchor

if TYPE_CHECKING:
    from sphinx.builders.html import StandaloneHTMLBuilder

OUTPUT_DIRNAME = "_jinja"


class jinja_source_anchor(nodes.Element):
    """Placeholder for a ``[source]`` link, resolved once the builder is known."""


def is_supported_builder(builder: Builder) -> bool:
    """Tell whether a builder can link to the generated source pages.

    ``singlehtml`` cannot link to a page that is not part of its single
    document, and ``epub`` does not list such pages in its manifest.
    """
    return (
        builder.format == "html"
        and builder.name != "singlehtml"
        and not builder.name.startswith("epub")
    )


def source_page_name(sig: str) -> str:
    """Return the name of the page displaying the source of a template."""
    return posixpath.join(OUTPUT_DIRNAME, *sig.split(os.sep))


def template_source_path(root: str, sig: str) -> str | None:
    """Locate the template file documented under the *sig* signature.

    Signatures escaping the template root, by being absolute or by walking the
    tree up, are ignored: source pages get published, and must not expose
    arbitrary files of the machine that built the documentation.
    """
    if not root:
        return None

    path = os.path.normpath(os.path.join(root, sig))
    if not path.startswith(os.path.join(root, "")):
        return None

    return path if os.path.isfile(path) else None


def doctree_read(app: Sphinx, doctree: nodes.Node) -> None:
    """Remember where the documented templates come from, and mark their signature."""
    templates = app.env.domaindata["jinja"]["template"]
    for objnode in doctree.findall(addnodes.desc):
        if objnode.get("domain") != "jinja":
            continue

        for signode in objnode.findall(addnodes.desc_signature):
            sig = signode.get("path")
            # Signatures excluded from the index have no domain data entry.
            if sig not in templates:
                continue

            source = template_source_path(app.config.jinja_template_path, sig)
            if source is None:
                continue

            docname, synopsis, _previous = templates[sig]
            templates[sig] = (docname, synopsis, source)
            app.env.note_dependency(source)
            signode += jinja_source_anchor()


def doctree_resolved(app: Sphinx, doctree: nodes.Node, docname: str) -> None:
    """Turn the marked signatures into links, or drop them for other builders."""
    supported = is_supported_builder(app.builder)
    for node in list(doctree.findall(jinja_source_anchor)):
        if not supported:
            node.parent.remove(node)
            continue

        sig = node.parent["path"]
        anchor = nodes.inline("", _("[source]"), classes=["viewcode-link"])
        node.replace_self(
            make_refnode(app.builder, docname, source_page_name(sig), None, anchor)
        )


def collect_pages(app: Sphinx) -> Iterator[tuple[str, dict[str, Any], str]]:
    """Generate a page displaying the source of each documented template."""
    if not is_supported_builder(app.builder):
        return

    templates = app.env.domaindata["jinja"]["template"]
    documented = sorted(item for item in templates.items() if item[1][2])
    # Only HTML builders reach this point, and they carry a highlighter.
    highlighter = cast("StandaloneHTMLBuilder", app.builder).highlighter
    lexer = app.config.jinja_template_lexer

    for sig, (docname, _synopsis, source) in status_iterator(
        documented,
        __("highlighting jinja templates... "),
        "blue",
        len(documented),
        app.verbosity,
        lambda item: item[0],
    ):
        with open(source, encoding="utf-8") as fd:
            code = fd.read()

        # The lexer is configured once for every template, so a template it does
        # not fit should not warn about it: highlight in relaxed mode instead.
        highlighted = highlighter.highlight_block(code, lexer, force=True)
        pagename = source_page_name(sig)
        backlink = (
            app.builder.get_relative_uri(pagename, docname)
            + "#"
            + jinja_resource_anchor("template", sig)
        )
        context = {
            "parents": [],
            "title": sig,
            "body": (
                f"<h1>{html.escape(sig)}</h1>"
                f'<a class="viewcode-back" href="{backlink}">{_("[docs]")}</a>'
                f"{highlighted}"
            ),
        }
        yield pagename, context, "page.html"
