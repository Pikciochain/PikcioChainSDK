__all__ = ['Register']


class Register(object):
    """
    Safe2Contact Singleton pattern

    The singleton class makes sure that only one instance of it is ever
    created.

    This class is used to manage resources that by their very nature can
    only exist once.
    """

    _register = {}

    @staticmethod
    def get(key):
        if key in Register._register:
            return Register._register[key]

        return None

    @staticmethod
    def set(key, value):
        Register._register[key] = value

    @staticmethod
    def delete(key):
        if key in Register._register:
            del Register._register[key]
