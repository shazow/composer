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

try:
    import docutils.core
except ImportError:
    docutils = False

try:
    import jinja2
except ImportError:
    jinja2 = False


__all__ = ['Filter',
           'Mako', 'MakoContainer', 'Jinja2',
           'RestructuredText','Markdown']


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
        self.converter = markdown2.Markdown(**markdown_kw).convert

    def __call__(self, content, route=None):
        return self.converter(content)


class Mako(Filter):
    def __init__(self, index, **template_kw):
        if not mako:
            raise ImportError("Mako filter requires the 'Mako' package to be installed.")

        super(Mako, self).__init__(index)

        kw = dict(input_encoding='utf-8', output_encoding='utf-8', encoding_errors='replace')
        kw.update(template_kw)

        self.template_kw = kw
        self.lookup = mako.lookup.TemplateLookup(**self.template_kw)

    def __call__(self, content, route=None):
        t = mako.template.Template(content, lookup=self.lookup, **self.template_kw)

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


class RestructuredText(Filter):
    # FIXME: This is untested and probably not Best Practices compliant. Someone
    # who seriously uses RST should make this filter better.

    def __init__(self, index, **rst_kw):
        if not docutils:
            raise ImportError("RestructuredText filter requires the 'docutils' package to be installed.")

        super(RestructuredText, self).__init__(index)

        self.rst_kw = rst_kw

    def __call__(self, content, route=None):
        return docutils.core.publish_string(content, **self.rst_kw)


class Jinja2(Filter):
    # FIXME: This is untested and probably not Best Practices compliant. Someone
    # who seriously uses Jinja2 should make this filter better.

    # TODO: Make a Jinja2Container version of this Filter (similar to MakoContainer)

    def __init__(self, index, searchpaths=None):
        super(Jinja2, self).__init__(index)

        if not jinja2:
            raise ImportError("Jinja2 filter requires the 'Jinja2' package to be installed.")

        loaders = []
        if searchpaths:
            loaders.append(jinja2.FileSystemLoader(searchpaths))

        # TODO: Add support for more loaders?

        self.jinja_env = jinja2.Environment(
            loaders=jinja2.ChoiceLoaders(loaders)
        )

    def __call__(self, content, route=None):
        t = self.jinja_env.from_string(content)
        return t.render(index=self.index, route=route)



default_filters = {
    'mako': Mako,
    'markdown': Markdown,
    'rst': RestructuredText,
    'jinja2': Jinja2,
}
