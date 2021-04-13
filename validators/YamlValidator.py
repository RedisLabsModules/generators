import sys
import yaml
#from Validator import Validator 


class YamlValidator():
    
    def __init__(self):
        super().__init__(self)

    def validate(self, config):
        try:
            yaml.safe_load(config)
            return config
        except:
            sys.exit('Failed to validate config.')