class Manager(object):

    def __new__(cls, *args, **kwargs):
        raise TypeError("Cannot instantiate static manager classes")

    def __init__(self):
        raise TypeError("Cannot instantiate static manager classes")
