"""Description: Blueprints Manager is a special module that`s parses blueprint connections into
project '.blue' file configuration and loads that configuration to generate a working copy of a
selected game API
"""
import json
from blueprints.blueprint import Blueprint
from utils import logger_utils
from blueprints.attribute_blueprint import AttributeBlueprint as AB
from blueprints.character_blueprint import CharacterBlueprint as CB
from gui.blueprints.attribute_blueprint import AttributeBlueprint
from gui.blueprints.character_blueprint import CharacterBlueprint
from blueprints.function_blueprint import FunctionBlueprint as FB
from blueprints.sprite_blueprint import SpriteBlueprint as SB
from gui.blueprints.function_blueprint import FunctionBlueprint
from gui.blueprints.sprite_blueprint import SpriteBlueprint


class BlueprintManager(object):
    __LOGGER = logger_utils.get_logger(__name__)

    def __init__(self):
        object.__init__(self)
        raise TypeError("Cannot instantiate static managers")

    @classmethod
    def generate_connections(cls, content, bps):
        bp_conns = list()
        for conn in content:
            for k, v in conn.items():
                root, slave = None, None
                for bp in bps:
                    if v.get("ROOT").get("NAME") == bp.get_blueprint().name and \
                            v.get("ROOT").get("TYPE") == bp.get_blueprint().get_type():
                        root = bp
                    elif v.get("SLAVE").get("NAME") == bp.get_blueprint().name and \
                            v.get("SLAVE").get("TYPE") == bp.get_blueprint().get_type():
                        slave = bp
                if (root is not None) and (slave is not None):
                    bp_conns.append([root, slave])

        return bp_conns

    @classmethod
    def parse_blueprints(cls, bps, bp_conns):
        """Description: Function analyses and creates JSON-format .bp files from
        blueprint connections.
        """
        data = dict()
        conns = list()
        for bp, bp_rect in bps:
            d = dict()
            d["BLUEPRINT"] = BlueprintManager.call_parser(bp)
            d["RECTANGLE"] = {"COORDS": {"X": bp_rect[0][0], "Y": bp_rect[0][1]},
                              "SIZE": {"WIDTH": bp_rect[1][0], "HEIGHT": bp_rect[1][1]}}
            data[bp.name] = json.dumps(d)
        for i in range(0, len(bp_conns), 1):
            bp1, bp2 = bp_conns[i]
            d = dict()
            d[i] = {"ROOT": {"NAME": bp1.get_blueprint().name,
                             "TYPE": bp1.get_blueprint().get_type()},
                    "SLAVE": {"NAME": bp2.get_blueprint().name,
                              "TYPE": bp2.get_blueprint().get_type()}}
            conns.append(d)
        return data, conns

    @classmethod
    def reverse_parse_blueprints(cls, panel, contents):
        """Descripion: Function parses JSON-format .bp file contents into relevent
        blueprint object
        """
        r = list()
        BlueprintManager.__LOGGER.debug(contents)
        for d in contents:
            r.append(BlueprintManager.call_reverse_parser(panel, d))
        return r

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
    def call_reverse_parser(cls, panel, bp):
        func_calls = {
            Blueprint.TYPES.get("FUNCTION"): BlueprintManager.reverse_parse_function,
            Blueprint.TYPES.get("SPRITE"): BlueprintManager.reverse_parse_sprite,
            Blueprint.TYPES.get("CHARACTER"): BlueprintManager.reverse_parse_character,
            Blueprint.TYPES.get("ATTRIBUTE"): BlueprintManager.reverse_parse_attribute,
        }
        try:
            return func_calls[bp.get("BLUEPRINT").get("TYPE")](panel, bp)
        except KeyError as ex:
            BlueprintManager.__LOGGER.error("Unknown blueprint type {}".format(bp.get("BLUEPRINT").get("TYPE")))

    @classmethod
    def get_general_data(cls, data):
        return {"NAME": data.name,
                "TYPE": data.get_type()
                }

    @classmethod
    def parse_attribute(cls, data):
        bp = BlueprintManager.get_general_data(data)
        d = dict()
        d["TYPE"] = data.get_data_type()
        d["NAME"] = data.get_value()
        bp["DATA"] = d
        return bp

    @classmethod
    def parse_function(cls, data):
        bp = BlueprintManager.get_general_data(data)
        bp["CODE"] = data.code
        return bp

    @classmethod
    def parse_sprite(cls, data):
        bp = BlueprintManager.get_general_data(data)
        bp["ATTRIBUTES"] = data.attributes
        bp["FUNCTIONS"] = data.functions
        return bp

    @classmethod
    def parse_character(cls, data):
        bp = BlueprintManager.get_general_data(data)
        bp["ATTRIBUTES"] = data.attributes
        bp["FUNCTIONS"] = data.functions
        bp["SPRITES"] = data.sprites
        return bp

    @classmethod
    def reverse_parse_attribute(cls, panel, data):
        d, r = data.get("BLUEPRINT"), data.get("RECTANGLE")
        bp = AB(name=d.get("NAME"), data_type=d.get("DATA").get("TYPE"), value=d.get("DATA").get("VALUE"))
        bp_gui = AttributeBlueprint(panel)
        bp_gui.initialize(
            (r.get("COORDS").get("X"), r.get("COORDS").get("Y")),
            (r.get("SIZE").get("WIDTH"), r.get("SIZE").get("HEIGHT")),
            bp, panel
        )
        return bp_gui

    @classmethod
    def reverse_parse_function(cls, panel, data):
        d, r = data.get("BLUEPRINT"), data.get("RECTANGLE")
        bp = FB(name=d.get("NAME"))
        bp_gui = FunctionBlueprint(panel)
        bp_gui.initialize(
            (r.get("COORDS").get("X"), r.get("COORDS").get("Y")),
            (r.get("SIZE").get("WIDTH"), r.get("SIZE").get("HEIGHT")),
            bp, panel
        )
        return bp_gui

    @classmethod
    def reverse_parse_sprite(cls, panel, data):
        d, r = data.get("BLUEPRINT"), data.get("RECTANGLE")
        bp = SB(name=d.get("NAME"))
        bp_gui = SpriteBlueprint(panel)
        bp_gui.initialize(
            (r.get("COORDS").get("X"), r.get("COORDS").get("Y")),
            (r.get("SIZE").get("WIDTH"), r.get("SIZE").get("HEIGHT")),
            bp, panel
        )
        return bp_gui

    @classmethod
    def reverse_parse_character(cls, panel, data):
        d, r = data.get("BLUEPRINT"), data.get("RECTANGLE")
        bp = CB(name=d.get("NAME"))
        bp_gui = CharacterBlueprint(panel)
        bp_gui.initialize(
            (r.get("COORDS").get("X"), r.get("COORDS").get("Y")),
            (r.get("SIZE").get("WIDTH"), r.get("SIZE").get("HEIGHT")),
            bp, panel
        )
        return bp_gui
