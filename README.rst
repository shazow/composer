Compose dynamic templates and markup into a static website.

Used to generate `shazow.net <http://shazow.net>`_ (`source repo <https://github.com/shazow/shazow.net>`_).

Usage
=====

Install
-------

::

    $ pip install https://github.com/shazow/composer/tarball/master
    $ pip install mako markdown2 # If you're using the built-in filters (optional)

Auto-reloading server
---------------------

Great for live preview and debugging. ::

    $ composer serve examples/simple_mako/index.json
    $ open http://localhost:8080/foo

Static build
------------

::

    $ composer build examples/simple_mako/index.json
    $ open build/foo/index.html


Write your own index file
-------------------------

We can write an indexer script which will generate our index file. ::

    #!/usr/bin/env python
    # indexer.py - Generate a Composer Index for my website.

    from composer.index import Index, Route, Static

    class SimpleIndex(Index):

        def _generate_static(self):
            yield Static('static', 'my_static_files')

        def _generate_routes(self):
            yield Route('foo', 'foo.mako', filters=['mako'])
            yield Route('post/1', 'posts/1.md', filters=['markdown', 'pygments'])


    if __name__ == '__main__':
        import json
        index = SimpleIndex()
        print json.dumps(index.to_dict(), indent=4)


Now we run the script to generate the intermediate index file and run it. ::

    $ python indexer.py > index.json
    $ composer build index.json


Or we can call the Index generator directly from Composer. This is great for
really large and complex websites. ::

    $ composer build indexer:SimpleIndex


Some examples of indexer scripts can be found here:

- https://github.com/shazow/shazow.net/blob/master/indexer.py
- https://github.com/shazow/composer/blob/master/examples/simple_mako/indexer.py


Filters
-------

A Filter is any callable factory which takes a string of content (and an
optional Route object) and returns a modified string of content. When defining a
Route, multiple filters can be chained together so that each filter's output
will be the next filter's input.

Here are two hypothetical implementations of a filter which appends a fixed
footer string to the content: ::

    # myfilter.py

    # 1. Using a class:

    from composer.filters import Filter

    class FooterFilter(Filter):
        def __init__(self, footer=''):
            self.footer = footer

        def __call__(self, content, route=None):
            return content + '\n\n' + self.footer

    # 2. Same thing without using a class:

    def FooterFilter(footer=''):
        def _(content, route=None):
            return content + '\n\n' + footer
        return _


Now we can register our FooterFilter in our Index and use it in our Routes: ::

    # ...
    from myfilter import FooterFilter

    class SimpleIndex(Index):
        def _register_filters(self):
            self.register_filter(id='footer',
                                 filter_cls=FooterFilter,
                                 filter_kwargs={'footer': '<!-- Generated by Composer -->'})

        # ...


Composer comes with a few builtin filters whose source should be easy to
understand and extend. Default registered filters include:

* ``mako``: `composer.filters.Mako <https://github.com/shazow/composer/blob/master/composer/filters.py>`_
* ``markdown``: `composer.filters.Markdown <https://github.com/shazow/composer/blob/master/composer/filters.py>`_
* ``rst``: `composer.filters.RestructuredText <https://github.com/shazow/composer/blob/master/composer/filters.py>`_
* ``jinja2``: `composer.filters.Jinja2 <https://github.com/shazow/composer/blob/master/composer/filters.py>`_
* ``pygments``: `composer.filters.Pygments <https://github.com/shazow/composer/blob/master/composer/filters.py>`_

These filters are registered by default within
``Index._register_default_filters()``. There are also some builtin unregistered
filters (such as
`composer.filters.MakoContainer <https://github.com/shazow/composer/blob/master/composer/filters.py>`_)
which can be registered manually or extended.


Components and Philosophy
=========================

Composer builds static websites in two steps: First we index, then we compose.

During indexing, we can output a ``index.json`` file which describes all the
route URLs and how to render them. We feed the index into composer to generate
static content--this can be done with the JSON file or the Index generator can
be plugged in directly.

This makes the composing step really simple because all the complex logic is
separately assembled and can be flattened into a JSON file.

Every complex setup seems to require a unique indexing step, so this allows you
to customize just the piece that is applicable to you while letting Composer do
what it does best.


TODO
====

Roughly in priority-order:

#. More filters
#. More error handling and exceptions
#. More Tests
#. More documentation
#. Optimize for large content bases:

   #. ``serve`` mode: Index routes for more efficient lookup. (Done)
   #. ``build`` mode: Add mtime-based checking to skip regenerating content that is already current.

#. Scaffolds (with Makefile)
#. Everything else
#. Ponies


License
=======

The MIT License (see LICENSE.txt)
