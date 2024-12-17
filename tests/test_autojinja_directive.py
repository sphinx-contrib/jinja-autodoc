import pytest
from bs4 import BeautifulSoup

from . import fmt


@pytest.mark.sphinx("html", testroot="autojinja")
def test_jinja_directive_html(app, status, warning, file_regression):
    """Nominal test case."""
    app.builder.build_all()
    html = (app.outdir / "index.html").read_text(encoding="utf8")
    html = BeautifulSoup(html, "html.parser")
    role = html.select("dl.jinja")[0].prettify(formatter=fmt)
    file_regression.check(role, extension=".html")


@pytest.mark.sphinx("html", testroot="autojinja")
def test_several_comments(app, status, warning, file_regression):
    """Test a file with several comments."""
    app.builder.build_all()
    html = (app.outdir / "multiple_comments.html").read_text(encoding="utf8")
    html = BeautifulSoup(html, "html.parser")
    role = html.select("dl.jinja")[0].prettify(formatter=fmt)
    file_regression.check(role, extension=".html")
