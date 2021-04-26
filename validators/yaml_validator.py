from validators import BaseValidator
import yaml

class YamlValidator(BaseValidator):
    """A subclass of BaseValidator. Validates YAML contentד."""

    def is_valid(self, content:str) -> bool:
        """Returns True is the content is valid YAML content. Otherwise, False"""

        try:
            y = yaml.load(content, Loader=yaml.CLoader)
        except yaml.scanner.ScannerError:
            return False
        return True