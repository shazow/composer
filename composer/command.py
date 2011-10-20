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


def serve_command(environ):
    from .server import serve

    extra_files = []

    index_file = environ.get('index_file')
    if index_file:
        extra_files.append(index_file)

    serve(environ, use_reloader=True, extra_files=extra_files)


def build_command(environ, build_path='build', clean_build_path=False):
    from distutils.dir_util import copy_tree, remove_tree
    from .writer import FileWriter

    if clean_build_path:
        log.info("Cleaning build path: %s", build_path)
        if os.path.exists(build_path):
            remove_tree(build_path)

    writer = FileWriter(environ, build_path=build_path)

    for route in environ.get('routes', []):
        writer(route['url'])

    for static in environ.get('static', []):
        url_path = writer.materialize_url(static['url'])
        file_path = os.path.join(environ.get('base_path', ''), static['file'])
        copy_tree(file_path, url_path)


def parse_environ(data):
    default_context = data.get('default_context', {})

    routes = []
    for route in data.get('routes', []):
        context = {}
        context.update(default_context)
        context.update(route.get('context', {}))

        route['context'] = context
        routes.append(route)

    index_file = data.get('index_file')

    environ = {
        'index_file': index_file,
        'base_path': os.path.dirname(index_file or '.'),
        'routes': routes,
        'static': data.get('static', {}),
        'filters': data.get('filters', {}),
    }

    return environ



def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-v', '--verbose', dest='verbose', action='count')

    command_parser = parser.add_subparsers(dest='command')

    serve_parser = command_parser.add_parser('serve')
    serve_parser.add_argument(dest='index_file', help='JSON index file.')

    build_parser = command_parser.add_parser('build')
    build_parser.add_argument(dest='index_file', help='JSON index file.')
    build_parser.add_argument('-b', '--build-path', dest='build_path', default='build')
    build_parser.add_argument('-c', '--clean-build-path', dest='clean_build_path', action='store_true', help='Delete contents of build path before building into it.')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(asctime)s %(levelname)-5.5s %(message)s',
                            level=logging.INFO)

    if args.verbose > 1:
        logging.setLevel(logging.DEBUG)

    data = json.load(open(args.index_file))
    data['index_file'] = args.index_file

    environ = parse_environ(data)

    log.debug("Loaded environ: %r" , environ)

    if args.command == 'serve':
        serve_command(environ)

    elif args.command == 'build':
        build_command(environ, build_path=args.build_path, clean_build_path=args.clean_build_path)



if __name__ == "__main__":
    main()
