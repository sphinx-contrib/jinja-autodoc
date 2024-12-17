import pytest
from bs4 import BeautifulSoup

from . import fmt


@pytest.mark.sphinx("html", testroot="jinja")
def test_jinja_directive_html(app, status, warning, file_regression):
    """Nominal test case."""
    app.builder.build_all()
    html = (app.outdir / "index.html").read_text(encoding="utf8")
    html = BeautifulSoup(html, "html.parser")
    role = html.select("dl.jinja")[0].prettify(formatter=fmt)
    file_regression.check(role, extension=".html")
