import pytest
from sphinx.util.parallel import parallel_available


@pytest.mark.sphinx("html", testroot="domain-purge")
def test_domain_data_is_purged_on_reread(app, status, warning):
    """Templates of a re-read document do not survive in the domain data."""
    app.builder.build_all()
    assert "purged/template.in" in app.env.domaindata["jinja"]["template"]

    (app.srcdir / "index.rst").write_text("Nothing documented here.\n", encoding="utf8")
    app.builder.build_update()

    assert "purged/template.in" not in app.env.domaindata["jinja"]["template"]


@pytest.mark.skipif(not parallel_available, reason="requires forking")
@pytest.mark.sphinx("html", testroot="domain-parallel", parallel=2)
def test_domain_data_is_merged_after_a_parallel_read(app, status, warning):
    """Templates read by different processes all end up in the domain data."""
    app.builder.build_all()
    assert "serial read" not in warning.getvalue()

    assert app.env.domaindata["jinja"]["template"] == {
        "first.html": ("index", "", str(app.srcdir / "first.html")),
        "second.html": ("second", "", str(app.srcdir / "second.html")),
    }
