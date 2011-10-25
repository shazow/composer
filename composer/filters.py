# composer/filters.py
# Copyright 2011 Andrey Petrov
#
# This module is part of Composer and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import os

try:
    import markdown2
except ImportError:
    markdown2 = False

try:
    import mako.lookup
    import mako.template
except ImportError:
    mako = False


__all__ = ['Filter', 'Markdown', 'Mako', 'MakoContainer']


class Filter(object):
    def __init__(self, index):
        self.index = index

    def __call__(self, content, route=None):
        """
        :param content:
            String to filter, such as the contents of a file.

        :param route:
            Route object that contains a ``context`` property.
        """
        return content


class Markdown(Filter):
    def __init__(self, index, **markdown_kw):
        if not markdown2:
            raise ImportError("Markdown filter requires the 'markdown2' package to be installed.")

        super(Markdown, self).__init__(index)
        self.markdowner = markdown2.Markdown(**markdown_kw).convert

    def __call__(self, content, route=None):
        return self.markdowner(content)


class Mako(Filter):
    def __init__(self, index, **template_kw):
        if not mako:
            raise ImportError("Mako filter requires the 'Mako' package to be installed.")

        super(Mako, self).__init__(index)

        from mako.lookup import TemplateLookup

        kw = dict(input_encoding='utf-8', output_encoding='utf-8', encoding_errors='replace')
        kw.update(template_kw)

        self.template_kw = kw
        self.lookup = TemplateLookup(**self.template_kw)


    def __call__(self, content, route=None):
        from mako.template import Template
        t = Template(content, lookup=self.lookup, input_encoding='utf-8', output_encoding='utf-8', encoding_errors='replace')

        return str(t.render(index=self.index, route=route))


class MakoContainer(Mako):
    """
    Similar to Mako except it loads the template from a given ``template`` and
    pipes the ``content`` into the ``body`` context variable.
    """
    def __init__(self, index, template, **lookup_kw):
        if not mako:
            raise ImportError("MakoContainer filter requires the 'Mako' package to be installed.")

        super(MakoContainer, self).__init__(index, **lookup_kw)

        template = os.path.relpath(self.index.absolute_path(template), '.')

        self.template = self.lookup.get_template(template)

    def __call__(self, content, route=None):
        return str(self.template.render(index=self.index, body=content, route=route))


default_filters = {
    'mako': Mako,
    'markdown': Markdown,
}
