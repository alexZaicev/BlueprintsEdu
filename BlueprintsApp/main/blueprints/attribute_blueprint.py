from blueprints.blueprint import Blueprint
from utils import logger_utils


class AttributeBlueprint(Blueprint):

    NONE = "none"
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    CHAR = "char"

    def __init__(self, data_type="none", value=None, name=None):
        Blueprint.__init__(self, type=Blueprint.TYPES.get("ATTRIBUTE"), name=name)
        self.__logger = logger_utils.get_logger(__name__)
        self.__data_type = data_type
        self.__value = value

    def get_data_type(self):
        return self.__data_type

    def set_data_type(self, value):
        self.__data_type = value

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value

    def to_dict(self):
        r = super().to_dict()
        r["DATA"] = {
            "TYPE": self.__data_type,
            "VALUE": self.__value
        }
        return r
