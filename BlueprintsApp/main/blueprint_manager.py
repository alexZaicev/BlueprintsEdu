"""Description: Blueprints Manager is a special module that`s parses blueprint connections into
project '.blue' file configuration and loads that configuration to generate a working copy of a
selected game API
"""
import json
from blueprints.blueprint import Blueprint
from utils import logger_utils
from blueprints.attribute_blueprint import AttributeBlueprint


class BlueprintManager(object):

    __LOGGER = logger_utils.get_logger(__name__)

    def __init__(self):
        object.__init__(self)
        raise TypeError("Cannot instantiate static managers")

    @classmethod
    def parse_blueprints(cls, bp_conns):
        """Description: Function analyses and creates JSON-format .bp files from
        blueprint connections.
        """
        json_strs = list()
        for bp_1, bp_2 in bp_conns:
            dict_bp1 = self.__call_parser(bp_1)
            dict_bp2 = self.__call_parser(bp_1)

            json_strs.append(json.dump(dict_bp1))
            json_strs.append(json.dump(dict_bp2))

        return json_strs

    def reverse_parse_blueprints(cls, contents):
        """Descripion: Function parses JSON-format .bp file contents into relevent
        blueprint object
        """
        return list(list())

    def __call_parser(self, bp):
        func_calls = {
            Blueprint.TYPES.get("FUNCTION"): self.__parse_function,
            Blueprint.TYPES.get("SPRITE"): self.__parse_sprite,
            Blueprint.TYPES.get("CHARACTER"): self.__parse_character,
            Blueprint.TYPES.get("ATTRIBUTE"): self.__parse_attribute,
        }
        try:
            func_calls[bp.get_type()](bp)
        except KeyError as ex:
            BlueprintManager.__LOGGER.error("Unknown blueprint type {}".format(bp.get_type()))

    def __call_reverse_parser(self, bp):
        func_calls = {
            Blueprint.TYPES.get("FUNCTION"): self.__reverse_parse_function,
            Blueprint.TYPES.get("SPRITE"): self.__reverse_parse_sprite,
            Blueprint.TYPES.get("CHARACTER"): self.__reverse_parse_character,
            Blueprint.TYPES.get("ATTRIBUTE"): self.__reverse_parse_attribute,
        }
        try:
            func_calls[bp.get_type()](bp)
        except KeyError as ex:
            BlueprintManager.__LOGGER.error("Unknown blueprint type {}".format(bp.get_type()))

    def __parse_attribute(self, data):
        bp = {
            "blueprint": {
                "name": data.name,
                "type": data.get_type(),
                "data": {
                    "type": data.get_data_type(),
                    "value": data.get_value()
                }
            }
        }
        return bp

    def __parse_function(self, data):
        pass

    def __parse_sprite(self, data):
        pass

    def __parse_character(self, data):
        pass

    def __reverse_parse_attribute(self, data):
        pass

    def __reverse_parse_function(self, data):
        pass

    def __reverse_parse_sprite(self, data):
        pass

    def __reverse_parse_character(self, data):
        pass
