from validators import BaseValidator
import tempfile
import os

class CliValidator(BaseValidator):
    """A subclass of BaseValidator. Validates CLI contents."""
    
    def is_valid(self, content:str) -> bool:
        """Returns True is the content is valid CLI content. Otherwise, False"""
        fd, abspath = tempfile.mkstemp(suffix=".yaml")
        with open(abspath, 'w+') as f:
            f.write(content)

        try:
            ex = os.system('circleci config validate %s' % abspath)
            return ex == 0
        except OSError:
            return False
        return False
