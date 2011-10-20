# composer/filters.py
# Copyright 2011 Andrey Petrov
#
# This module is part of Composer and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import os

class Filter(object):
    def __init__(self, environ):
        self.environ = environ

    def __call__(self, content, **context):
        return content


class Markdown(Filter):
    def __call__(self, content, **context):
        from markdown import markdown
        return markdown(content)


class Mako(Filter):
    def __init__(self, environ, **lookup_kw):
        super(Mako, self).__init__(environ)

        from mako.lookup import TemplateLookup

        kw = dict(input_encoding='utf-8', output_encoding='utf-8', encoding_errors='replace')
        kw.update(lookup_kw)

        self.lookup = TemplateLookup(**kw)


    def __call__(self, content, **context):
        from mako.template import Template
        t = Template(content, lookup=self.lookup)

        route = self.environ.get('current_route')
        return str(t.render(environ=self.environ, route=route, **context))


class MakoContainer(Mako):
    """
    Similar to Mako except it loads the template from a given ``template`` and
    pipes the ``content`` into the ``body`` context variable.
    """
    def __init__(self, environ, template, **lookup_kw):
        super(MakoContainer, self).__init__(environ, **lookup_kw)

        path = lambda p: os.path.join(self.environ.get('base_path', ''), p)

        self.template = self.lookup.get_template(path(template))

    def __call__(self, content, **context):
        route = self.environ.get('current_route')
        return str(self.template.render(environ=self.environ, route=route, body=content, **context))


default_filters = {
    'mako': Mako,
    'markdown': Markdown,
}
