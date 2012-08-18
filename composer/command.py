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

from .index import Index, import_object
from .server import serve


log = logging.getLogger(__name__)

def serve_command(index, **kw):
    serve(index, use_reloader=True, **kw)


def build_command(index, build_path='build', clean=False):
    from distutils.dir_util import copy_tree, remove_tree
    from .writer import FileWriter

    if clean:
        log.info("Cleaning build path: %s", build_path)
        if os.path.exists(build_path):
            remove_tree(build_path)

    writer = FileWriter(index, build_path=build_path)

    for route in index.routes:
        writer(route.url)

    for static in index.static:
        log.info("Copying static url: %s", static.url)
        url_path = writer.materialize_url(static.url)
        copy_tree(static.file, url_path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-v', '--verbose', dest='verbose', action='count', help="Show DEBUG messages")

    command_parser = parser.add_subparsers(dest='command', title="Commands")

    # Server:

    serve_parser = command_parser.add_parser('serve',
                                             help="Preview the result in an auto-reloading and debug-enabled server (thanks to werkzeug).")

    serve_parser.add_argument('--host', dest='serve_host', metavar='HOST', default='localhost',
                              help='(Default: %(default)s)')

    serve_parser.add_argument('--port', dest='serve_port', metavar='PORT', default=8080, type=int,
                              help='(Default: %(default)s)')

    # Build:

    build_parser = command_parser.add_parser('build',
                                             help="Compose the index into a static build of the website, ready for deploying.")

    build_parser.add_argument('--build-path', dest='build_path', metavar="DIR", default='./build',
                              help="Path to build into. (Default: %(default)s)")

    build_parser.add_argument('--clean', dest='clean', action='store_true',
                              help='Delete contents of build path before building into it.')

    # Both:

    for p in [serve_parser, build_parser]:
        p.add_argument(dest='index_path', metavar="INDEX",
                       help="")

        p.add_argument('--base-path', dest='base_path', metavar="DIR",
                       help="Treat relative paths in the Index from this path. (Default: Path of json index file or cwd when index type is object)")

        p.add_argument('--index-type', dest='index_type', default='auto',
                       choices=['auto', 'json', 'object'],
                       help="How to interpret the INDEX value. 'auto' will try "
                            "to guess, 'object' is a Python dotted object path "
                            "like 'foo.bar:MyIndex'. (Default: %(default)s)")


    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s',
                        level=logging.INFO)

    if args.verbose > 0:
        log.setLevel(logging.DEBUG)

    # FIXME: Make this next part prettier.

    extra_files = []

    if args.index_type == 'auto':
        log.debug("Unspecified index type, trying to guess based on value provided: %s", args.index_path)

    if args.index_type == 'json' or args.index_path.endswith('json'): # JSON
        log.debug("Loading index from json.")

        data = json.load(open(args.index_path))
        base_path = os.path.dirname(args.index_path)
        index = Index.from_dict(data, base_path=base_path)
        extra_files += [base_path]

    elif args.index_type == 'object' or ':' in args.index_path: # Object
        log.debug("Loading index from Python object.")

        IndexCls = import_object(args.index_path)
        index = IndexCls(base_path=os.path.curdir)

    else:
        parser.error("Couldn't guess the type of your index file, try specifying `--index-type`.")


    if args.command == 'serve':
        serve_command(index, extra_files=[args.index_path], host=args.serve_host, port=args.serve_port)

    elif args.command == 'build':
        build_command(index, build_path=args.build_path, clean=args.clean)


if __name__ == "__main__":
    main()
