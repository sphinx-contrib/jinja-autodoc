import pytest

from jinja_autodoc.viewsource import template_source_path


@pytest.mark.sphinx("html", testroot="viewsource")
def test_source_page(app, status, warning):
    """Documented templates get a link to a page displaying their source."""
    app.builder.build_all()
    index = (app.outdir / "index.html").read_text(encoding="utf8")
    assert "_jinja/greeting.html.html" in index
    assert index.count("[source]") == 1

    page = (app.outdir / "_jinja" / "greeting.html.html").read_text(encoding="utf8")
    assert "Hello" in page
    assert "[docs]" in page


@pytest.mark.sphinx("html", testroot="viewsource")
def test_no_page_outside_the_template_root(app, status, warning):
    """Only templates living in the template root get a source page."""
    app.builder.build_all()
    pages = sorted(path.name for path in (app.outdir / "_jinja").iterdir())
    assert pages == ["greeting.html.html"]


@pytest.mark.sphinx("text", testroot="viewsource")
def test_unsupported_builder(app, status, warning):
    """Builders that cannot link to the source pages get no link at all."""
    app.builder.build_all()
    assert "[source]" not in (app.outdir / "index.txt").read_text(encoding="utf8")


def test_template_source_path(tmp_path):
    """Signatures escaping the template root are rejected."""
    root = tmp_path / "templates"
    root.mkdir()
    template = root / "greeting.html"
    template.write_text("{# doc #}\n")
    outside = tmp_path / "conf.py"
    outside.write_text("{# doc #}\n")

    assert template_source_path(str(root), "greeting.html") == str(template)
    assert template_source_path(str(root), "unknown.html") is None
    assert template_source_path(str(root), "") is None
    assert template_source_path(str(root), "../conf.py") is None
    assert template_source_path(str(root), str(outside)) is None
    assert template_source_path("", "greeting.html") is None


@pytest.mark.sphinx("singlehtml", testroot="viewsource")
def test_unsupported_html_builder(app, status, warning):
    """HTML builders that cannot reach the source pages do not get them."""
    app.builder.build_all()
    assert "[source]" not in (app.outdir / "index.html").read_text(encoding="utf8")
    assert not (app.outdir / "_jinja").exists()


@pytest.mark.sphinx("epub", testroot="viewsource")
def test_epub_builder(app, status, warning):
    """Source pages are not generated for epub, which cannot list them."""
    app.builder.build_all()
    assert not (app.outdir / "_jinja").exists()
