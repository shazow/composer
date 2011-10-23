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
    Writer only cares about the ``filters`` and ``base_path`` in the
    ``index``. It doesn't know anything about the routes, but only knows
    how to render them once they're received.
    """
    def __init__(self, index):
        self.index = index

    def render_route(self, route):
        file_path = route.file
        content = open(file_path).read()

        for filter_id in route.filters:
            content = self.index.filters[filter_id](content, route=route)

        return content

    def __call__(self, path):
        route = self.index.get_route(path)
        if route:
            return self.render_route(route)


class WSGIWriter(Writer):

    def __call__(self, environ, start_response):

        # Translate to remove the base_url
        path = environ.get('PATH_INFO', '')
        path = os.path.relpath(path, self.index.base_url)

        content = super(WSGIWriter, self).__call__(path)

        if content is None:
            start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
            return ['Not Found']

        start_response('200 OK', [('Content-Type', 'text/html')])
        return [content]


class FileWriter(Writer):
    """
    Writer who creates a static filesystem structure to mimic the desired url
    structures.
    """
    def __init__(self, index, build_path='build'):
        super(FileWriter, self).__init__(index)

        self.build_path = build_path

        if not os.path.exists(self.build_path):
            os.makedirs(self.build_path)

    def materialize_url(self, url, content=None, index_file='index.html'):
        url = url.lstrip('/')

        url_path = os.path.join(self.build_path, url)
        file_path = index_file and os.path.join(url_path, index_file)

        log.info("Materializing: /%s", url)

        if not os.path.exists(url_path):
            os.makedirs(url_path)

        if not file_path or not content:
            return url_path

        fp = open(file_path, 'w')
        fp.write(content)
        fp.close()

        return file_path

    def __call__(self, path):
        content = super(FileWriter, self).__call__(path)

        index_file = 'index.html'
        if path.endswith('.html'):
            # Leave .html files alone.
            # TODO: Allow other pass-through extensions like .htm?
            path, index_file = os.path.dirname(path), os.path.basename(path)

        self.materialize_url(path, content, index_file)
