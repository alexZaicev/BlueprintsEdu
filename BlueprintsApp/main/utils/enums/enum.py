class Enum(object):

    def __new__(cls, *args, **kwargs):
        raise AttributeError("Cannot create/instantiate enum data type")

    def __init__(self):
        raise AttributeError("Cannot create/instantiate enum data type")
