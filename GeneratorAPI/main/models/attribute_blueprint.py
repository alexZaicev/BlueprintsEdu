from models.blueprint import Blueprint
from utils import logger_utils

NONE = "none"
INT = "int"
FLOAT = "float"
STRING = "string"
CHAR = "char"


class AttributeBlueprint(Blueprint):

    def __init__(self, data):
        Blueprint.__init__(self, data)
        self.__logger = logger_utils.get_logger(__name__)
        self.data_type = data.get("DATA").get("TYPE")
        self.value = data.get("DATA").get("VALUE")

