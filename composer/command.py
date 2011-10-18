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


from .server import serve


log = logging.getLogger(__name__)


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

    default_context = data.get('default_context', {})

    routes = []
    for route in data.get('routes', []):
        context = route.get('context', {})
        context.update(default_context)

        route['context'] = context
        routes.append(route)

    environ = {
        'base_path': os.path.dirname(args.routes_file),
        'routes': routes,
    }

    log.debug("Loaded environ: %r" , environ)

    if args.command == 'serve':
        serve(environ, use_reloader=True, extra_files=[args.routes_file])

    elif args.command == 'build':
        print "Not implemented yet."



if __name__ == "__main__":
    main()
