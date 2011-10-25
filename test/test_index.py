import sys
import unittest

sys.path.append('../')


from composer.index import Index, Route

class TestIndex(unittest.TestCase):
    def test_routes(self):

        class TestIndex(Index):
            def _generate_routes(self):
                yield Route('/foo', 'bar', filters=['baz'], context={'quux': 42})
                yield Route('/a', 'b')

        index = TestIndex()
        r = index.to_dict()

        self.assertEqual(r['routes'], [
            {'url': '/foo', 'file': 'bar', 'context': {'quux': 42}, 'filters': ['baz']},
            {'url': '/a', 'file': 'b', 'context': None, 'filters': []},
        ])



if __name__ == '__main__':
    unittest.main()
