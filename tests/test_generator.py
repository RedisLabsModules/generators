import unittest
import yaml
import tempfile
import sys
import os
sys.path.append("..")
from generator import Generator


class TestGenerator(unittest.TestCase):


    MOCKVARFILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "sample", "sample_vars.yml"))
    TEMPLATEFILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "sample", "template.j2"))

    def test_input_validation(self):
        """Test input validation"""

        # validate it fails with no template
        with self.assertRaises(AttributeError):
            g = Generator(None)

        g = Generator(template=self.TEMPLATEFILE)
        
        # validate it succeeds with a source directory that exists or no source directory
        with self.assertRaises(AttributeError):
            g.generate(srcpath="/etc555")

        g.generate(srcpath="/etc")

        # validate vars file
        with self.assertRaises(AttributeError):
            g.generate(varfile="/asdasdasdasdsadsa")

        g.generate(varfile=self.MOCKVARFILE)

        # validate validator is a real validator
        with self.assertRaises(AttributeError):
            g.generate(validator="shooboomafoo")

        g.generate(validator="yaml")

    def test_varsfile(self):
        """Validate loading variables from yaml files and from list."""
        g = Generator(template=self.TEMPLATEFILE)
        g.generate(varfile=self.MOCKVARFILE)
        self.assertNotEqual(g.VARS, None)
        g.generate(varslist=['avital', 'goof'])
        self.assertNotEqual(g.VARS, None)

        broken = """
asdsadsadsadsadadAS
asdsaddsa: asdasdsad: asdasdsa: asdasdas: asdasd
"""
        t = tempfile.mktemp()
        fp = open(t, "w+")
        fp.write(broken)
        fp.close()
        with self.assertRaises(yaml.scanner.ScannerError):
            g.__read_vars__(t, None)

    def test_generate(self):
        """Test generating a generic template"""

        # standard case, no includes
        g = Generator(template=self.TEMPLATEFILE)
        result = g.generate(varfile=self.MOCKVARFILE).strip()
        expected = """
version: 2.3
author: Avi Cohen
""".strip()
        self.assertEqual(result, expected)

        # test writing to destination file
        t = tempfile.mktemp()
        g.generate(varfile=self.MOCKVARFILE, srcpath="/etc", dest=t)
        with open(t) as fp:
            content = fp.read().strip()
            self.assertEqual(content, expected)


if __name__ == '__main__':
    unittest.main()
