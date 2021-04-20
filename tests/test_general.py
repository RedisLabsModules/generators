import unittest
import yaml
import tempfile
import sys
import os
sys.path.append("..")
from generator import Generator
from io import StringIO
# from mock_opts import Opts

class mockopts:

    def __init__(self, **kwargs):
        
        self.SRCDIR = None
        self.TEMPLATE = None
        self.DEST = None
        self.DEBUG = None
        self.VALIDATOR = None
        self.VARIABLES = None
        for key, val in kwargs.items():
            setattr(self, key.upper(), val)

class TestGeneral(unittest.TestCase):

    # TEMPLATE = "foo.yaml"

    MOCKDATAFILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "sample", "sample_vars.yml"))
    TEMPLATEFILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "sample", "template.j2"))

    def test_input_validation(self):
        """Test input validation"""

        with self.assertRaises(AttributeError):
            g = Generator(None)

        # validate it fails with no valid options  (template)
        with self.assertRaises(AttributeError):
            opts = mockopts()
            g = Generator(opts)

        # validate it succeeds with a source directory that exists or no source directory
        with self.assertRaises(AttributeError):
            opts = mockopts(TEMPLATE="/etc/profile", SRCDIR="/etc555")
            g = Generator(opts)

        # valid directory
        opts = mockopts(TEMPLATE="/etc/profile", SRCDIR="/etc")
        g = Generator(opts)

        # validate vars file
        with self.assertRaises(AttributeError):
            opts = mockopts(TEMPLATE="/etc/profile", VARIABLES="/asdasdasdasdsadsa")
            g = Generator(opts)

        opts = mockopts(TEMPLATE="/etc/profile", VARIABLES=self.MOCKDATAFILE)
        g = Generator(opts)

        # validate validator is a real validator
        with self.assertRaises(AttributeError):
            opts = mockopts(TEMPLATE="/etc/profile", validator="shooboomafoo")
            g = Generator(opts)

        opts = mockopts(TEMPLATE="/etc/profile", validator="yaml")
        g = Generator(opts)

    def test_varsfile(self):
        """Validate loading variables from yaml files."""
        opts = mockopts(TEMPLATE="/etc/profile", VARIABLES=self.MOCKDATAFILE)
        g = Generator(opts)
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
            g.__read_varfile__(t)

    def test_generate(self):
        """Test generating a generic template"""

        # standard case, no includes
        opts = mockopts(TEMPLATE=self.TEMPLATEFILE, VARIABLES=self.MOCKDATAFILE, SRCDIR="/etc")
        g = Generator(opts)
        result = g.generate().strip()
        expected = """
version: 2.3
author: Avi Cohen
""".strip()
        self.assertEqual(result, expected)

        t = tempfile.mktemp()
        g.generate(t)
        with open(t) as fp:
            content = fp.read().strip()
            self.assertEqual(content, expected)


if __name__ == '__main__':
    unittest.main()
