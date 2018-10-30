class SecurityManager(object):

    def __init__(self):
        object.__init__(self)
        raise TypeError("Cannot instantiate static managers")

    @classmethod
    def encode_data(cls, data):
        pass

    @classmethod
    def decode_data(cls, e_data):
        pass
