# composer/traverser.py
# Copyright 2011 Andrey Petrov
#
# This module is part of Composer and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import itertools
import logging
import os


log = logging.getLogger(__name__)


class TraverserError(BaseException):
    pass


class Traverser(object):
    """
    Iterable object that yields tuples the content for each desired url. ::

        >>> list(mytraverser)
        [('/helloworld', '<html>Hello, world!</html>'),
         ('/', 'I am the root url.')]

    The nature of the traverser is to delegate the rendering to the appropriate
    renderer. The traverser's primary goal is to traverse all the available URLs
    and to make sure their respective content is available.

    :param base_path:
        Base filesystem path where the input content lives.
    """
    def __init__(self, base_path):
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
        for path in self._walk_suffix('.html'):
            yield self._invent_url(path, 'index.html'), open(path).read()


def compound_traversers(*traversers):
    return itertools.chain.from_iterable(traversers)



class MakoTraverser(Traverser):
    def __init__(self, base_path):
        super(MakoTraverser, self).__init__(base_path=base_path)

        from mako.lookup import TemplateLookup
        self.template_lookup = TemplateLookup(
            directories=[base_path],
            input_encoding='utf-8', output_encoding='utf-8',
            encoding_errors='replace',
        )

    def __iter__(self):
        for path in self._walk_suffix('.html.mako'):
            t = self.template_lookup.get_template(path)

            content = t.render()
            url = self._invent_url(path, 'index.html.mako')

            yield url, content


class ManifestTraverser(Traverser):
    def __init__(self, manifest_path, filters):
        self.filters = filters
        self.manifest_path = manifest_path

        if not os.path.exists(manifest_path):
            raise TraverserError("Path does not exist: %s" % manifest_path)

    def __iter__(self):
        for line in open(self.manifest_path):
            file_path, url, filters = line.split()

            content = open(file_path).read()
            for filter_name in filters.split(','):
                content = self.filters[filter_name](content)

            yield url, content
