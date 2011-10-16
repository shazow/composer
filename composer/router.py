# composer/router.py
# Copyright 2011 Andrey Petrov
#
# This module is part of Composer and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import logging
import os


log = logging.getLogger(__name__)


class Router(object):
    """
    Iterable object that yields tuples the content for each desired url. ::

    >>> list(myrouter)
    [('/helloworld', '<html>Hello, world!</html>'),
     ('/', 'I am the root url.')]

    The nature of the router is to delegate the rendering to the appropriate
    renderer. The router's primary goal is to traverse all the available URLs
    and to make sure their respective content is available.

    :param base_path:
        Base filesystem path where the input content lives.
    """
    def __init__(self, base_path, controller):
        self.controller = controller
        self.base_path = base_path

    def _walk_suffix(self, suffix):
        for root, dirs, files in os.walk(self.base_path):
            for f in files:
                if f.endswith(suffix):
                    yield f

    def _invent_url(self, path, prefix=None):
        path = path.split(prefix, 1)[-1]
        return path.split('/')[-1].replace(' ', '-') # FIXME: Something more reasonable, lol


    def __iter__(self):
        for path in self._walk_suffix('.html.mako'):
            # FIXME: The invent_url prefix part is shitty and doesn't work for most cases
            yield self._invent_url(path, 'index.html.mako'), self.controller(path)
