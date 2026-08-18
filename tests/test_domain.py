import pytest


@pytest.mark.sphinx("html", testroot="domain-purge")
def test_domain_data_is_purged_on_reread(app, status, warning):
    """Templates of a re-read document do not survive in the domain data."""
    app.builder.build_all()
    assert "purged/template.in" in app.env.domaindata["jinja"]["template"]

    (app.srcdir / "index.rst").write_text("Nothing documented here.\n", encoding="utf8")
    app.builder.build_update()

    assert "purged/template.in" not in app.env.domaindata["jinja"]["template"]
