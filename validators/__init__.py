import abc


VALIDATORS = ['yaml', 'circleli', ]


class BaseValidator(metaclass=abc.ABCMeta):
    """An absract base class for validators."""

    def is_valid(self, content):
        """An abstract method that returns True if the content is valid, False otherwise."""

        raise NotImplementedError("Child classes must implement the is_valid function.")


def create_validator(name:str) -> BaseValidator:
    """A function that returns the corresponding BaseValidator instance (factory)."""

    if name == "yaml":
        from .yaml_validator import YamlValidator
        yv = YamlValidator()
        return yv
    elif name == "circleci":
        from .circleci_validator import CircleCiValidator
        cv = CircleCiValidator()
        return cv

    raise AttributeError("Validator must be one of: %s" %  ', '.join(VALIDATORS))
