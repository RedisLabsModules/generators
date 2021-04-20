import unittest
import sys
sys.path.append("..")
from validators import create_validator


class TestYAMLValidator(unittest.TestCase):

    def test_validation(self):
        """Test yaml validation"""

        result = "IAMVALIDYAMLWEEEE: somevalue"
        y = create_validator("yaml")
        self.assertTrue(y.is_valid(result))

        broken = """
asdsadsadsadsadadAS
asdsaddsa: asdasdsad: asdasdsa: asdasd
"""
        y = create_validator("yaml")
        self.assertFalse(y.is_valid(broken))

if __name__ == "__main__":
    unittest.main()