# composer/writer.py
# Copyright 2011 Andrey Petrov
#
# This module is part of Composer and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import os
import logging


log = logging.getLogger(__name__)


class Writer(object):
    """
    Callable object that creates a static filesystem structure to mimic the
    desired url structures.

    The Writer doesn't know about anything except the base path of where your
    desired url structure will live. You call the resulting writer with a router
    and it blindly traverses the routes and content returned from the router.

    :param base_path:
        Base filesystem path for where the static HTML structure should be
        created.
    """
    def __init__(self, base_path):
        self.base_path = base_path

        if not os.path.exists(base_path):
            os.makedirs(base_path)

    def manifest_url(self, url, content, index_file='index.html'):
        url_path = os.path.join(self.base_path, url)

        if not os.path.exists(url_path):
            os.makedirs(url_path)

        fp = open(os.path.join(url_path, index_file), 'w')
        fp.write(content)
        fp.close()


    def __call__(self, router):

        for url, content in router:
            log.info("Writing url: ", url)
            self.manifest_url(url, content)


