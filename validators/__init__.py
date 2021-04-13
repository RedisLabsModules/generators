from abc import abstractmethod


VALIDATORS = ['yaml',]


class Validator(object):

    def validate(self, name, content):
        if name == "yaml":
            from .yaml_validator import YamlValidator
            yv = YamlValidator()
            return yv._validate(content)

        return False

    @abstractmethod
    def _validate(self, config):
        raise NotImplementedError("Child classes must implement the validate function.")