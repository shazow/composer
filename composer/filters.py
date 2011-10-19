# composer/filters.py
# Copyright 2011 Andrey Petrov
#
# This module is part of Composer and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from markdown import markdown


def _markdown_filter(content, environ, route, **context):
    return markdown(content)

def _mako_filter(content, environ, route, **context):
    from mako.template import Template
    from mako.lookup import TemplateLookup

    lookup = TemplateLookup(directories=environ.get('mako.directories', []),
                input_encoding='utf-8', output_encoding='utf-8',
                encoding_errors='replace',
    )

    t = Template(content, lookup=lookup)

    content = t.render(environ=environ, route=route, **context)
    return content


filters = {
    'mako': _mako_filter,
    'markdown': _markdown_filter,
}

##
