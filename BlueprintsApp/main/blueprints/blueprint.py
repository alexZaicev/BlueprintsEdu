class  Blueprint(object):

    TYPES = {
        "FUNCTION": "BT_0",
        "CHARACTER": "BT_1",
        "SPRITE": "BT_2"
    }

    def __init__(self, type):
        object().__init__(self)
        self.__type = type
