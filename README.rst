Compose dynamic templates and markup into a static website.

Usage
=====

::

    $ mkdir templates
    $ touch templates/index.html.mako
    $ composer --build-dir ./build --source-dir ./templates
    $ find build


Components
==========

Route Generator
---------------

An iterable which returns a tuple of ``url`` and content.


Controller
----------

Takes requests from the Route Generator and returns HTML.

TODO: How should a controller be called?


Writer
------

Outputs values from the Route Generator into the appropriate file paths on the
filesystem.


TODO
====

* Copy over static stuff
* Scaffolds (with Makefile)
* Filters and plugins and pre/post processors.
* Tests
* Docs
* Everything else
* Ponies
