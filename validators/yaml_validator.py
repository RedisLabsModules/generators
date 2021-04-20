from validators import BaseValidator
import yaml

class YamlValidator(BaseValidator):
    
    def is_valid(self, content:str) -> bool:
        try:
            y = yaml.load(content, Loader=yaml.CLoader)
        except yaml.scanner.ScannerError:
            return False
        return True