import pytest
from bs4 import BeautifulSoup

TARGET = "index.html#template-emails-welcome.html"


def template_links(path):
    """Return the target and the text of every link to a documented template."""
    html = BeautifulSoup(path.read_text(encoding="utf8"), "html.parser")
    return [
        (link["href"], link.get_text())
        for link in html.select("a:has(code.jinja-template)")
    ]


@pytest.mark.sphinx("html", testroot="xref")
def test_reference_to_a_template(app, status, warning):
    """The jinja:template role links to the documentation of a template."""
    app.builder.build_all()
    assert not warning.getvalue()
    assert (TARGET, "emails/welcome.html") in template_links(
        app.outdir / "references.html"
    )


@pytest.mark.sphinx("html", testroot="xref")
def test_reference_titles(app, status, warning):
    """A leading tilde shortens the title, and an explicit title is kept."""
    app.builder.build_all()
    links = template_links(app.outdir / "references.html")
    assert (TARGET, "welcome.html") in links
    assert (TARGET, "the welcome email") in links


@pytest.mark.sphinx("html", testroot="xref")
def test_any_reference(app, status, warning):
    """Templates are resolved by the any role too."""
    app.builder.build_all()
    html = BeautifulSoup(
        (app.outdir / "references.html").read_text(encoding="utf8"), "html.parser"
    )
    links = html.select("a:has(code.any.jinja-template)")
    assert [link["href"] for link in links] == [TARGET]


@pytest.mark.sphinx("html", testroot="xref", confoverrides={"nitpicky": True})
def test_dangling_reference(app, status, warning):
    """An unknown template is reported instead of being linked."""
    app.builder.build_all()
    assert not template_links(app.outdir / "dangling.html")

    # The message itself is localized, its interpolations are not.
    warnings = warning.getvalue()
    assert "jinja:template" in warnings
    assert "emails/unknown.html" in warnings
