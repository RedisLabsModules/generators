from validators import BaseValidator
import tempfile
import os

class CliValidator(BaseValidator):
    
    def is_valid(self, content:str) -> bool:
        
        fd, abspath = tempfile.mkstemp(suffix=".yaml")
        with open(abspath, 'w+') as f:
            f.write(content)

        try:
            ex = os.system('circleci config validate %s' % abspath)
            print(ex)
            return ex == 0
        except OSError:circleci update
