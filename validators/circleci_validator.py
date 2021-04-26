from validators import BaseValidator
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

        cmd = 'circleci config validate %s' % abspath
        try:
            ex = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            ex.check_returncode()
            return True
        except subprocess.CalledProcessError:
            os.unlink(abspath)
            return False
        return False
