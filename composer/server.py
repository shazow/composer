# composer/server.py
# Copyright 2011 Andrey Petrov
#
# This module is part of Composer and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
import logging

from .writer import WSGIWriter


log = logging.getLogger(__name__)


def serve(index, host='localhost', port=8080, debug=True, **kw):
    from werkzeug.wsgi import SharedDataMiddleware
    from werkzeug.serving import run_simple

    app = WSGIWriter(index)

    static_routes = dict((index.absolute_url(s.url), index.absolute_path(s.file)) for s in index.static)

    log.info("Adding static routes: %r", static_routes)
    app = SharedDataMiddleware(app, static_routes)

    run_simple(host, port, app, use_debugger=debug, **kw)
