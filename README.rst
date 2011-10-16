Compose dynamic templates and markup into a static website.

Used to generate `shazow.net <http://shazow.net>`_.

Usage
=====

::

    $ mkdir templates
    $ touch templates/index.html.mako
    $ composer --build-dir ./build --source-dir ./templates
    $ find build
    build
    build/index.html


Components
==========

Each layer tries to be as agnostic to the layer below it as possible.


Writer
------

At the top, we have the Writer. The Writer is responsible for generating the
filesystem structure and its content which corresponds to the desired URL
structure.

The Writer object is called with a Traverser iterable which yeilds tuples of
(``url``, ``content``). A most basic Writer object behaves like this: ::

    def a_writer(traverser):
        for url, content in traverser:
            fp = open(convert_to_path(url), 'w')
            fp.write(content)
            fp.close()


Traverser
---------

The traverser is responsible for figuring out all the possible URLs and fetching
the content that goes in them.

A simple Traverser object behaves like this: ::

    def a_traverser(base_path, suffix='.mako'):
        for _, _, files in os.walk(base_path):
            for f in files:
                if f.endswith(suffix):
                    yield f[:-len(suffix)], render_template(f)

Or a traverser could delegate the rendering of a URL to another component, such
as a WSGI application.


TODO
====

* Copy over static stuff
* Scaffolds (with Makefile)
* Filters and plugins and pre/post processors.
* Tests
* Docs
* Everything else
* Ponies
