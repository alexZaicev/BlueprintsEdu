from gui.blueprints.blueprint import Blueprint
from utils.string_utils import StringUtils
import pygame as pg
from utils.gui_utils import Themes
from blueprints.character_blueprint import CharacterBlueprint as CB


class CharacterBlueprint(Blueprint):

    SIZE = [.25, .2]

    def __init__(self, panel):
        Blueprint.__init__(self, panel, "{}_1".format(StringUtils.get_string("ID_CHARACTER")), CB())
        # TODO improve random blueprint name generation
        self.set_custom_size(CharacterBlueprint.SIZE)
        self.change_font(pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().height * .1)))

    def get_data(self):
        data = super().get_data()
        data["type"] = StringUtils.get_string("ID_CHARACTER")
        return data
