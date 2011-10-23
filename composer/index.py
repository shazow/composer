# composer/index.py
# Copyright 2011 Andrey Petrov
#
# This module is part of Composer and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import os
import re
import fnmatch

from .filters import default_filters


class Index(object):
    """
    :param base_path:
        Base path that the rest of the file paths should be resolved in
        relation to.
    """
    def __init__(self, base_path='', default_filters=default_filters):
        self.base_path = os.path.abspath(base_path)
        self.filters = {}

        for filter_id, filter_cls in default_filters.iteritems():
            self.register_filter(filter_id, filter_cls)

    def register_filter(self, id, filter_cls, kwargs=None):
        """
        Instantiate the filter and register it under the given id for this
        Index.

        :param id:
            Id of filter used to reference it in routes.

        :param filter_cls:
            Class or callable which gets the Index instance as the first
            argument and ``\**kwargs`` after that.

        :param kwargs:
            Dictionary of keyword arguments passed into ``filter_cls``.

        :returns: Instantiated filter object in respect to this Index.
        """
        kwargs = kwargs or {}
        self.filters[id] = filter = filter_cls(self, **kwargs)
        return filter

    def _compile_globs(self, globs_or_regexps):
        if not globs_or_regexps:
            return []

        return [re.compile(fnmatch.translate(s)) for s in globs_or_regexps if isinstance(s, basestring)]

    def _prune_paths(self, paths, exclude, include_only):
        for path in paths:
            if not any(r.match(path) for r in include_only):
                continue
            if any(r.match(path) for r in exclude):
                continue
            yield path

    def walk(self, exclude=None, include_only=None):
        """
        Walk and yield absolute paths from the Index's ``base_path``.

        :param exclude:
            List of string globs or regular expression objects to omit.

        :param include_only:
            List of string globs or regular expressions objects which one must
            match in order to be included.
        """
        # Compile globs into regexps
        exclude = self._compile_globs(exclude)
        include_only = self._compile_globs(include_only)

        for dirpath, dirnames, filenames in os.walk(self.base_path, topdown=True, followlinks=True):
            # FIXME: Should these paths be converted to absolute or relative before pruning?
            dirnames[:] = self._prune_paths(dirnames, exclude, include_only)
            filenames = self._prune_paths(filenames, exclude, include_only)
            for file in filenames:
                yield filenames

    def _absolute_path(self, path):
        """
        Get the absolute path in respect to the Index base path.
        """
        return os.path.join(self.base_path, path)

    def _relative_path(self, path, start='.'):
        """
        Get the relative path in respect to the Index base path + start.
        """
        return os.path.relpath(path, os.path.join(self.base_path, start))

    def _generate_routes(self):
        """
        Yield Route objects.
        """
        pass

    def _generate_static(self):
        """
        Yield Static objects."
        """
        pass

    @property
    def routes(self):
        return self._generate_routes()

    @property
    def static(self):
        return self._generate_static()


class Route(object):
    """
    :param url:
        Url of the route.

    :param file:
        Path of the while used to populate ``content`` if ``content` is None.

    :param filters:
        List of filter ids.

    :param context:
        Object passed into each filter.

    :param content:
        Fixed content to start the route with. If set, ignores the ``file``
        param.
    """
    def __init__(self, url=None, file=None, filters=None, context=None, content=None):
        self.url = url
        self.file = file
        self.filters = filters or []
        self.context = context
        self.content = None


class Static(object):
    def __init__(self, url, file):
        self.url = url
        self.file = file


class Indexer(object):
    """
    Abstract Interface for building an Indexer object.

    An Index is created in these steps:

    1. Walk the filesystem (or something similar) and generate routes
    2. Process and mutate the route.
       a. Extract metadata for route
       b. Assign filters for route
       c. Assign url for route
    """
    def __init__(self, **index_kw):
        self.index = Index(**index_kw)

    def _before(self):
        "Setup filters and static routes. (Called first)"
        pass

    def _after(self):
        "Clean up. (Called last)"
        pass

    def generate_routes(self):
        "Yield routes."
        pass

    def process_route(self, route):
        "Mutate the route object as necessary."
        pass

    def __call__(self):
        self._before()

        for route in self.generate_routes():
            yield self.process(route)

        self._after()
