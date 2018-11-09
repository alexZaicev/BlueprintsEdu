from utils import logger_utils
from utils.enums.status import Status


class Blueprint(object):

    def __init__(self, name, b_type):
        self.name = name
        self.type = b_type

    def to_dict(self):
        return {
            "NAME": self.name,
            "TYPE": self.type
        }


class AttributeBlueprint(Blueprint):

    def __init__(self, name=Status.NONE, b_type=Status.NONE, data_type=Status.NONE, value=Status.NONE):
        Blueprint.__init__(self, name, b_type)
        self.__logger = logger_utils.get_logger(__name__)
        self.data_type = data_type
        self.value = value

    def to_dict(self):
        r = super().to_dict()
        r["DATA"] = {
            "TYPE": self.type,
            "VALUE": self.value
        }


class CharacterBlueprint(Blueprint):

    def __init__(self, name=Status.NONE, b_type=Status.NONE, attributes=None, functions=None, sprites=None):
        Blueprint.__init__(self, name, b_type)
        if attributes is None:
            self.attributes = list()
        else:
            self.attributes = attributes
        if functions is None:
            self.functions = list()
        else:
            self.functions = functions
        if sprites is None:
            self.sprites = list()
        else:
            self.sprites = sprites

    def to_dict(self):
        r = super().to_dict()


class FunctionBlueprint(Blueprint):

    def __init__(self, name=Status.NONE, b_type=Status.NONE, code=None):
        Blueprint.__init__(self, name, b_type)
        self.code = code


class SpriteBlueprint(Blueprint):

    def __init__(self, name=Status.NONE, b_type=Status.NONE, attributes=None, functions=None):
        Blueprint.__init__(self, name, b_type)
        if attributes is None:
            self.attributes = list()
        else:
            self.attributes = attributes
        if functions is None:
            self.functions = list()
        else:
            self.functions = functions
