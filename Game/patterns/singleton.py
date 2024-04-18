from exceptions import SingletonAlreadyExists, CanNotInstantiate


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls == Singleton:
            raise CanNotInstantiate("Instantiation of base singleton class is not permitted.")
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            return cls._instance
        else:
            raise SingletonAlreadyExists(f"A singleton instance of type {cls} already exists.")
