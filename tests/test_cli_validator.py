import unittest
import sys
sys.path.append("..")
from validators import create_validator


class TestCLIValidator(unittest.TestCase):

    def test_validation(self):
        """Test cli validation"""

        result = """
version: 2.1

jobs:
  build:
    docker:
      - image: circleci/<language>:<version TAG>
        auth:
          username: mydockerhub-user
          password: $DOCKERHUB_PASSWORD  # context / project UI env-var reference
    steps:
      - checkout
      - run: echo "this is the build job"
  test:
    docker:
      - image: circleci/<language>:<version TAG>
        auth:
          username: mydockerhub-user
          password: $DOCKERHUB_PASSWORD  # context / project UI env-var reference
    steps:
      - checkout
      - run: echo "this is the test job"

workflows:
  build_and_test:
    jobs:
      - build
      - test:
          requires:
            - build"""

        c = create_validator("circleci")
        self.assertTrue(c.is_valid(result))

        broken = """
asdsadsadsadsadadAS
asdsaddsa: asdasdsad: asdasdsa: asdasd
"""
        c = create_validator("circleci")
        self.assertFalse(c.is_valid(broken))

if __name__ == "__main__":
    unittest.main()
