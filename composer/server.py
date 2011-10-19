# composer/server.py
# Copyright 2011 Andrey Petrov
#
# This module is part of Composer and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
import os


import logging
log = logging.getLogger(__name__)


from .filters import filters

class ComposerApp(object):
    def __init__(self, app_environ):
        self.app_environ = app_environ

    def render_route(self, route, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])

        path = lambda p: os.path.join(self.app_environ.get('base_path', ''), p)

        file_path = path(route.get('file'))
        content = open(file_path).read()

        for filter in route.get('filters'):
            context = {}
            context.update(route.get('context', {}))

            if isinstance(filter, dict):
                # FIXME: This is hacky.
                context.update(filter)
                context['body'] = content
                content = open(path(filter['file'])).read()
                filter = filter['id']

            content = filters[filter](content, self.app_environ, route, **context)

        return [str(content)]

    def __call__(self, environ, start_response):
        environ['composer'] = self.app_environ

        path = environ.get('PATH_INFO', '').lstrip('/')

        for route in self.app_environ.get('routes', []):
            if route.get('url') == path:
                log.info("Route matched: %s", path)
                return self.render_route(route, start_response)

        start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
        return ['Not Found']



def serve(environ, host='localhost', port=8080, debug=True, **kw):
    from werkzeug.debug import DebuggedApplication
    from werkzeug.wsgi import SharedDataMiddleware
    from werkzeug.serving import run_simple

    path = lambda p: os.path.join(environ.get('base_path', ''), p)

    app = ComposerApp(environ)

    static_routes = dict((r['url'], path(r['path'])) for r in environ.get('static', []))

    log.info("Adding static routes:\n%r", static_routes)
    app = SharedDataMiddleware(app, static_routes)

    if debug:
        app = DebuggedApplication(app, evalex=True)

    run_simple(host, port, app, **kw)

