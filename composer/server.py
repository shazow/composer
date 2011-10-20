# composer/server.py
# Copyright 2011 Andrey Petrov
#
# This module is part of Composer and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
import os

from .filters import default_filters

import logging
log = logging.getLogger(__name__)

##

def import_object(path):
    module, obj = path.split(':', 1)
    o = __import__(module, fromlist=[obj])
    return getattr(o, obj)


class ComposerApp(object):
    def __init__(self, app_environ):
        self.app_environ = app_environ

        self.filters = {}

        for filter_id, filter_conf in app_environ.get('filters', {}).iteritems():
            filter_cls = import_object(filter_conf['class'])
            self.filters[filter_id] = filter_cls(app_environ, **filter_conf.get('kwargs', {}))

        for filter_id, filter_cls in default_filters.iteritems():
            if filter_id in self.filters:
                continue

            self.filters[filter_id] = filter_cls(app_environ)

        log.debug("Loaded filters: %r" % self.filters)


    def render_route(self, route, start_response):
        self.app_environ['current_route'] = route

        start_response('200 OK', [('Content-Type', 'text/html')])

        path = lambda p: os.path.join(self.app_environ.get('base_path', ''), p)

        file_path = path(route.get('file'))
        content = open(file_path).read()

        for filter_id in route.get('filters'):
            context = {}
            context.update(route.get('context', {}))
            content = self.filters[filter_id](content, **context)

        return [content]

    def __call__(self, environ, start_response):
        environ['composer'] = self.app_environ

        path = environ.get('PATH_INFO', '').lstrip('/')

        for route in self.app_environ.get('routes', []):
            # TODO: Should we pre-index this in init?

            if route.get('url') == path:
                log.info("Route matched: %s", path)
                return self.render_route(route, start_response)

        start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
        return ['Not Found']


##

def serve(environ, host='localhost', port=8080, debug=True, **kw):
    from werkzeug.wsgi import SharedDataMiddleware
    from werkzeug.serving import run_simple

    path = lambda p: os.path.join(environ.get('base_path', ''), p)

    app = ComposerApp(environ)

    static_routes = dict((r['url'], path(r['path'])) for r in environ.get('static', []))

    log.info("Adding static routes: %r", static_routes)
    app = SharedDataMiddleware(app, static_routes)

    run_simple(host, port, app, use_debugger=debug, **kw)
