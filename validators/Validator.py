from abc import abstractmethod


class Validator:

    def __init__(self):
        pass

    @abstractmethod
    def validate(self, config):
        pass
