from copy import deepcopy


class Prototype:
    keep_shallow = ()
    ignore = ()

    def copy(self):
        to_copy = {
            attr_name: attr_value
            for (attr_name, attr_value) in self.__dict__.items()
            if not (attr_name in self.ignore)}
        shallow = {
            attr_name: attr_value
            for (attr_name, attr_value) in to_copy.items()
            if attr_name in self.keep_shallow
        }
        deep = {
            attr_name: deepcopy(attr_value)
            for (attr_name, attr_value) in to_copy.items()
            if not (attr_name in self.keep_shallow)
        }
        return self.__class__(**shallow, **deep)


class Spawner:

    def __init__(self, prototype: Prototype):
        self._prototype = prototype

    def spawn(self, **kwargs):
        new_entity = self._prototype.copy()
        for (attr_name, attr_value) in kwargs.items():
            setattr(new_entity, attr_name, attr_value)
        return new_entity
