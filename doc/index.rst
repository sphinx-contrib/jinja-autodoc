.. module:: jinja_autodoc.jinja

Documenting jinja templates
===========================

This contrib extension, :mod:`jinja_autodoc`, provides a Sphinx
domain for describing jinja templates.

In order to use it, add :mod:`jinja_autodoc` into
:data:`extensions` list of your Sphinx configuration file (:file:`conf.py`)::

    extensions = ['jinja_autodoc']

Basic usage
-----------

There are several provided :ref:`directives <directives>` that describe
jinja templates.

.. sourcecode:: rst

   .. jinja:template:: /etc/network/interfaces

      Template for network config

      :param hostname: your computer's hostname
      :type hostname: str
      :param ip: your computer's ip
      :type ip: str

will be rendered as:

.. jinja:template:: /etc/network/interfaces

  Template for network config

  :param hostname: your computer's hostname
  :type hostname: str
  :param ip: your computer's ip
  :type ip: str

.. _directives:


Automatic documentation
-----------------------

The ``autojinja`` directive generates Jinja reference documentation from a start comment in jinja template.
Basicly it just takes `docstring` between `{#` and `#}` and inserts it where you
specified `autojinja` directive.

To make everything work you also have to specify relative or absolute path
to your templates. If this option is not specified templates won't be displayed
in your documentation.
You can do this by setting `jinja_template_path` in your Sphinx configuration
(:file:`conf.py`) file.

For example, considering this template:

.. literalinclude :: sample_template.in
   :language: jinja
   :caption: sample_template.in

the following documentation:

.. sourcecode:: rst
   :caption: templates_doc.rst

   .. autojinja:: sample_template.in

will be rendered as:

    .. autojinja:: sample_template.in

If the path is a directory, all the templates inside this directory will be rendered.
To restrict the discovery to a subset of files, you can use the ``jinja_template_pattern`` to set a pattern to recognize template filenames.

.. sourcecode:: python

   jinja_template_pattern = r"\.html$"

Directives
----------

.. rst:directive:: .. jinja:template:: path

   Describes an jinja template.

.. rst:directive:: .. jinja:autojinja:: path

   Reads the first comment of a file and dynamically builds a Jinja documentation.
   If the path is a directory, the templates in the directory will be documented.

.. _resource-fields:


Author and License
==================

The :mod:`sphinxcontrib.jinja` and :mod:`sphinxcontrib.autojinja`,
parts of :mod:`sphinxcontrib`, was originally written by `Jaka Hudoklin`_,
and then `forked <https://github.com/offlinehacker/sphinxcontrib.jinjadomain>`__ and maintained
by `Yaal Coop`_ and distributed under BSD license.

The source code is mantained under `the common repository of contributed
extensions for Sphinx`__ (find the :file:`jinja` directory inside
the repository).

.. sourcecode:: console

   $ git clone git://github.com/azmeuk/sphinxcontrib.jinja.git
   $ cd jinja
   $ python setup.py install

This package is also avalible on PyPI as `sphinxcontrib-jinja`

.. _Jaka Hudoklin: http://www.offlinehacker.net/
.. _Yaal Coop: https://yaal.coop
__ https://github.com/azmeuk/sphinxcontrib.jinja
