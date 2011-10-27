import sys
import unittest

sys.path.append('../')

from composer.index import Index
from composer.writer import FileWriter


class DummyFileWriter(FileWriter):
    def __init__(self, *args, **kw):
        self.reset()

        super(DummyFileWriter, self).__init__(*args, **kw)

    def reset(self):
        self._made_dirs = []
        self._written_files = []

    def _prepare_dir(self, path):
        if path not in self._made_dirs:
            self._made_dirs.append(path)

    def _write_file(self, path, content):
        self._written_files.append(path)


class TestWriter(unittest.TestCase):
    def test_file_materialize_path(self):
        w = DummyFileWriter(Index())

        self.assertEqual(w._made_dirs, ['build'])

        test_values = [
            ('/', ['build'], ['build/index.html']),
            ('/foo', ['build/foo'], ['build/foo/index.html']),
            ('/bar.html', ['build'], ['build/bar.html']),
            ('/bar.html/', ['build/bar.html/'], ['build/bar.html/index.html']),
            ('/bar.someunknownext', ['build'], ['build/bar.someunknownext']),
        ]

        for url, made_dirs, written_files in test_values:
            w.reset()
            w.materialize_url(url, '')
            self.assertEqual(w._made_dirs, made_dirs)
            self.assertEqual(w._written_files, written_files)


if __name__ == '__main__':
    unittest.main()
