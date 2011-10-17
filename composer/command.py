#!/usr/bin/env
# composer/command.py
# Copyright 2011 Andrey Petrov
#
# This module is part of Composer and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import argparse
import logging
import os


from .traverser import MakoTraverser
from .writer import Writer


log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')

    parser.add_argument('-b', '--build-dir', dest='build_dir', required=True)
    parser.add_argument('-s', '--source-dir', dest='source_dir', required=True)

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(asctime)s %(levelname)-5.5s %(message)s',
                            level=logging.DEBUG)

    source_dir = os.path.abspath(args.source_dir)
    build_dir = os.path.abspath(args.build_dir)

    traverser = MakoTraverser(source_dir)
    writer = Writer(build_dir)

    writer(traverser)


if __name__ == "__main__":
    main()
