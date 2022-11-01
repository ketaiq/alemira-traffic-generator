from abc import ABC, abstractmethod


class Model(ABC):
    @abstractmethod
    def __init__(self, keys: tuple = (), *args, **kwargs):
        # empty constructor
        if not args and not kwargs:
            for key in keys:
                setattr(self, key, None)
        # dict constructor
        if args and type(args[0]) is dict:
            dictionary = args[0]
            for key, value in dictionary.items():
                if key in keys:
                    setattr(self, key, value)
        # key word constructor
        for key, value in kwargs.items():
            if key in keys:
                setattr(self, key, value)
        for key in keys:
            if key not in self.__dict__:
                setattr(self, key, None)

    @staticmethod
    @abstractmethod
    def gen_random_object(*args, **kwargs) -> "Model":
        pass

    @abstractmethod
    def gen_random_update(self) -> "Model":
        pass

    def to_dict(self) -> dict:
        """Return a dict excluding None."""
        data = dict()
        for field, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, Model):
                    data[field] = value.to_dict()
                else:
                    data[field] = value
        return data
