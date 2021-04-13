from validators import Validator
import yaml

class YamlValidator(Validator):
    
    def _validate(self, content):
        try:
            y = yaml.load(content, Loader=yaml.CLoader)
        except AttributeError:
            return False
        return True