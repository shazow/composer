#!/usr/bin/env python

from composer.index import Index, Route, Static
from composer.filters import MakoContainer


class SimpleIndex(Index):

    def _register_filters(self):
        super(SimpleIndex, self)._register_filters()
        self.register_filter('post', MakoContainer, {'directories': ['.'], 'template': 'post.mako'})

    def _generate_static(self):
        yield Static('/static', 'static')

    def _generate_routes(self):
        context = {'title': 'Hello'}

        for path in self.walk(include_only=['*.mako'], exclude=['post.mako']):
            url = self.absolute_url(path.split('.')[0])
            yield Route(url, path, filters=['mako'], context=context)

        for path in self.walk('posts', include_only=['*.md']):
            url = self.absolute_url('post/%s' % path.split('/', 1)[1].split('.')[0])
            yield Route(url, path, filters=['markdown', 'mako'], context=context)

if __name__ == '__main__':
    import json
    import os

    index = SimpleIndex(os.path.dirname(__file__))
    print json.dumps(index.to_dict(), indent=4)
