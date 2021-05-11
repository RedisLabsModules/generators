from validators import BaseValidator
import sys
import tempfile
import subprocess
import os

class CircleCiValidator(BaseValidator):
    """A subclass of BaseValidator. Validates CLI contents."""

    def is_valid(self, content:str) -> bool:
        """Returns True is the content is valid CLI content. Otherwise, False"""
        abspath = tempfile.mktemp(suffix=".yaml")
        with open(abspath, 'w+') as f:
            f.write(content)

        if not os.path.isfile(abspath):
            return False

        try:
            cmd = 'circleci config validate %s' % abspath
            ex = subprocess.run(cmd, capture_output=True, shell=True)
            sys.stderr.write(cmd + "\n")
            if ex.returncode != 0:
                sys.stderr.write(ex.stderr.decode('utf-8'))
                return False
            return True
        except subprocess.CalledProcessError:
            os.unlink(abspath)
            return False
        return False
