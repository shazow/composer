#!/usr/bin/env
# composer/command.py
# Copyright 2011 Andrey Petrov
#
# This module is part of Composer and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import argparse
import logging
import os


from .renderer import MakoRenderer
from .router import Router
from .writer import Writer


log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-b', '--build-dir', dest='build_dir', required=True)
    parser.add_argument('-s', '--source-dir', dest='source_dir', required=True)

    args = parser.parse_args()

    source_dir = os.path.abspath(args.source_dir)
    build_dir = os.path.abspath(args.build_dir)

    renderer = MakoRenderer(source_dir)
    router = Router(source_dir, renderer)
    writer = Writer(build_dir)

    writer(router)


if __name__ == "__main__":
    main()

