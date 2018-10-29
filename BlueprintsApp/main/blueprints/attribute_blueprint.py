from blueprints.blueprint import Blueprint


class AttributeBlueprint(Blueprint):

    def __init__(self):
        Blueprint.__init__(self, Blueprint.TYPES.get("ATTRIBUTE"))
        self.__data_type = "none"
        self.__value = None

    def get_data_type(self):
        return self.__data_type

    def get_value(self):
        return self.__value
