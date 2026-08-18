.. module:: jinja_autodoc.jinja

Documenting jinja templates
===========================

This contrib extension, :mod:`jinja_autodoc`, provides a Sphinx
domain for describing jinja templates.

This package is available on PyPI as `jinja-autodoc`.

In order to use it, add :mod:`jinja_autodoc` into
:data:`extensions` list of your Sphinx configuration file (:file:`conf.py`)::

    extensions = ['jinja_autodoc']

Basic usage
-----------

There are several provided :ref:`directives <directives>` that describe
jinja templates.

.. sourcecode:: rst

   .. jinja:template:: emails/welcome.html

      Welcome email, sent after a registration

      :param user: the user to greet
      :type user: User
      :param login_url: where the user can log in
      :type login_url: str

will be rendered as:

.. jinja:template:: emails/welcome.html

  Welcome email, sent after a registration

  :param user: the user to greet
  :type user: User
  :param login_url: where the user can log in
  :type login_url: str

.. _directives:


Automatic documentation
-----------------------

The ``autotemplate`` directive generates Jinja reference documentation from a start comment in jinja template.
Basicly it just takes `docstring` between `{#` and `#}` and inserts it where you
specified `autotemplate` directive.

To make everything work you also have to specify the path to your templates,
either absolute, or relative to the directory containing your :file:`conf.py`
file. If this option is not specified templates won't be displayed
in your documentation.
You can do this by setting `jinja_template_path` in your Sphinx configuration
(:file:`conf.py`) file.

.. versionchanged:: 0.2

   Relative paths used to be resolved against the directory ``sphinx-build`` was
   launched from. They are now resolved against the directory containing
   :file:`conf.py`, like the other Sphinx path options.

For example, considering this template:

.. literalinclude :: sample_template.in
   :language: jinja
   :caption: sample_template.in

the following documentation:

.. sourcecode:: rst
   :caption: templates_doc.rst

   .. autotemplate:: sample_template.in

will be rendered as:

    .. autotemplate:: sample_template.in

If the path is a directory, all the templates inside this directory will be rendered.
To restrict the discovery to a subset of files, you can use the ``jinja_template_pattern`` to set a pattern to recognize template filenames.

.. sourcecode:: python

   jinja_template_pattern = r"\.html$"

Documents are rebuilt when the templates they document are edited.

.. versionadded:: 0.2

   Editing a template used to leave the documentation untouched until the next
   full rebuild. Note that templates being *added to* or *removed from* a
   documented directory still go unnoticed, as Sphinx dependencies can only be
   files. Such changes need a full rebuild, with ``sphinx-build --fresh-env``.

Template sources
----------------

Documented templates get a ``[source]`` link, pointing at a page that displays
their highlighted source, the way :mod:`sphinx.ext.viewcode` does for python
modules. Only templates living inside ``jinja_template_path`` get such a page.

Templates are highlighted with the ``html+jinja`` Pygments lexer, which fits
HTML templates. If your templates are written in another language, set
``jinja_template_lexer`` to another `Pygments lexer
<https://pygments.org/languages/>`__:

.. sourcecode:: python

   jinja_template_lexer = "jinja"

.. versionadded:: 0.2

Directives
----------

.. rst:directive:: .. jinja:template:: path

   Describes an jinja template.

.. rst:directive:: .. jinja:autotemplate:: path

   Reads the first comment of a file and dynamically builds a Jinja documentation.
   If the path is a directory, the templates in the directory will be documented.

.. _resource-fields:


Author and License
==================

The project was originally written by `Jaka Hudoklin`_,
and then `forked <https://github.com/offlinehacker/sphinxcontrib.jinjadomain>`__ and maintained
by `Yaal Coop`_ and distributed under BSD license.

.. _Jaka Hudoklin: http://www.offlinehacker.net/
.. _Yaal Coop: https://yaal.coop
