"""Regression check for static and generated map canonical metadata."""
from html.parser import HTMLParser
from pathlib import Path
import tempfile
import shutil
import unittest
import core
import pages_b

EXPECTED = 'https://nhadat.myagentvn.com/ban-do.html'
ROOT = Path(__file__).resolve().parent.parent

class Canonicals(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.urls = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.urls.append(attrs.get('href'))

class MapIndexing(unittest.TestCase):
    def test_published_page(self):
        self.assertEqual(Canonicals((ROOT / 'ban-do.html').read_text()).urls, [EXPECTED])
    def test_generator(self):
        previous = core.OUT
        try:
            with tempfile.TemporaryDirectory() as target:
                core.OUT = target
                (Path(target) / "img").mkdir()
                shutil.copy(ROOT / "img/credits.json", Path(target) / "img/credits.json")
                pages_b.misc_pages()
                self.assertEqual(Canonicals((Path(target) / 'ban-do.html').read_text()).urls, [EXPECTED])
        finally:
            core.OUT = previous

if __name__ == '__main__':
    unittest.main()
