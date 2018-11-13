from models.blueprint import *
from utils.managers.manager import Manager


class BlueprintManager(Manager):
    TYPES = {
        "FUNCTION": "BT_0",
        "CHARACTER": "BT_1",
        "SPRITE": "BT_2",  # IMAGE
        "ATTRIBUTE": "BT_3"
    }

    __LOGGER = logger_utils.get_logger(__name__)

    @classmethod
    def call_parser(cls, bp):
        func_calls = {
            BlueprintManager.TYPES.get("FUNCTION"): BlueprintManager.parse_function,
            BlueprintManager.TYPES.get("SPRITE"): BlueprintManager.parse_sprite,
            BlueprintManager.TYPES.get("CHARACTER"): BlueprintManager.parse_character,
            BlueprintManager.TYPES.get("ATTRIBUTE"): BlueprintManager.parse_attribute,
        }
        try:
            return func_calls[bp.get("TYPE")](bp)
        except KeyError as ex:
            BlueprintManager.__LOGGER.error("Unknown blueprint type {}".format(bp.get("TYPE")))
            raise AttributeError("Unknown blueprint type {}".format(bp.get("TYPE")))

    @classmethod
    def parse_function(cls, data):
        r = FunctionBlueprint(
            data.get("NAME"), data.get("TYPE"),
            data.get("CODE")
        )
        return r

    @classmethod
    def parse_attribute(cls, data):
        r = AttributeBlueprint(
            data.get("NAME"), data.get("TYPE"),
            data.get("DATA").get("TYPE"),
            data.get("DATA").get("VALUE")
        )
        return r

    @classmethod
    def parse_sprite(cls, data):
        a, f = list(), list()
        for d in data.get("ATTRIBUTES"):
            a.append(BlueprintManager.parse_attribute(d))
        for d in data.get("FUNCTIONS"):
            f.append(BlueprintManager.parse_function(d))
        r = SpriteBlueprint(
            data.get("NAME"), data.get("TYPE"), a, f
        )
        return r

    @classmethod
    def parse_character(cls, data):
        a, f, s = list(), list(), list()
        for d in data.get("ATTRIBUTES"):
            a.append(BlueprintManager.parse_attribute(d))
        for d in data.get("FUNCTIONS"):
            f.append(BlueprintManager.parse_function(d))
        for d in data.get("SPRITES"):
            s.append(BlueprintManager.parse_sprite(d))
        r = CharacterBlueprint(
            data.get("NAME"), data.get("TYPE"), data.get("POSITION"), data.get("SIZE"), data.get("ALIVE"), a, f, s)
        return r
