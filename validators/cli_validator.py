from validators import BaseValidator
import subprocess
import tempfile
import os

class CliValidator(BaseValidator):
    
    def is_valid(self, content:str) -> bool:
        #try:

        path, abspath = tempfile.mkstemp(prefix=".circleci/",suffix=".yaml")
        with open(path, 'w') as f:
            f.write(content)

        os.system('circleci config validate')
        '''y = subprocess.check_output(["circleci config validate " + path])'''
        '''except ScannerError:
            return False
        return True '''