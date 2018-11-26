from blueprints.blueprint import Blueprint
from utils.app_utils import Colors
from utils.string_utils import StringUtils


class SystemBlueprint(Blueprint):

    def __init__(self, name=StringUtils.get_string("ID_SYSTEM"), size=None, colors=None,
                 music="DISABLED"):
        Blueprint.__init__(self, type=Blueprint.TYPES.get("SYSTEM"), name=name)
        if size is None:
            size = (640, 480)
        self.size = size
        if colors is None:
            colors = {
                "BLACK": Colors.BLACK,
                "RED": Colors.RED,
                "WHITE": Colors.WHITE,
                "BLUE": Colors.BLUE,
                "GREEN": Colors.GREEN
            }
        self.colors = colors
        self.music = music  # SOUND EFFECTS

    def to_dict(self):
        r = super().to_dict()
        r["SIZE"] = self.size
        r["COLORS"] = self.colors
        r["MUSIC"] = self.music
        return r
