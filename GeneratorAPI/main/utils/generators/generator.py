class Generator(object):

    def __new__(cls, *args, **kwargs):
        raise AttributeError("Generator classes cannot be instantiated")

    def __init__(self):
        raise AttributeError("Generator classes cannot be instantiated")
