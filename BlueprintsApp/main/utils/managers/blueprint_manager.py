"""Description: Blueprints Manager is a special module that`s parses blueprint connections into
project '.blue' file configuration and loads that configuration to generate a working copy of a
selected game API
"""
from __future__ import division

import json

from blueprints.attribute_blueprint import AttributeBlueprint as AB
from blueprints.blueprint import Blueprint
from blueprints.character_blueprint import CharacterBlueprint as CB
from blueprints.function_blueprint import FunctionBlueprint as FB
from blueprints.sprite_blueprint import SpriteBlueprint as SB
from blueprints.system_blueprint import SystemBlueprint as SYS_BP
from gui.blueprints.attribute_blueprint import AttributeBlueprint
from gui.blueprints.character_blueprint import CharacterBlueprint
from gui.blueprints.function_blueprint import FunctionBlueprint
from gui.blueprints.sprite_blueprint import SpriteBlueprint
from gui.blueprints.system_blueprint import SystemBlueprint
from utils import logger_utils
from utils.app_utils import DisplaySettings, BlueprintParseError
from utils.managers.manager import Manager


class BlueprintManager(Manager):
    __LOGGER = logger_utils.get_logger(__name__)

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
    def to_percentage(cls, value, constant):
        return int(value * 100 / constant)

    @classmethod
    def from_percentage(cls, value, constant):
        return int(constant / 100 * value)

    @classmethod
    def parse_blueprints(cls, bps, bp_conns):
        """Description: Function analyses and creates JSON-format .bp files from
        blueprint connections.
        """
        data = dict()
        conns = list()
        size = DisplaySettings.get_size_by_key()
        for bp, bp_rect in bps:
            d = dict()
            d["BLUEPRINT"] = BlueprintManager.call_parser(bp)
            d["RECTANGLE"] = {"COORDS": {"X": BlueprintManager.to_percentage(bp_rect[0][0], size[0]),
                                         "Y": BlueprintManager.to_percentage(bp_rect[0][1], size[1])},
                              "SIZE": {"WIDTH": BlueprintManager.to_percentage(bp_rect[1][0], size[0]),
                                       "HEIGHT": BlueprintManager.to_percentage(bp_rect[1][1], size[1])}}
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

        if len(r) > 0:
            # FIND SYSTEM AND ASSIGN TO BLUEPRINTS
            for b in r:
                if isinstance(b, SystemBlueprint):
                    parent = b.get_blueprint()
                    break
            else:
                raise BlueprintParseError(
                    "Failed to parse project state. System instance not present in the project")
            # FIND CHARACTER/SPRITE AND PARSE CONNECTIONS
            for bp in r:
                if bp.get_blueprint().get_type() == Blueprint.TYPES.get("CHARACTER"):
                    BlueprintManager.sort_character_connections(bp, r)
                    bp.parent = parent
                elif bp.get_blueprint().get_type() == Blueprint.TYPES.get("SPRITE"):
                    BlueprintManager.sort_sprite_connections(bp, r)
        return r

    @classmethod
    def call_parser(cls, bp):
        func_calls = {
            Blueprint.TYPES.get("FUNCTION"): BlueprintManager.parse_function,
            Blueprint.TYPES.get("SPRITE"): BlueprintManager.parse_sprite,
            Blueprint.TYPES.get("CHARACTER"): BlueprintManager.parse_character,
            Blueprint.TYPES.get("ATTRIBUTE"): BlueprintManager.parse_attribute,
            Blueprint.TYPES.get("SYSTEM"): BlueprintManager.parse_system
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
            Blueprint.TYPES.get("SYSTEM"): BlueprintManager.reverse_parse_system
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
        d["VALUE"] = data.get_value()
        bp["DATA"] = d
        return bp

    @classmethod
    def parse_function(cls, data):
        bp = BlueprintManager.get_general_data(data)
        bp["FUNCTION_TYPE"] = data.func_type
        bp["ORIENTATION"] = data.orientation
        bp["DIRECTIONAL"] = data.directional
        bp["KEY_PRESS"] = data.key_press
        bp["CODE"] = data.code
        return bp

    @classmethod
    def parse_sprite(cls, data):
        bp = BlueprintManager.get_general_data(data)
        d = dict()
        for att in data.attributes:
            d[att.name] = att.get_type()
        bp["ATTRIBUTES"] = d
        d = dict()
        for func in data.functions:
            d[func.name] = func.get_type()
        bp["FUNCTIONS"] = d
        return bp

    @classmethod
    def parse_character(cls, data):
        bp = BlueprintManager.get_general_data(data)
        bp["POSITION"] = list(data.pos)
        bp["SIZE"] = list(data.size)
        bp["ALIVE"] = data.alive
        d = dict()
        for att in data.attributes:
            d[att.name] = att.get_type()
        bp["ATTRIBUTES"] = d
        d = dict()
        for func in data.functions:
            d[func.name] = func.get_type()
        bp["FUNCTIONS"] = d
        d = dict()
        for sp in data.sprites:
            d[sp.name] = sp.get_type()
        bp["SPRITES"] = d
        bp["COLOR_SCHEME"] = data.color_scheme
        return bp

    @classmethod
    def parse_system(cls, data):
        bp = BlueprintManager.get_general_data(data)
        bp["SIZE"] = list(data.size)
        bp["MUSIC"] = data.music
        bp["COLORS"] = data.colors
        bp["MUSIC_EFFECT"] = data.music_effect
        return bp

    @classmethod
    def reverse_parse_system(cls, panel, data):
        d, r = data.get("BLUEPRINT"), BlueprintManager.extract_rect(data.get("RECTANGLE"))
        bp = SYS_BP(name=d.get("NAME"), size=d.get("SIZE"), music=d.get("MUSIC"),
                    colors=d.get("COLORS"), music_effect=d.get("MUSIC_EFFECT"))
        bp_gui = SystemBlueprint(panel)
        bp_gui.initialize(
            r[0], r[1],
            bp, panel
        )
        return bp_gui

    @classmethod
    def reverse_parse_attribute(cls, panel, data):
        d, r = data.get("BLUEPRINT"), BlueprintManager.extract_rect(data.get("RECTANGLE"))
        bp = AB(name=d.get("NAME"), data_type=d.get("DATA").get("TYPE"), value=d.get("DATA").get("VALUE"))
        bp_gui = AttributeBlueprint(panel)
        bp_gui.initialize(
            r[0], r[1],
            bp, panel
        )
        return bp_gui

    @classmethod
    def reverse_parse_function(cls, panel, data):
        d, r = data.get("BLUEPRINT"), BlueprintManager.extract_rect(data.get("RECTANGLE"))
        bp = FB(name=d.get("NAME"), func_type=d.get("FUNCTION_TYPE"), orientation=d.get("ORIENTATION"),
                directional=d.get("DIRECTIONAL"), key_press=d.get("KEY_PRESS"))
        bp_gui = FunctionBlueprint(panel)
        bp_gui.initialize(
            r[0], r[1],
            bp, panel
        )
        return bp_gui

    @classmethod
    def extract_rect(cls, rect):
        size = DisplaySettings.get_size_by_key()
        coord = (BlueprintManager.from_percentage(rect.get("COORDS").get("X"), size[0]),
                 BlueprintManager.from_percentage(rect.get("COORDS").get("Y"), size[1]))
        size = (BlueprintManager.from_percentage(rect.get("SIZE").get("WIDTH"), size[0]),
                BlueprintManager.from_percentage(rect.get("SIZE").get("HEIGHT"), size[1]))
        return coord, size

    @classmethod
    def reverse_parse_sprite(cls, panel, data):
        d, r = data.get("BLUEPRINT"), BlueprintManager.extract_rect(data.get("RECTANGLE"))
        bp = SB(name=d.get("NAME"))
        for k, v in d.get("ATTRIBUTES").items():
            bp.attributes.append({k: v})
        for k, v in d.get("FUNCTIONS").items():
            bp.functions.append({k: v})
        bp_gui = SpriteBlueprint(panel)
        bp_gui.initialize(
            r[0], r[1],
            bp, panel
        )
        return bp_gui

    @classmethod
    def reverse_parse_character(cls, panel, data):
        d, r = data.get("BLUEPRINT"), BlueprintManager.extract_rect(data.get("RECTANGLE"))
        bp = CB(name=d.get("NAME"), pos=d.get("POSITION"), size=d.get("SIZE"), alive=d.get("ALIVE"),
                color_scheme=d.get("COLOR_SCHEME"))
        for k, v in d.get("ATTRIBUTES").items():
            bp.attributes.append({k: v})
        for k, v in d.get("FUNCTIONS").items():
            bp.functions.append({k: v})
        for k, v in d.get("SPRITES").items():
            bp.sprites.append({k: v})
        bp_gui = CharacterBlueprint(panel)
        bp_gui.initialize(
            r[0], r[1],
            bp, panel
        )
        return bp_gui

    @classmethod
    def sort_character_connections(cls, character, bp_guis):
        cb = character.get_blueprint()
        bps = [
            bp.get_blueprint() for bp in bp_guis
        ]
        # SORT ATTRIBUTES
        a, f, s = list(), list(), list()
        for att in cb.attributes:
            for bp in bps:
                name = list(att.keys())[0]
                if name == bp.name and att.get(name) == bp.get_type():
                    a.append(bp)
        # SORT FUNCTIONS
        for func in cb.functions:
            for bp in bps:
                name = list(func.keys())[0]
                if name == bp.name and func.get(name) == bp.get_type():
                    f.append(bp)
        # SORT SPRITES
        for sp in cb.sprites:
            for bp in bps:
                name = list(sp.keys())[0]
                if name == bp.name and sp.get(name) == bp.get_type():
                    s.append(bp)
        cb.attributes = a
        cb.functions = f
        cb.sprites = s

    @classmethod
    def sort_sprite_connections(cls, sprite, bp_guis):
        sb = sprite.get_blueprint()
        bps = [
            bp.get_blueprint() for bp in bp_guis
        ]
        a, f = list(), list()
        for att in sb.attributes:
            for bp in bps:
                name = list(att.keys())[0]
                if name == bp.name and att.get(name) == bp.get_type():
                    a.append(bp)
        # SORT FUNCTIONS
        for func in sb.functions:
            for bp in bps:
                name = list(func.keys())[0]
                if name == bp.name and func.get(name) == bp.get_type():
                    f.append(bp)
        sb.attributes = a
        sb.functions = f
