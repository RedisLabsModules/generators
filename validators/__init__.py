import abc


VALIDATORS = ['yaml',]


class BaseValidator(metaclass=abc.ABCMeta):

    def is_valid(self, content):
        raise NotImplementedError("Child classes must implement the validate function.")


def create_validator(name:str) -> BaseValidator:
    """
    """
    if name == "yaml":
        from .yaml_validator import YamlValidator
        yv = YamlValidator()
        return yv
    elif name == "cli":
        from .cli_validator import CliValidator
        cv = CliValidator()
        return cv

    raise AttributeError("Validator must be one of: %s" %  ', '.join(VALIDATORS))