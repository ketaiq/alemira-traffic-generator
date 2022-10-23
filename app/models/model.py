from abc import ABC, abstractmethod


class Model(ABC):
    @abstractmethod
    def __init__(self, keys: tuple = (), *args, **kwargs):
        if args and type(args[0]) is dict:
            dictionary = args[0]
            for key, value in dictionary.items():
                if key in keys:
                    setattr(self, key, value)
        for key, value in kwargs.items():
            if key in keys:
                setattr(self, key, value)
        for key in keys:
            if key not in self.__dict__:
                setattr(self, key, None)

    @staticmethod
    @abstractmethod
    def gen_random_object() -> "Model":
        pass

    def to_dict(self) -> dict:
        data = dict()
        for field, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, Model):
                    data[field] = value.to_dict()
                else:
                    data[field] = value
        return data
