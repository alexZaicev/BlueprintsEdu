

class Language(object):

    def __new__(cls, *args, **kwargs):
        raise TypeError("Cannot instantiate static language classes")

    def __init__(self):
        raise TypeError("Cannot instantiate static language classes")