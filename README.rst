Compose dynamic templates and markup into a static website.

Used to generate `shazow.net <http://shazow.net>`_.

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
            yield Route('post/1', 'posts/1.md', filters=['markdown'])


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


Components
==========

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

Roughly in priority-order: ::

#. More filters
#. More error handling and exceptions
#. More Tests
#. More documentation
#. ``serve`` mode: Index routes for more efficient lookup.
#. ``build`` mode: Add mtime-based checking to skip regenerating content that is already current.
#. Scaffolds (with Makefile)
#. Everything else
#. Ponies


License
=======

The MIT License (see LICENSE.txt)
