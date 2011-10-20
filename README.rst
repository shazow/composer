Compose dynamic templates and markup into a static website.

Used to generate `shazow.net <http://shazow.net>`_.

Usage
=====

TODO. For now: ::

    $ composer serve examples/simple_mako/index.json
    $ open http://localhost:8080/foo

Soon: ::

    $ composer build examples/simple_mako/index.json
    $ open build/index.html

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

* Index generator
* Build
* Copy over static stuff
* Scaffolds (with Makefile)
* Tests
* Docs
* Everything else
* Ponies
