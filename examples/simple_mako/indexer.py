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
        yield Route('foo', 'foo.mako')
        yield Route('post/1', 'posts/1.md')

    def _process_route(self, route):
        route.context = {'title': 'Hello'}

        if route.file.endswith('md'):
            route.filters = ['markdown', 'post']
        elif route.file.endswith('mako'):
            route.filters = ['mako']

        if route.file.startswith('posts/'):
            route.url = 'post/%s' % route.file.split('/', 1)[1].split('.')[0]
        else:
            route.url = route.file.split('.')[0]

        return route


if __name__ == '__main__':
    import json
    index = SimpleIndex()
    print json.dumps(index.to_dict(), indent=4)
