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

        file_path = os.path.join(self.app_environ.get('base_path', ''), route.get('file'))
        content = open(file_path).read()

        for filter_name in route.get('filters'):
            content = filters[filter_name](content, self.app_environ, route)

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



def serve(environ, host='localhost', port=8080, **kw):
    from werkzeug.debug import DebuggedApplication
    from werkzeug.serving import run_simple

    app = ComposerApp(environ)
    app = DebuggedApplication(app, evalex=True)
    run_simple(host, port, app, **kw)

