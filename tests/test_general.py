import unittest
import sys
import os
sys.path.append("..")
from generator import Generator
from mock_opts import Opts


class TestGeneral(unittest.TestCase):

    TEMPLATE = "foo.yaml"

    def setUp(self):
        self.OPTS = Opts()
        self.ARGS = []

    def tearDown(self):
        pass

    def test_missing_template(self):
        #self.assertFail(Generator(self.ARGS, self.OPTS))
        pass

    def test_variables_insertion(self):
        self.OPTS.TEMPLATE = "/home/avital/repositories/generators/circleci/tests/mock_data/text_variables.j2"
        self.OPTS.VARIABLES = "/home/avital/repositories/generators/circleci/tests/mock_data/variables.txt"
        g = Generator(self.ARGS, self.OPTS)
        msg = """
version: 2.3
Autor: Avi Cohen"""
        self.assertEqual(msg, g.__create_tamplate_and_render__())
        pass

    def test_include_files(self):
        pass

    def test_library_absolute_path(self):
        pass

if __name__ == '__main__':
    unittest.main()
