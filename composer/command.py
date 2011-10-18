#!/usr/bin/env
# composer/command.py
# Copyright 2011 Andrey Petrov
#
# This module is part of Composer and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import argparse
import logging
import os
import json


log = logging.getLogger(__name__)

##

from markdown import markdown


def _markdown_filter(content, route):
    return markdown(content)

def _mako_filter(content, route):
    from mako.template import Template
    from mako.lookup import TemplateLookup

    lookup = TemplateLookup(directories=route.get('mako.directories', []),
                input_encoding='utf-8', output_encoding='utf-8',
                encoding_errors='replace',
    )

    t = Template(content, lookup=lookup)

    content = t.render(**route)
    return content


filters = {
    'mako': _mako_filter,
    'markdown': _markdown_filter,
}

##

class ComposerApp(object):
    def __init__(self, app_environ):
        self.app_environ = app_environ

    def render_route(self, route, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])

        file_path = os.path.join(self.app_environ.get('base_path', ''), route.get('file'))
        content = open(file_path).read()

        for filter_name in route.get('filters'):
            content = filters[filter_name](content, route)

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




def serve(environ):
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, ComposerApp(environ))
    srv.serve_forever()

##


def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')

    command_parser = parser.add_subparsers(dest='command')

    serve_command = command_parser.add_parser('serve')
    serve_command.add_argument(dest='routes_file', help='Routes file.')

    build_command = command_parser.add_parser('build')
    build_command.add_argument(dest='routes_file', help='Routes file.')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(asctime)s %(levelname)-5.5s %(message)s',
                            level=logging.DEBUG)

    data = json.load(open(args.routes_file))

    routes = []
    for route in data.get('routes', []):
        route.update(data.get('default', {}))
        routes.append(route)

    environ = {
        'base_path': os.path.dirname(args.routes_file),
        'routes': routes,
    }

    log.debug("Loaded environ: %r" , environ)

    if args.command == 'serve':
        serve(environ)

    elif args.command == 'build':
        print "Not implemented yet."



if __name__ == "__main__":
    main()
