from blueprints.blueprint import Blueprint
from utils import logger_utils
import json

NONE = "none"
INT = "int"
FLOAT = "float"
STRING = "string"
CHAR = "char"


class AttributeBlueprint(Blueprint):

    def __init__(self, data_type=NONE):
        Blueprint.__init__(self, Blueprint.TYPES.get("ATTRIBUTE"))
        self.__logger = logger_utils.get_logger(__name__)
        self.__data_type = data_type
        self.__value = None

    def get_data_type(self):
        return self.__data_type

    def set_data_type(self, value):
        self.__data_type = value

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value
