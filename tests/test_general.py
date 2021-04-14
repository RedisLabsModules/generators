import unittest
import sys
sys.path.append("..")
import generator
import os


class TestGeneral(unittest.TestCase):

    TEMPLATE = "foo.yaml"

    def setUp(self):
        self.OPTS = {'SRCDIR': None, 'TEMPLATE': None, 'DEST': None, 'DEBUG': None, 'VALIDATOR': None, 'VARIABLES': None}
        self.ARGS = []

    def tearDown(self):
        pass

    def test_not_illegal_arguments(self):
        try:
            g = Generator(self.ARGS, self.OPTS)
            self.assertFail()
        except Exception as inst:
            print(inst)
            print(inst.values)
            print(inst.args)
            print(inst.__traceback__)
            print(inst.__context__)
            self.assertEqual(inst.message, "Invalid template file.\n")

    def test_variables_insertion(self):
        pass

    def test_include_files(self):
        pass

    def test_library_absolute_path(self):
        pass

if __name__ == '__main__':
    unittest.main()
