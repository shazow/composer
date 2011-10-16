# composer/renderer.py
# Copyright 2011 Andrey Petrov
#
# This module is part of Composer and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

# TODO: Split up the dependency-specific renderers into their own optional submodules

import logging


log = logging.getLogger(__name__)


class Renderer(object):
    pass


class HelloWorldRenderer(object):
    def __call__(self):
        return "Hello World"


class MakoRenderer(object):
    """
    :param base_path:
        Where to look for templates.
    """
    def __init__(self, base_path):
        from mako.lookup import TemplateLookup
        self.template_lookup = TemplateLookup(
            directories=[base_path],
            input_encoding='utf-8', output_encoding='utf-8',
            encoding_errors='replace',
        )

    def __call__(self, template_name=None, **render_kw):
        t = self.template_lookup.get_template(template_name)
        return t.render(**render_kw)
