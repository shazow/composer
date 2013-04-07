# composer/writer.py
# Copyright 2011 Andrey Petrov
#
# This module is part of Composer and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import codecs
import logging
import mimetypes
import os


log = logging.getLogger(__name__)


class Writer(object):
    """
    Writer only cares about the ``filters`` and ``base_path`` in the
    ``index``. It doesn't know anything about the routes, but only knows
    how to render them once they're received.
    """
    def __init__(self, index):
        self.index = index

    def _guess_content_type(self, path):
        filename = os.path.basename(path)

        if '.' not in filename: # Assume html
            return 'text/html'

        return mimetypes.guess_type(path)[0]

    def render_route(self, route):
        file_path = route.file
        with codecs.open(file_path, encoding='utf8') as fp:
            content = fp.read()

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
        content = super(WSGIWriter, self).__call__(path)

        if content is None:
            start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
            return ['Not Found']

        content_type = self._guess_content_type(path)
        if not content_type:
            content_type = 'application/octet-stream'
            log.warn("Serving literal file of unknown content type: /%s  "
                     "(Hint: Add / suffix to treat it as a directory)", path)

        start_response('200 OK', [('Content-Type', content_type)])
        return [content]


class FileWriter(Writer):
    """
    Writer who creates a static filesystem structure to mimic the desired url
    structures.
    """
    def __init__(self, index, build_path='build'):
        super(FileWriter, self).__init__(index)

        self.build_path = build_path

        self._prepare_dir(build_path)

    def _get_materialize_path(self, url, default_index_file='index.html'):
        url = url.lstrip('/')

        index_file = default_index_file
        url_index = os.path.basename(url)
        if '.' in url_index:
            index_file = url_index
            url = os.path.dirname(url)

        if not url:
            return self.build_path, index_file

        url_path = os.path.join(self.build_path, url)
        return url_path, index_file

    def _prepare_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def _write_file(self, path, content):
        fp = open(path, 'w')
        fp.write(content)
        fp.close()

    def materialize_url(self, url, content=None, default_index_file='index.html'):
        url = url.lstrip('/')

        if not self._guess_content_type(url):
            log.warn("Materializing literal file of unknown content type: /%s  "
                     "(Hint: Add '/' suffix to treat it as a directory)", url)

        log.info("Materializing: /%s", url)

        url_path, index_file = self._get_materialize_path(url, default_index_file)

        self._prepare_dir(url_path)

        file_path = index_file and os.path.join(url_path, index_file)

        if not file_path or content is None:
            return url_path

        self._write_file(file_path, content)
        return file_path

    def __call__(self, path):
        content = super(FileWriter, self).__call__(path)

        index_file = 'index.html'
        if path.endswith('.html'):
            # Leave .html files alone.
            # TODO: Allow other pass-through extensions like .htm?
            path, index_file = os.path.dirname(path), os.path.basename(path)

        self.materialize_url(path, content, index_file)
