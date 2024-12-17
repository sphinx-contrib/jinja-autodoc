import pytest
from bs4 import BeautifulSoup

from . import fmt


@pytest.mark.sphinx("html", testroot="autotemplate")
def test_jinja_directive_html(app, status, warning, file_regression):
    """Nominal test case."""
    app.builder.build_all()
    html = (app.outdir / "index.html").read_text(encoding="utf8")
    html = BeautifulSoup(html, "html.parser")
    role = html.select("dl.jinja")[0].prettify(formatter=fmt)
    file_regression.check(role, extension=".html")


@pytest.mark.sphinx("html", testroot="autotemplate")
def test_several_comments(app, status, warning, file_regression):
    """Test a file with several comments."""
    app.builder.build_all()
    html = (app.outdir / "multiple_comments.html").read_text(encoding="utf8")
    html = BeautifulSoup(html, "html.parser")
    role = html.select("dl.jinja")[0].prettify(formatter=fmt)
    file_regression.check(role, extension=".html")


@pytest.mark.sphinx("html", testroot="autotemplate")
def test_templatedir(app, status, warning, file_regression):
    """Test using autotemplate on a directory."""
    app.builder.build_all()
    html = (app.outdir / "templatedir.html").read_text(encoding="utf8")
    html = BeautifulSoup(html, "html.parser")
    roles = "\n".join(role.prettify(formatter=fmt) for role in html.select("dl.jinja"))
    file_regression.check(roles, extension=".html")


@pytest.mark.sphinx("html", testroot="autotemplate-pattern")
def test_file_filter(app, status, warning, file_regression):
    """Test using autotemplate on a directory with a filename filter."""
    app.builder.build_all()
    html = (app.outdir / "index.html").read_text(encoding="utf8")
    html = BeautifulSoup(html, "html.parser")
    roles = "\n".join(role.prettify(formatter=fmt) for role in html.select("dl.jinja"))
    file_regression.check(roles, extension=".html")
