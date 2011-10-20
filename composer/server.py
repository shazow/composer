# composer/server.py
# Copyright 2011 Andrey Petrov
#
# This module is part of Composer and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
import os


from .writer import WSGIWriter


import logging
log = logging.getLogger(__name__)


def serve(environ, host='localhost', port=8080, debug=True, **kw):
    from werkzeug.wsgi import SharedDataMiddleware
    from werkzeug.serving import run_simple

    path = lambda p: os.path.join(environ.get('base_path', ''), p)

    app = WSGIWriter(environ)

    static_routes = dict((r['url'], path(r['path'])) for r in environ.get('static', []))

    log.info("Adding static routes: %r", static_routes)
    app = SharedDataMiddleware(app, static_routes)

    run_simple(host, port, app, use_debugger=debug, **kw)
