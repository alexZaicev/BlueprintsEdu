class Manager(object):

    def __new__(cls, *args, **kwargs):
        raise AttributeError("Cannot instantiate static manager classes")

    def __init__(self):
        raise AttributeError("Cannot instantiate static manager classes")
