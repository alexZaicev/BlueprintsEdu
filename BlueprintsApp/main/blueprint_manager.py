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
    def parse_blueprints(cls, bps, bp_conns):
        """Description: Function analyses and creates JSON-format .bp files from
        blueprint connections.
        """
        data = list()
        conns = list()
        for bp, bp_rect in bps:
            d = dict()
            d["BLUEPRINT"] = BlueprintManager.call_parser(bp)
            d["RECTANGLE"] = {"COORDS": {"X": bp_rect[0][0], "Y": bp_rect[0][1]},
                              "SIZE": {"WIDTH": bp_rect[1][0], "HEIGHT": bp_rect[1][0]}}
            data.append(json.dumps(d))
        for i in range(0, len(bp_conns), 1):
            bp1, bp2 = bp_conns[i]
            d = dict()
            d[i] = {"ROOT": {"NAME": bp1.get_blueprint().name,
                             "TYPE": bp1.get_blueprint().get_type()},
                    "SLAVE": {"NAME": bp2.get_blueprint().name,
                              "TYPE": bp2.get_blueprint().get_type()}}
            conns.append(json.dumps(d))
        return data, conns

    @classmethod
    def reverse_parse_blueprints(cls, contents):
        """Descripion: Function parses JSON-format .bp file contents into relevent
        blueprint object
        """
        return list(list())

    @classmethod
    def call_parser(cls, bp):
        func_calls = {
            Blueprint.TYPES.get("FUNCTION"): BlueprintManager.parse_function,
            Blueprint.TYPES.get("SPRITE"): BlueprintManager.parse_sprite,
            Blueprint.TYPES.get("CHARACTER"): BlueprintManager.parse_character,
            Blueprint.TYPES.get("ATTRIBUTE"): BlueprintManager.parse_attribute,
        }
        try:
            return func_calls[bp.get_type()](bp)
        except KeyError as ex:
            BlueprintManager.__LOGGER.error("Unknown blueprint type {}".format(bp.get_type()))

    @classmethod
    def call_reverse_parser(self, bp):
        func_calls = {
            Blueprint.TYPES.get("FUNCTION"): BlueprintManager.reverse_parse_function,
            Blueprint.TYPES.get("SPRITE"): BlueprintManager.reverse_parse_sprite,
            Blueprint.TYPES.get("CHARACTER"): BlueprintManager.reverse_parse_character,
            Blueprint.TYPES.get("ATTRIBUTE"): BlueprintManager.reverse_parse_attribute,
        }
        try:
            return func_calls[bp.get_type()](bp)
        except KeyError as ex:
            BlueprintManager.__LOGGER.error("Unknown blueprint type {}".format(bp.get_type()))

    @classmethod
    def parse_attribute(self, data):
        bp = {
            "name": data.name,
            "type": data.get_type(),
            "data": {
                "type": data.get_data_type(),
                "value": data.get_value()
            }
        }
        return bp

    @classmethod
    def parse_function(self, data):
        pass

    @classmethod
    def parse_sprite(self, data):
        pass

    @classmethod
    def parse_character(self, data):
        pass

    @classmethod
    def reverse_parse_attribute(self, data):
        pass

    @classmethod
    def reverse_parse_function(self, data):
        pass

    @classmethod
    def reverse_parse_sprite(self, data):
        pass

    @classmethod
    def reverse_parse_character(self, data):
        pass
