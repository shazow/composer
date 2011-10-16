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
    :param base_path:
        Base filesystem path where the input content lives.
    """
    def __init__(self, base_path, controller):
        self.controller = controller
        self.base_path = base_path

    def walk_suffix(self, suffix):
        for root, dirs, files in os.walk(self.base_path):
            for f in files:
                if f.endswith(suffix):
                    yield f

    def invent_url(self, path, prefix=None):
        path = path.split(prefix, 1)[-1]
        return path.split('/')[-1].replace(' ', '-') # FIXME: Something more reasonable, lol


    def __call__(self):
        for path in self.walk_suffix('.html.mako'):
            # FIXME: The invent_url prefix part is shitty and doesn't work for most cases
            yield self.invent_url(path, 'index.html.mako'), self.controller(path)
