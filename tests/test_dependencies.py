import os

import pytest


@pytest.mark.sphinx("html", testroot="autotemplate")
def test_template_edition_triggers_rebuild(app, status, warning):
    """Documents are outdated when the templates they document change."""
    app.builder.build_all()
    assert not app.env.get_outdated_files(config_changed=False)[1]

    os.utime(app.srcdir / "sample_template.in")

    assert app.env.get_outdated_files(config_changed=False)[1] == {"index"}


@pytest.mark.sphinx("html", testroot="autotemplate")
def test_every_read_template_is_a_dependency(app, status, warning):
    """Templates without a docstring are dependencies too."""
    app.builder.build_all()
    assert {str(path) for path in app.env.dependencies["templatedir"]} == {
        str(app.srcdir / "templatedir" / "no_comment.in"),
        str(app.srcdir / "templatedir" / "template1.in"),
        str(app.srcdir / "templatedir" / "template2.in"),
    }


@pytest.mark.sphinx("html", testroot="autotemplate-missing")
def test_missing_template(app, status, warning):
    """Missing templates are reported instead of breaking the build."""
    app.builder.build_all()
    assert "missing_template.in does not exist" in warning.getvalue()
    assert not app.env.dependencies.get("index")


@pytest.mark.sphinx("html", testroot="autotemplate-unconfigured")
def test_unconfigured_template_path(app, status, warning):
    """Without a template path, templates are neither documented nor depended upon."""
    app.builder.build_all()
    html = (app.outdir / "index.html").read_text(encoding="utf8")
    assert "sample_template.in" not in html
    assert not app.env.dependencies.get("index")
