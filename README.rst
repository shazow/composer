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
    # indexer.py - Generate index JSON for my website.

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


Now run the script to generate the intermediate index file. ::

    $ python indexer.py > index.json


Some examples of indexer scripts can be found here:

- https://github.com/shazow/shazow.net/blob/master/indexer.py
- https://github.com/shazow/composer/blob/master/examples/simple_mako/indexer.py


Soon: The plan is to make the intermediate index file optional. You'll be able
to plug the Index class directly into Composer.


Components
==========

Composer builds static websites in two steps: First we index, then we compose.

During indexing, we generate a ``index.json`` file which describes all the
route URLs and how to render them. Second, we feed the index file into composer
to generate static content.

This makes the composing step really simple because all the complex logic is
already compiled and flattened in the index file.

Every complex setup seems to require a unique indexing step, so this allows you
to customize just the piece that is applicable to you while letting Composer do
what it does best.


TODO
====

#. Error handling and exceptions
#. Tests
#. Docs
#. Scaffolds (with Makefile)
#. Everything else
#. Ponies
