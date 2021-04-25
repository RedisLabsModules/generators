from validators import BaseValidator
import tempfile
import subprocess
import os

class CliValidator(BaseValidator):
    """A subclass of BaseValidator. Validates CLI contents."""
    
    def is_valid(self, content:str) -> bool:
        """Returns True is the content is valid CLI content. Otherwise, False"""
        fd, abspath = tempfile.mkstemp(suffix=".yaml")
        with open(abspath, 'w+') as f:
            f.write(content)

        try:
            ex = subprocess.run('circleci config validate %s' % abspath, shell=True, check=True)
            return ex == 0
        except subprocess.CalledProcessError:
            return False
        return False
