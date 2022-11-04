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

    def __eq__(self, other):
        for key in self.__dict__:
            if getattr(self, key) != getattr(other, key):
                return False
        return True
