from blueprints.blueprint import Blueprint
from utils.app_utils import Colors
from utils.string_utils import StringUtils


class SystemBlueprint(Blueprint):

    SOUND_EFFECTS = {
        "NONE": "ID_NONE",
        "RIDER_ON_THE_STORM": "ID_RIDERS_ON_THE_STORM",
        "TOKYO_DRIFT": "ID_TOKYO_DRIFT"
    }

    def __init__(self, name=StringUtils.get_string("ID_SYSTEM"), size=None, colors=None,
                 music="DISABLED", board_color=None, music_effect=None):
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
        if music_effect is None:
            self.music_effect = "NONE"
        else:
            self.music_effect = music_effect
        if board_color is None:
            if len(self.colors) < 1:
                self.board_color = None
            else:
                self.board_color = list(self.colors.keys())[0]
        else:
            self.board_color = board_color

    def to_dict(self):
        r = super().to_dict()
        r["SIZE"] = self.size
        r["COLORS"] = self.colors
        r["MUSIC"] = self.music
        r["BOARD_COLOR"] = self.board_color
        r["MUSIC_EFFECT"] = self.music_effect   # name of the sound effect
        return r
